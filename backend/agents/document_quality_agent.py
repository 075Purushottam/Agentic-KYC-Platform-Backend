import asyncio 
from agents.base_agent import BaseAgent 

class DocumentQualityAgent(BaseAgent): 

    def __init__(self,agent_name="DOCUMENT_QUALITY_AGENT"): 
        self.agent_name = agent_name

    async def run(self, state): 
        await self.emit_event({ "status": "RUNNING", "message": "Checking Document Quality" }) 
        await asyncio.sleep(2) 
        await self.emit_event(
            {
                "status": "COMPLETED",
                "message": "Document quality issues detected",
                "risk_score": state["risk_score"],
                "signal": "Linked suspicious entity",

                "state_snapshot": {
                    "risk_score": state["risk_score"],
                    "active_signals": state["active_signals"]
                },
                "evidence": {
                    "agent": "DOCUMENT_QUALITY_AGENT",
                    "title": "Document Quality Assessment",
                    "details": [
                        "Potential watchlist match",
                        "Confidence 91%",
                        "Risk Impact: +25%"
                    ]
                },

                "agent_details": {
                    "agent_name": self.agent_name,
                    "input": [
                        "Passport Data",
                        "Pancard Data",
                    ],
                    "checks": [
                        "Check for potential matches against watchlists and databases",
                        "Evaluate the quality and reliability of the documents provided"
                    ],
                    "finding": [
                        "Potential match found for a known suspicious entity in the watchlist database"
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