from typing import TypedDict, Optional

class AgentState(TypedDict):
    query: str
    search_query: Optional[str]
    abstracts: list[dict]
    llm_response: Optional[str]
    claims: Optional[list[str]]
    scored_claims: Optional[list[dict]]
    confidence_score: Optional[float]
    final_response: Optional[dict]