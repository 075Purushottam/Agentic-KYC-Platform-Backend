import asyncio
from agents.base_agent import BaseAgent


class ComplianceAgent(BaseAgent):
    def __init__(self, agent_name="COMPLIANCE_AGENT"):
        self.agent_name = agent_name

    async def run(self, state):
        await self.emit_event(
            {"status": "RUNNING", "message": "Generating compliance explanation"}
        )

        await asyncio.sleep(2)

        explanation = f""" Customer marked as: {state["final_decision"]} Reason: AML suspicious entity detected. """
        state["completed_agents"].append(self.agent_name)
        await self.emit_event(
            {
                "status": "COMPLETED",
                "message": explanation,
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
                    # "description": "Provides a human-readable explanation of the compliance decision based on the analysis results.",
                    # "capabilities": [
                    #     "Generate clear explanations for compliance decisions",
                    #     "Summarize key risk factors and signals",
                    #     "Support for regulatory reporting requirements"
                    # ],
                    "input": ["Final Decision", "Risk Score", "Active Signals"],
                    "check": ["Compliance Explanation"],
                    "finding": ["N/A"],
                    "confidence": ["N/A"],
                },
            }
        )
        return state
