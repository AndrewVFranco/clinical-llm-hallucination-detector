from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from src.agent.graph import agent
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

class QueryRequest(BaseModel):
    query: str

@asynccontextmanager
async def lifespan(app):
    yield
app = FastAPI(lifespan=lifespan, title="SentinelMD")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/query")
async def query(request: QueryRequest):
    try:
        result = agent.invoke({
            "query": request.query,
            "search_query": None,
            "abstracts": [],
            "llm_response": None,
            "claims": None,
            "scored_claims": None,
            "confidence_score": None,
            "final_response": None
        })

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference failed: {str(e)}")

@app.get("/health")
async def health():
    return {"status": "ok"}