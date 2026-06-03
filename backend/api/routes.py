from fastapi import APIRouter 
from graph.workflow import graph 
from state.investigation_state import InvestigationState

router = APIRouter() 

@router.post("/start-investigation") 
async def start_investigation(): 
    initial_state: InvestigationState = {
        "case_id": "CASE-1001",
        "uploaded_docs": ["passport.pdf"],
        "extracted_data": {},
        "risk_score": 0,
        "active_signals": [],
        "completed_agents": [],
        "event_logs": [],
        "final_decision": "",
    }
    final_state = await graph.ainvoke(initial_state)
    return final_state

