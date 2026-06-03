import asyncio 
from agents.base_agent import BaseAgent 
class OCRAgent(BaseAgent): 

    def __init__(self,agent_name="OCR_AGENT"): 
        self.agent_name = agent_name

    async def run(self, state): 
        await self.emit_event({ "status": "RUNNING", "message": "Extracting document data" }) 
        await asyncio.sleep(2) 
        state["extracted_data"] = { "name": "Arjun Malhotra", "passport": "N882712" } 
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
                    # "description": "Performs OCR on uploaded documents to extract relevant data.",
                    # "capabilities": [
                    #     "Extract text from images",
                    #     "Structured data output",
                    #     "Supports multiple document types"
                    # ],
                    "input": [
                        "Scanned Passport Image"
                    ],
                    "output": [
                        "Extracted Name",
                        "Extracted Passport Number"
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
