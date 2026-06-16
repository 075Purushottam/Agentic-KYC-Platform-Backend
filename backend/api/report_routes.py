from fastapi import APIRouter
from fastapi.responses import FileResponse
from services.report_service import generate_pdf_report
from services.case_store import report_store
router = APIRouter()

@router.get("/report/{case_id}/preview")
async def preview_report(case_id: str):
    print(f"preview for case id:{case_id}")
    return report_store.get(case_id)

@router.get("/report/{case_id}")
async def download_report(case_id: str):
    print(f"download for case id:{case_id}")
    report = report_store.get(case_id)
    if not report:
        return {
            "error": "Report not found"
        }
    pdf_path = generate_pdf_report(report)

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"KYC_Investigation_Report {case_id}.pdf"
    )
