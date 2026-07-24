from typing import TypedDict

from langgraph.graph import StateGraph,START,END
from app.agents.planner import Planner
from app.agents.answer import AnswerAgent
from app.agents.reflection import Reflection
from app.models.answer import AnswerOutput
from app.models.reflection import ReflectionOutput
from app.models.planner import PlannerOutput
from app.models.chunks import Chunk
from app.retrieval.retriever import Retriever
from app.core.logging import logger



class State(TypedDict):
    query: str
    api_key: str
    planner_output: PlannerOutput|None
    retrieved_chunks: list[Chunk]
    reflection_output: ReflectionOutput|None
    answer:AnswerOutput|None
    retry_count: int

retriever = Retriever()

def planner_node(state: State) -> State:

    logger.info("Planner started")

    planner = Planner(api_key=state["api_key"])

    planner_output = planner.plan(state["query"])

    logger.info(
        "Planner completed | Intent=%s | TopK=%d",
        planner_output.intent,
        planner_output.top_k,
    )

    state["planner_output"] = planner_output

    return state

def retriever_node(state: State) -> State:

    logger.info("Hybrid retrieval started")

    planner_output = state["planner_output"]

    chunks = retriever.retrieve(
        query=planner_output.rewritten_query,
        top_k=planner_output.top_k,
    )

    logger.info(
        "Retrieved %d chunks",
        len(chunks),
    )

    state["retrieved_chunks"] = chunks

    return state

def reflection_node(state: State) -> State:

    logger.info("Reflection started")

    reflection = Reflection(api_key=state["api_key"])

    result = reflection.evaluate(
        query=state["query"],
        chunks=state["retrieved_chunks"],
    )

    logger.info(
        "Reflection completed | Retry=%s",
        result.retry,
    )

    state["reflection_output"] = result

    return state

def answer_node(state: State) -> State:

    logger.info("Answer generation started")

    answer = AnswerAgent(api_key=state["api_key"])

    result = answer.answer(
        query=state["query"],
        chunks=state["retrieved_chunks"],
    )

    logger.info(
        "Answer generated | Citations=%d",
        len(result.citation),
    )

    state["answer"] = result

    return state

def should_retry(state: State):

    reflection = state["reflection_output"]

    if reflection.retry and state["retry_count"] < 1:

        logger.info("Retrying retrieval")

        state["retry_count"] += 1
        return "retry"

    logger.info("Proceeding to Answer Agent")

    return "answer"

def create_initial_state(
    query: str,
    api_key: str,
) -> State:

    return {
        "query": query,
        "api_key": api_key,
        "planner_output": None,
        "retrieved_chunks": [],
        "reflection_output": None,
        "answer": None,
        "retry_count": 0,
    }

graph = StateGraph(State, name = "Enterprise Agentic RAG")

graph.add_node("Planner",planner_node)
graph.add_node("Retriever",retriever_node)
graph.add_node("Reflection",reflection_node)
graph.add_node("Answer", answer_node)

graph.add_edge(START,"Planner")
graph.add_edge("Planner","Retriever")
graph.add_edge("Retriever","Reflection")

graph.add_conditional_edges(
    "Reflection",
    should_retry,
    {"retry":"Retriever",
    "answer":"Answer"
    }
)

graph.add_edge("Answer",END)

workflow = graph.compile()

if __name__ == "__main__":

    import os

    result = workflow.invoke(
        {
            "query": "What is the standard refund window for subscription services?",
            "api_key": os.getenv("GROQ_API_KEY"),
            "planner_output": None,
            "retrieved_chunks": [],
            "reflection_output": None,
            "answer": None,
            "retry_count": 0,
        }
    )

    print(result["answer"])