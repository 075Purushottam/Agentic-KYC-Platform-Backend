from typing import List, Dict, Any
from typing_extensions import TypedDict

class InvestigationState(TypedDict): 
    case_id: str 
    uploaded_docs: List[str] 
    extracted_data: Dict[str, Any] 
    risk_score: int 
    active_signals: List[str] 
    completed_agents: List[str] 
    event_logs: List[Dict[str, Any]] 
    final_decision: str
    adverse_media_results: list
    adverse_media_score: int