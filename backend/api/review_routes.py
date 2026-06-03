from pydantic import BaseModel
from agents.approve_agent import ApproveAgent
from agents.edd_agent import EddAgent
from agents.compliance_agent import ComplianceAgent
from services.review_store import get_review, remove_review
from fastapi import APIRouter
from events.event_manager import event_manager

approve_agent = ApproveAgent()
edd_agent = EddAgent()
compliance_agent = ComplianceAgent()

router = APIRouter()


class ReviewRequest(BaseModel):

    case_id: str

    action: str


@router.post("/review-action")
async def review_action(request: ReviewRequest):
    state = get_review(request.case_id)

    if not state:

        return {"error": "Case not found"}

    if request.action == "APPROVE":

        state["final_decision"] = "APPROVED"

    elif request.action == "REJECT":

        state["final_decision"] = "REJECTED"

    elif request.action == "ESCALATE":

        state["final_decision"] = "ESCALATED"
    
    await event_manager.broadcast({
        "agent": "HUMAN_REVIEW_AGENT",
        "status": "COMPLETED",
        "message": f"Reviewer action: {request.action}",
        "case_id": state["case_id"],
        "risk_score": state["risk_score"],
        "signals": state["active_signals"]
    })

    # await compliance_agent.run(state)
    if state["final_decision"] == "APPROVED":
        state = await approve_agent.run(state)
    elif state["final_decision"] == "ESCALATED":
        state = await edd_agent.run(state)
    
    await compliance_agent.run(state)

    remove_review(request.case_id)

    return {"success": True}
