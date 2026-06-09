from agents.base_agent import BaseAgent

class RejectAgent(BaseAgent):
    def __init__(self,agent_name="REJECT_AGENT"): 
        self.agent_name = agent_name

    async def run(self, state):

        await self.emit_event({
            "status": "RUNNING",
            "message": "Rejecting customer"
        })

        state["final_decision"] = "REJECTED"

        await self.emit_event({
            "status": "COMPLETED",
            "message": "Customer rejected"
        })

        return state    