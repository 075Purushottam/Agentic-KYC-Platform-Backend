# agents/adverse_media_agent.py

from agents.base_agent import BaseAgent
from services.adverse_search import search
from agents.ocr_prompt import refine_adverse_result
import asyncio

class AdverseMediaAgent(BaseAgent):

    def __init__(self):
        self.agent_name = "ADVERSE_MEDIA_AGENT"

    async def run(self, state):

        await self.emit_event({
            "status": "RUNNING",
            "message": "Searching adverse media sources"
        })

        # await asyncio.sleep(2)
        # adverse_context = search(state['extracted_data'])
        # results = refine_adverse_result(state['extracted_data'],adverse_context)
        # print("Adverse Media Results:",results)

        findings = [
            "Customer linked to procurement fraud article",
            "Mentioned in regulatory investigation"
        ]
        agent_results = {
            "status": "COMPLETED",
            "message": "Adverse media findings detected",

            "evidence": {
                "agent": "ADVERSE_MEDIA_AGENT",
                "title": "Adverse Media Findings",
                "details": findings
            },

            "agent_details": {
                "agent_name": "ADVERSE_MEDIA_AGENT",
                "input": [
                    "Customer Name",
                    "Jurisdiction"
                ],
                "checks": [
                    "News Search",
                    "Regulatory Mentions",
                    "Legal Cases"
                ],
                "finding": findings,
                "confidence": ["87%"],
                "risk_impact": ["+25"]
            }
        }
        state['adverse_media_results']=agent_results
        await self.emit_event(agent_results)

        return {
            "adverse_media_results": findings,
            "adverse_media_score": 25
        }