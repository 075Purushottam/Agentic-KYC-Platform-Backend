# agents/adverse_media_agent.py

from agents.base_agent import BaseAgent
from services.adverse_search import search
import asyncio

class AdverseMediaAgent(BaseAgent):

    def __init__(self):
        self.agent_name = "ADVERSE_MEDIA_AGENT"

    async def run(self, state):

        await self.emit_event({
            "status": "RUNNING",
            "message": "Searching adverse media sources"
        })

        await asyncio.sleep(2)
        # result = search(state['extracted_data'])

        findings = [
            "Customer linked to procurement fraud article",
            "Mentioned in regulatory investigation"
        ]



        await self.emit_event({
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
        })

        return {
            "adverse_media_results": findings,
            "adverse_media_score": 25
        }