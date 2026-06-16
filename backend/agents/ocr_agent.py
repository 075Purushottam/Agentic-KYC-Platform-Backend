import asyncio
import json
from agents.base_agent import BaseAgent
# from services.ocr_service import ocr_image
from agents.ocr_prompt import ocr_json
from services.easy_try import extract_text_from_image


class OCRAgent(BaseAgent):

    def __init__(self, agent_name="OCR_AGENT"):
        self.agent_name = agent_name

    async def run(self, state):
        await self.emit_event(
            {"status": "RUNNING", "message": "Extracting document data"}
        )
        # await asyncio.sleep(2)
        image1 = state["uploaded_docs"][0]
        image2 = state["uploaded_docs"][1]
        print("UPLOAD DOCS PATH:",image1, image2)
        aadhar = extract_text_from_image(image1)
        pan    = extract_text_from_image(image2)
        input_text = f""" ADHAAR DATA: {aadhar},
                            PAN DATA : {pan} """
        extracted_json = ocr_json(input_text)
        state["extracted_data"] = extracted_json
        details = [f"{k.upper()}: {v}" for k,v in extracted_json.items()]
        state["completed_agents"].append(self.agent_name)
        agent_results =             {
                "status": "COMPLETED",
                "message": "Passport data extracted",
                "state_snapshot": {"extracted_data": state["extracted_data"]},
                "evidence": {
                    "agent": "OCR_AGENT",
                    "title": "AADHAAR PAN Extraction",
                    "details": details,
                },
                "agent_details": {
                    "agent_name": self.agent_name,
                    "input": ["Scanned ADHAAR Image","Scanned PAN Image"],
                    "output": [
                        f"Extracted Name {extracted_json['name']}",
                        f"Extracted AADHAAR Number {extracted_json['aadhaar_no']}",
                        f"Extracted PAN Number {extracted_json['pan_no']}",
                        f"Extracted Country {extracted_json['country']}",
                    ],
                    "confidence": ["95%"],
                    "risk_impact": ["N/A"],
                },
            }
        state['ocr_results']=agent_results 
        await self.emit_event(
            agent_results
        )
        return state
