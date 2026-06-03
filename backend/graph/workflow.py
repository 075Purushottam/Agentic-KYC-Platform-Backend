from langgraph.graph import StateGraph, END 
from state.investigation_state import InvestigationState 
from agents.planner_agent import PlannerAgent 
from agents.ocr_agent import OCRAgent 
from agents.aml_agent import AMLAgent 
from agents.risk_agent import RiskAgent 
from agents.compliance_agent import ComplianceAgent 
from agents.approve_agent import ApproveAgent
from agents.edd_agent import EddAgent
from agents.human_review_agent import HumanReviewAgent

planner_agent = PlannerAgent() 
ocr_agent = OCRAgent() 
aml_agent = AMLAgent() 
risk_agent = RiskAgent() 
compliance_agent = ComplianceAgent() 
approve_agent = ApproveAgent()
edd_agent = EddAgent()
human_review_agent = HumanReviewAgent()

def route_after_risk(state):
  
    score = state["risk_score"]
    print("Score in route risk",score)
    if score < 20:
        return "APPROVE"

    elif score < 50:
        return "HUMAN_REVIEW"

    return "EDD_REVIEW"

workflow = StateGraph(InvestigationState) 

workflow.add_node( "planner_agent", planner_agent.run ) 
workflow.add_node( "ocr_agent", ocr_agent.run ) 
workflow.add_node( "aml_agent", aml_agent.run ) 
workflow.add_node( "risk_agent", risk_agent.run ) 
workflow.add_node( "compliance_agent", compliance_agent.run ) 
workflow.add_node("approve_agent", approve_agent.run)
workflow.add_node("edd_agent", edd_agent.run)
workflow.add_node("human_review_agent", human_review_agent.run)

workflow.set_entry_point("planner_agent") 

workflow.add_edge( "planner_agent", "ocr_agent" ) 
workflow.add_edge( "ocr_agent", "aml_agent" ) 
workflow.add_edge( "aml_agent", "risk_agent" ) 
workflow.add_edge( "risk_agent", "human_review_agent" ) 
# workflow.add_conditional_edges( "risk_agent", route_after_risk, {
#     "APPROVE": "approve_agent",
#     "HUMAN_REVIEW": "human_review_agent",
#     "EDD_REVIEW": "edd_agent"
# })
# workflow.add_edge( "human_review_agent", "approve_agent" ) 
# workflow.add_edge( "human_review_agent", "edd_agent" ) 
# workflow.add_edge( "approve_agent", "compliance_agent" ) 
# workflow.add_edge( "edd_agent", "compliance_agent" ) 
# workflow.add_edge( "approve_agent", "compliance_agent" ) 
# workflow.add_edge( "human_review_agent", "compliance_agent" ) 
# workflow.add_edge( "edd_agent", "compliance_agent" ) 

# workflow.add_edge( "compliance_agent", END ) 

graph = workflow.compile()