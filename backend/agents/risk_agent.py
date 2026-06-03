import asyncio
from agents.base_agent import BaseAgent


class RiskAgent(BaseAgent):

    def __init__(self, agent_name="RISK_AGENT"):
        self.agent_name = agent_name

    async def run(self, state):
        await self.emit_event(
            {"status": "RUNNING", "message": "Calculating final risk score"}
        )

        await asyncio.sleep(2)

        if state["risk_score"] < 20:
            decision = "APPROVE"
        elif state["risk_score"] < 50:
            decision = "HUMAN_REVIEW"
        else:
            decision = "EDD_REVIEW"

        state["final_decision"] = decision

        state["completed_agents"].append(self.agent_name)

        await self.emit_event(
            {
                "status": "COMPLETED",
                "message": "Risk analysis completed",
                "route": decision,
                "final_decision": decision,
                "state_snapshot": {
                    "risk_score": state["risk_score"],
                    "active_signals": state["active_signals"],
                    "final_decision": decision
                },
                "evidence": {
                    "agent": "RISK_AGENT",
                    "title": "Risk Assessment",
                    "details": [
                        f"Final Risk Score: {state['risk_score']}",
                        f"Active Signals: {', '.join(state['active_signals'])}",
                        f"Final Decision: {decision}"
                    ]
                },

                "agent_details": {
                    "agent_name": self.agent_name,
                    # "description": "Aggregates all risk factors and signals to calculate a final risk score and decision.",
                    # "capabilities": [
                    #     "Aggregate risk scores from multiple agents",
                    #     "Apply decision rules based on risk thresholds",
                    #     "Provide final compliance decision"
                    # ],
                    "input": [
                        "Risk Score",
                        "Active Signals"
                    ],
                    "check": ["Final Risk Assessment"],
                    "finding": ["Final Decision"],
                    "confidence": ["N/A"],
                    "risk_impact": ["N/A"]
                }
            }
        )

        return state
