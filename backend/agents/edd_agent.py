import asyncio 
from agents.base_agent import BaseAgent 

class EddAgent(BaseAgent):
    def __init__(self,agent_name="EDD_AGENT"): 
        self.agent_name = agent_name

    async def run(self, state):

        await self.emit_event({
            "status": "RUNNING",
            "message": "Enhanced due diligence started"
        })

        state["final_decision"] = "EDD_REQUIRED"

        await self.emit_event({
            "status": "COMPLETED",
            "message": "EDD investigation initiated"
        })

        return state