import asyncio 
from agents.base_agent import BaseAgent 
from services.review_store import add_review
from langgraph.types import interrupt

class HumanReviewAgent(BaseAgent):
    def __init__(self,agent_name="HUMAN_REVIEW_AGENT"): 
        self.agent_name = agent_name

    async def run(self, state):
        print("human review agent executed") 
        await self.emit_event({
            "agent": "HUMAN_REVIEW_AGENT",
            "status": "WAITING",
            "message": "Awaiting analyst review",
            "case_id": state["case_id"],
            "risk_score": state["risk_score"],
            "signals": state["active_signals"]
        })

        state["final_decision"] = "HUMAN_REVIEW"
        state["human_review_required"] = True
        
        # await self.emit_event({
        #     "status": "COMPLETED",
        #     "message": "Waiting for reviewer",
        # })
        add_review(
            state["case_id"],
            state
        )
        return state