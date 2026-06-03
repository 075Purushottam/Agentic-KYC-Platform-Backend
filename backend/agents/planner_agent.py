from agents.base_agent import BaseAgent 
class PlannerAgent(BaseAgent): 
    
    def __init__(self,agent_name="PLANNER_AGENT"): 
        self.agent_name = agent_name

    async def run(self, state): 
        await self.emit_event({ "status": "RUNNING", "message": "Planning investigation workflow" }) 
        state["completed_agents"].append(self.agent_name) 
        await self.emit_event({ "status": "COMPLETED", "message": "Workflow initialized" }) 
        return state