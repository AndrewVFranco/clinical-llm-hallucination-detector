from typing import TypedDict, Optional

class AgentState(TypedDict):
    query: str
    has_drug_query: bool
    drug_names: Optional[list[str]]
    drug_labels: Optional[list[dict]]
    search_query: Optional[str]
    abstracts: list[dict]
    llm_response: Optional[str]
    claims: Optional[list[str]]
    scored_claims: Optional[list[dict]]
    confidence_score: Optional[float]
    final_response: Optional[dict]