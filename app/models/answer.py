from pydantic import BaseModel, Field

class AnswerOutput(BaseModel):
    """
    Structured output produced by the answer agent.
    """

    answer:str = Field(
        description="Grounded answer to the user's question."
    )

    citation:list[str] = Field(
        description = "Citations to support the answer."
    )