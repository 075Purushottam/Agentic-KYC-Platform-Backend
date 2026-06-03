import asyncio 
from agents.base_agent import BaseAgent 

class AMLAgent(BaseAgent): 

    def __init__(self,agent_name="AML_AGENT"): 
        self.agent_name = agent_name

    async def run(self, state): 
        await self.emit_event({ "status": "RUNNING", "message": "Running AML screening" }) 
        await asyncio.sleep(2) 
        state["active_signals"].append( "Linked suspicious entity" ) 
        state["risk_score"] += 5 
        state["completed_agents"].append(self.agent_name) 
        await self.emit_event(
            {
                "status": "COMPLETED",
                "message": "AML risk detected",
                "risk_score": state["risk_score"],
                "signal": "Linked suspicious entity",

                "state_snapshot": {
                    "risk_score": state["risk_score"],
                    "active_signals": state["active_signals"]
                },
                "evidence": {
                    "agent": "AML_AGENT",
                    "title": "AML Screening Result",
                    "details": [
                        "Potential watchlist match",
                        "Confidence 91%",
                        "Risk Impact: +25%"
                    ]
                },

                "agent_details": {
                    "agent_name": self.agent_name,
                    # "description": "Performs AML screening against watchlists and PEP databases.",
                    # "capabilities": [
                    #     "Screening against global watchlists",
                    #     "PEP (Politically Exposed Persons) detection",
                    #     "Adverse media monitoring"
                    # ],
                    "input": [
                        "Paassport Data",
                        "Customer Identity"
                    ],
                    "checks": [
                        "Watchlist Screening",
                        "Entity Resolution",
                        "Jurisdiction Screening"
                    ],
                    "finding": [
                        "Potential Match Found"
                    ],
                    "confidence":[
                        "91%"
                    ],
                    "risk_impact":[
                        "+25%"
                    ]

                }
            }
        )
        return state
