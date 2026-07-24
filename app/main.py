from fastapi import FastAPI, HTTPException

from app.graph.workflow import workflow, create_initial_state
from app.models.api import QueryRequest, QueryResponse
from app.core.langsmith import tracing

app = FastAPI(
    title="Enterprise Knowledge Intelligence Platform",
    version="1.0.0",
)

@app.get("/")
async def root():
    return {"status": "ok"}

@app.post("/query",response_model = QueryResponse)
async def query(request:QueryRequest):

    try:
        with tracing():

            result = workflow.invoke(
                create_initial_state(
                    request.query,
                    request.api_key,
                )
            )

        answer = result['answer']
        return QueryResponse(
            answer = answer.answer,
            citations=answer.citation
        )
    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail = str(e)
        )