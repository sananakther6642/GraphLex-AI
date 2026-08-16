from importlib import import_module

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="GraphLex Production API")

class QueryRequest(BaseModel):
    prompt: str

@app.post("/ask")
async def ask_graphlex_api(request: QueryRequest):
    """Run GraphLex for a single prompt and return the generated answer."""
    try:
        from src.engine import ask_graphlex

        answer = ask_graphlex(request.prompt)

        if not answer:
            return {
                "answer": "I'm sorry, but I couldn't find any relevant information in the internal documents to answer this safely.",
                "sources": []
            }

        return {"answer": answer, "sources": []}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
