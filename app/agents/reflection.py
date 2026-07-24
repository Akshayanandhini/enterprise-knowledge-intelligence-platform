from langchain_core.prompts import ChatPromptTemplate

from app.models.reflection import ReflectionOutput
from app.llm.groq_client import get_llm
from app.models.chunks import Chunk

import os
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
You are the Reflection Agent in an Agentic RAG system.

Your responsibilities:

1. Evaluate whether the retrieved evidence is sufficient.
2. Decide whether retrieval should be retried.
3. Never rewrite the query.
4. Never answer the user's question.
5. Return only structured output.

Retry ONLY when:
- The retrieved evidence is unrelated.
- The retrieved evidence is clearly insufficient.
- The retrieved evidence is missing critical information needed to answer the question.

Do NOT retry:
- If the evidence answers the question.
- If the evidence is relevant but could be more detailed.
- If the answer can be produced from the retrieved evidence.

Examples:

Example 1

Question:
What is the standard refund window for subscription services?

Evidence:
The refund policy states customers may request refunds within 30 days of purchase.

Output:
sufficient=True
retry=False
feedback=""

Example 2

Question:
How do I reset my password?

Evidence:
The retrieved documents discuss refund policies.

Output:
sufficient=False
retry=True
feedback="Retrieved evidence is unrelated to the user's question."

Example 3

Question:
Compare the refund policy and cancellation policy.

Evidence:
Only the refund policy was retrieved.

Output:
sufficient=False
retry=True
feedback="Retrieve information about the cancellation policy as well."

Example 4

Question:
Who approves annual leave?

Evidence:
The leave policy states managers approve annual leave requests.

Output:
sufficient=True
retry=False
feedback=""
"""

class Reflection:
    def __init__(self,api_key:str):
        self.llm = get_llm(api_key).with_structured_output(ReflectionOutput)

        self.prompt = ChatPromptTemplate.from_messages([
            ("system",SYSTEM_PROMPT),
            ("human","""
            Question:
            {query}
             
            Retrieved Evidence:
            {context}""")

        ])
    
    def evaluate(self, query:str, chunks:list[Chunk])->ReflectionOutput:

        context = '\n\n'.join(
            chunk.content for chunk in chunks
        )

        chain  = self.prompt|self.llm

        return chain.invoke({
            "query":query,
            "context":context
        })
    
if __name__ == "__main__":

    import os

    from app.retrieval.retriever import Retriever

    retriever = Retriever()

    reflection = Reflection(
        api_key=os.getenv("GROQ_API_KEY")
    )

    chunks = retriever.retrieve(
        "What is the standard refund window for subscription services?"
    )

    result = reflection.evaluate(
        "What is the standard refund window for subscription services?",
        chunks,
    )

    print(result)