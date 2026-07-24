from langchain_core.prompts import ChatPromptTemplate

from app.llm.groq_client import get_llm
from app.models.answer import AnswerOutput
from app.models.chunks import Chunk


SYSTEM_PROMPT = """
You are the Answer Agent in an Agentic RAG system.

Responsibilities:

1. Answer ONLY using the retrieved evidence.
2. Never use outside knowledge.
3. If the evidence is insufficient, clearly state that.
4. Be concise and factual.
5. Include citations.
6. Return only structured output.

Examples

Example 1

Question:
What is the refund window?

Evidence:
Customers may request refunds within 30 days.

Output:
answer="The standard refund window is 30 days from the date of purchase."
citations=[
"Customer Refund Policy > Subscription Refund Terms > Standard Refund Window"
]

Example 2

Question:
How many vacation days do employees receive?

Evidence:
No information about vacation days was retrieved.

Output:
answer="The retrieved documents do not contain enough information to answer this question."
citations=[]
"""

class AnswerAgent:

    def __init__(self, api_key: str):

        self.llm = get_llm(api_key).with_structured_output(
            AnswerOutput
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_PROMPT),
                (
                    "human",
                    """
                Question:
                {query}

                Retrieved Evidence:
                {context}
                """
                ),
            ]
        )

    def answer(
        self,
        query: str,
        chunks: list[Chunk],
    ) -> AnswerOutput:

        context = ""

        citations = []

        for chunk in chunks:

            heading = " > ".join(
                chunk.metadata.heading_path
            )

            context += (
                f"Source: {heading}\n"
                f"{chunk.content}\n\n"
            )

            citations.append(heading)

        chain = self.prompt | self.llm

        return chain.invoke(
            {
                "query": query,
                "context": context,
            }
        )
if __name__ == "__main__":

    import os

    from app.retrieval.retriever import Retriever

    retriever = Retriever()

    agent = AnswerAgent(
        api_key=os.getenv("GROQ_API_KEY")
    )

    chunks = retriever.retrieve(
        "What is the standard refund window for subscription services?"
    )

    result = agent.answer(
        "What is the standard refund window for subscription services?",
        chunks,
    )

    print(result)