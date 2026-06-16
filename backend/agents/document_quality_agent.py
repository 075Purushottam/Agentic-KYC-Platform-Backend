import asyncio 
from agents.base_agent import BaseAgent 
from services.document_quality_analyser import analyze_document_quality
class DocumentQualityAgent(BaseAgent): 

    def __init__(self,agent_name="DOCUMENT_QUALITY_AGENT"): 
        self.agent_name = agent_name
    
    async def run(self, state): 
        await self.emit_event({ "status": "RUNNING", "message": "Checking Document Quality" }) 
        image1 = state["uploaded_docs"][0]
        image2 = state["uploaded_docs"][1]
        aadhaar_result = analyze_document_quality(image1)    
        pan_result     = analyze_document_quality(image2)
        overall_score = (
            aadhaar_result["score"] +
            pan_result["score"]
        ) // 2    
        if overall_score < 50:
            state["active_signals"].append(
                "Poor quality identity documents"
            )

        elif overall_score < 70:
            state["active_signals"].append(
                "Document quality requires review"
            )
        agent_results =             {
                "status": "COMPLETED",
                "message": "Document quality issues detected",
                "risk_score": state["risk_score"],
                "signal": f"Overall Quality {aadhaar_result['status']}",

                "state_snapshot": {
                    "risk_score": state["risk_score"],
                    "active_signals": state["active_signals"]
                },
                "evidence": {
                    "agent": "DOCUMENT_QUALITY_AGENT",
                    "title": "Document Quality Assessment",
                    "details": [f"{k}: {v}" for k,v in aadhaar_result.items()]
                },

                "agent_details": {
                    "agent_name": self.agent_name,
                    "input": [
                        "Aadhaar Image",
                        "PAN Image",
                    ],
                    "checks": [
                        "Resolution",
                        "Blur Detection",
                        "Brigtness",
                        "Contrast",
                        "Document Visibility"
                    ],
                    "finding": aadhaar_result['findings'][:3],
                    "confidence":[f"{overall_score}%"],
                    "risk_impact":[
                        "Low Risk" if overall_score > 80 else "Medium Risk"
                    ]
                }
            }
        state['document_quality_results'] = agent_results
        await self.emit_event(
            agent_results
        )
        return state