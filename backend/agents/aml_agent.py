import asyncio 
from agents.base_agent import BaseAgent 
from services.aml_matcher import AMLScreeningEngine
class AMLAgent(BaseAgent): 

    def __init__(self,agent_name="AML_AGENT"): 
        self.agent_name = agent_name

    async def run(self, state): 
        await self.emit_event({ "status": "RUNNING", "message": "Running AML screening" }) 
        # await asyncio.sleep(2) 
        ofac = r"C:\Users\Tirupati\Desktop\agentic-kyc-platform\Agentic-KYC-Platform-Backend\backend\uploads\clean_ofac.json"
        pep = r"C:\Users\Tirupati\Desktop\agentic-kyc-platform\Agentic-KYC-Platform-Backend\backend\uploads\clean_pep.json"
        engine = AMLScreeningEngine(
            ofac,pep
        )
        result = engine.run(state['extracted_data'])
        agent_results =             {
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
        state['aml_results']=agent_results
        await self.emit_event(
            agent_results
        )
        return {
            "active_signals": state["active_signals"] + ["Linked suspicious entity"],
            "risk_score": state["risk_score"] + 5,
            "completed_agents": state["completed_agents"] + [self.agent_name]
        }
