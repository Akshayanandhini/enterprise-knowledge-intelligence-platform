from pydantic import BaseModel, Field

class ReflectionOutput(BaseModel):
    """
    Structured output produced by the reflection agent.
    """

    sufficient:bool = Field(
        description="Whether the retrieved evidence is sufficient."
    )

    retry:bool = Field(
        description="Whether retrieval should be attempted again."
    )

    feedback: str = Field(
        description="Feedback to improve retrieval. Empty if retry is not required."
    )