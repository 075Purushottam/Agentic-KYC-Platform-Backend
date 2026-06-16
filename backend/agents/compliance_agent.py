import asyncio
from agents.base_agent import BaseAgent
from services.report_service import build_report_data

class ComplianceAgent(BaseAgent):
    def __init__(self, agent_name="COMPLIANCE_AGENT"):
        self.agent_name = agent_name

    async def run(self, state):
        await self.emit_event(
            {"status": "RUNNING", "message": "Generating compliance explanation"}
        )

        # await asyncio.sleep(2)

        explanation = f""" Customer marked as: {state["final_decision"]} Reason: AML suspicious entity detected. """
        state["completed_agents"].append(self.agent_name)
        agent_results =             {
                "status": "COMPLETED",
                "message": explanation,
                "phase": "DONE",
                "state_snapshot": {
                    "final_decision": state["final_decision"],
                    "risk_score": state["risk_score"],
                    "active_signals": state["active_signals"],
                },
                "evidence": {
                    "agent": "COMPLIANCE_AGENT",
                    "title": "Compliance Explanation",
                    "details": [
                        f"Final Decision: {state['final_decision']}",
                        f"Risk Score: {state['risk_score']}",
                        f"Active Signals: {', '.join(state['active_signals'])}",
                    ],
                },
                "agent_details": {
                    "agent_name": self.agent_name,
                    "input": ["Final Decision", "Risk Score", "Active Signals"],
                    "check": ["Compliance Explanation"],
                    "finding": ["N/A"],
                    "confidence": ["N/A"],
                },
            }
        state['compliance_results']=agent_results
        report = build_report_data(state)
        
        state['investigation_report'] = report
        await self.emit_event(
            agent_results
        )
        await self.emit_event({

            "status": "REPORT_READY",

            "case_id": state["case_id"],

            "report": report

        })
        return state
