from pathlib import Path
from reportlab.platypus import (
SimpleDocTemplate,
Paragraph,
Spacer,
PageBreak
)
from services.case_store import report_store
from reportlab.lib.styles import getSampleStyleSheet

def build_report_data(state):
    report = {

    "case_id": state["case_id"],

    "generated_at": "...",

    "executive_summary": {

        "risk_level": "LOW",

        "final_decision": "APPROVED",

        "top_findings": state["active_signals"],

        "recommendation":
            "Customer approved for onboarding"

    },

    "customer_profile": state['extracted_data'],

    "document_verification": state['document_quality_results'],

    "aml_screening": {

        "watchlists_checked": [],

        "matches_found": 0,

        "risk": "LOW"

    },

    "adverse_media": {

        "articles_reviewed": 45,

        "relevant_hits": 2,

        "risk": "LOW"

    },

    "risk_assessment": {

        "score": 28,

        "breakdown": {

            "document_quality": 5,

            "aml": 10,

            "adverse_media": 13

        }

    },

    "human_review": {

        "decision": "APPROVED"

    },

    "compliance_explanation": {

        "reasoning":
            "Customer passed all checks"
    },

    "ai_insights": [

        "...",

        "...",

        "..."

    ]
}
    report_store[state["case_id"]] = report
    return report
    
# services/report_service.py


def generate_pdf_report(report_data: dict):

    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    case_id = report_data["case_id"]

    pdf_path = reports_dir / f"{case_id}.pdf"

    doc = SimpleDocTemplate(str(pdf_path))

    styles = getSampleStyleSheet()

    story = []

    # ==================================================
    # COVER PAGE
    # ==================================================

    story.append(
        Paragraph(
            "KYC Investigation Report",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"Case ID: {case_id}",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"Customer: {report_data['customer_profile'].get('name','N/A')}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Decision: {report_data['executive_summary'].get('final_decision','N/A')}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Risk Level: {report_data['executive_summary'].get('risk_level','N/A')}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 30))

    story.append(
        Paragraph(
            "Executive Snapshot",
            styles["Heading1"]
        )
    )

    story.append(
        Paragraph(
            f"""
            Recommendation:
            {report_data['executive_summary'].get('recommendation','N/A')}
            """,
            styles["Normal"]
        )
    )

    story.append(PageBreak())

    # ==================================================
    # CUSTOMER PROFILE
    # ==================================================

    story.append(
        Paragraph(
            "Customer Profile",
            styles["Heading1"]
        )
    )

    customer = report_data["customer_profile"]

    for key, value in customer.items():

        story.append(
            Paragraph(
                f"<b>{key}</b>: {value}",
                styles["Normal"]
            )
        )

    story.append(Spacer(1, 20))

    # ==================================================
    # DOCUMENT VERIFICATION
    # ==================================================

    doc_section = report_data["document_verification"]

    story.append(
        Paragraph(
            "Document Verification",
            styles["Heading1"]
        )
    )

    story.append(
        Paragraph(
            f"Quality Score: {doc_section.get('quality_score','N/A')}",
            styles["Normal"]
        )
    )

    for finding in doc_section.get("findings", []):

        story.append(
            Paragraph(
                f"• {finding}",
                styles["Normal"]
            )
        )

    story.append(Spacer(1, 20))

    # ==================================================
    # AML SCREENING
    # ==================================================

    aml = report_data["aml_screening"]

    story.append(
        Paragraph(
            "AML Screening",
            styles["Heading1"]
        )
    )

    story.append(
        Paragraph(
            f"Matches Found: {aml.get('matches_found',0)}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Risk: {aml.get('risk','LOW')}",
            styles["Normal"]
        )
    )

    for item in aml.get("watchlists_checked", []):

        story.append(
            Paragraph(
                f"• {item}",
                styles["Normal"]
            )
        )

    story.append(Spacer(1, 20))

    # ==================================================
    # ADVERSE MEDIA
    # ==================================================

    media = report_data["adverse_media"]

    story.append(
        Paragraph(
            "Adverse Media Screening",
            styles["Heading1"]
        )
    )

    story.append(
        Paragraph(
            f"Articles Reviewed: {media.get('articles_reviewed',0)}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Relevant Hits: {media.get('relevant_hits',0)}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Risk Assessment: {media.get('risk','LOW')}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 20))

    # ==================================================
    # RISK ASSESSMENT
    # ==================================================

    risk = report_data["risk_assessment"]

    story.append(
        Paragraph(
            "Risk Assessment",
            styles["Heading1"]
        )
    )

    story.append(
        Paragraph(
            f"Total Risk Score: {risk.get('score',0)}",
            styles["Normal"]
        )
    )

    breakdown = risk.get("breakdown", {})

    for k, v in breakdown.items():

        story.append(
            Paragraph(
                f"{k}: {v}",
                styles["Normal"]
            )
        )

    story.append(Spacer(1, 20))

    # ==================================================
    # HUMAN REVIEW
    # ==================================================

    review = report_data["human_review"]

    story.append(
        Paragraph(
            "Human Review",
            styles["Heading1"]
        )
    )

    story.append(
        Paragraph(
            f"Decision: {review.get('decision','N/A')}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Comments: {review.get('comments','N/A')}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 20))

    # ==================================================
    # COMPLIANCE EXPLANATION
    # ==================================================

    compliance = report_data["compliance_explanation"]

    story.append(
        Paragraph(
            "Compliance Explanation",
            styles["Heading1"]
        )
    )

    story.append(
        Paragraph(
            compliance.get(
                "reasoning",
                "No explanation available"
            ),
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 20))

    # ==================================================
    # AI INSIGHTS
    # ==================================================

    story.append(
        Paragraph(
            "AI Insights",
            styles["Heading1"]
        )
    )

    for insight in report_data.get(
        "ai_insights",
        []
    ):

        story.append(
            Paragraph(
                f"• {insight}",
                styles["Normal"]
            )
        )

    doc.build(story)

    return str(pdf_path)
