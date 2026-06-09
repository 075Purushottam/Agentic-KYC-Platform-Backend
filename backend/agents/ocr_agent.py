import asyncio 
from agents.base_agent import BaseAgent 
class OCRAgent(BaseAgent): 

    def __init__(self,agent_name="OCR_AGENT"): 
        self.agent_name = agent_name

    async def run(self, state): 
        await self.emit_event({ "status": "RUNNING", "message": "Extracting document data" }) 
        await asyncio.sleep(2) 
        state["extracted_data"] = { "name": "Arjun Malhotra", "passport": "N882712", "country": "India" } 
        state["completed_agents"].append(self.agent_name) 
        await self.emit_event(
            {
                "status": "COMPLETED",
                "message": "Passport data extracted",
                "state_snapshot": {
                    "extracted_data": state["extracted_data"]
                },
                "evidence": {
                "agent": "OCR_AGENT",
                "title": "Passport Extraction",
                "details": [
                    "Name: Arjun Malhotra",
                    "Passport: N882712",
                    "Country: India"
                    ]
                },
                "agent_details": {
                    "agent_name": self.agent_name,
            
                    "input": [
                        "Scanned Passport Image"
                    ],
                    "output": [
                        "Extracted Name",
                        "Extracted Passport Number",
                        "Extracted Country"
                    ],
                    "confidence":[
                        "95%"
                    ],
                    "risk_impact":[
                        "N/A"
                    ]
                }
            }
        )
        return state
