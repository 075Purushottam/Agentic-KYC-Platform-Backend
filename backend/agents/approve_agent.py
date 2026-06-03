import asyncio 
from agents.base_agent import BaseAgent 

class ApproveAgent(BaseAgent):
    def __init__(self,agent_name="APPROVE_AGENT"): 
        self.agent_name = agent_name

    async def run(self, state):

        await self.emit_event({
            "status": "RUNNING",
            "message": "Approving customer"
        })

        state["final_decision"] = "APPROVED"

        await self.emit_event({
            "status": "COMPLETED",
            "message": "Customer approved"
        })

        return state