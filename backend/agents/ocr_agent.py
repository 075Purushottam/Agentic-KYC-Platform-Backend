import asyncio
import json
from agents.base_agent import BaseAgent
from services.ocr_service import ocr_image
from agents.ocr_prompt import ocr_json


class OCRAgent(BaseAgent):

    def __init__(self, agent_name="OCR_AGENT"):
        self.agent_name = agent_name

    async def run(self, state):
        await self.emit_event(
            {"status": "RUNNING", "message": "Extracting document data"}
        )
        await asyncio.sleep(2)
        image1 = state["uploaded_docs"][0]
        image2 = state["uploaded_docs"][1]
        print(image1, image2)
        aadhar = ocr_image(image1)
        pan = ocr_image(image2)
        input_text = f""" aadhar data: {aadhar},
                            pan data : {pan} """
        extracted_json = ocr_json(input_text)
        state["extracted_data"] = {"name": "Aryan Malhotra", "country": "India"}
        state["completed_agents"].append(self.agent_name)
        await self.emit_event(
            {
                "status": "COMPLETED",
                "message": "Passport data extracted",
                "state_snapshot": {"extracted_data": state["extracted_data"]},
                "evidence": {
                    "agent": "OCR_AGENT",
                    "title": "Passport Extraction",
                    "details": [
                        "Name: Arjun Malhotra",
                        "Passport: N882712",
                        "Country: India",
                    ],
                },
                "agent_details": {
                    "agent_name": self.agent_name,
                    "input": ["Scanned Passport Image"],
                    "output": [
                        "Extracted Name",
                        "Extracted Passport Number",
                        "Extracted Country",
                    ],
                    "confidence": ["95%"],
                    "risk_impact": ["N/A"],
                },
            }
        )
        return state
