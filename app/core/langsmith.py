import os

from dotenv import load_dotenv
from langsmith import tracing_context

load_dotenv()


def tracing():
    return tracing_context(
        enabled=os.getenv("LANGSMITH_TRACING", "false").lower() == "true"
    )