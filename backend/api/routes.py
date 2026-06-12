from fastapi import APIRouter, UploadFile, File 
from graph.workflow import graph 
from state.investigation_state import InvestigationState
from typing import List, Optional
from services.case_store import get_case, save_case
from pydantic import BaseModel
import uuid
import os
import shutil

router = APIRouter() 

async def save_file(file,folder):
    path = os.path.join(folder,file.filename)

    with open(path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)
    
    return path

@router.post("/upload-documents")
async def upload_documents(
    aadhaar_file: UploadFile = File(...),
    pan_file: UploadFile = File(...),

    passport_file: Optional[UploadFile] = File(None),
    license_file: Optional[UploadFile] = File(None),
    salary_slip_file: Optional[UploadFile] = File(None),
    signature_file: Optional[UploadFile] = File(None),

    supporting_documents: Optional[List[UploadFile]]= File(None)
):
    case_id = f"CASE-{uuid.uuid4().hex[:8]}"
    folder = f"uploads/{case_id}"
    os.makedirs(folder,exist_ok=True)
    documents = {
        "aadhaar": await save_file(aadhaar_file,folder),
        "pan": await save_file(pan_file,folder)
    }
    state: InvestigationState = {
        "case_id": case_id,
        "uploaded_docs": list(documents.values()),
        "extracted_data": {},
        "risk_score": 0,
        "active_signals": [],
        "completed_agents": [],
        "event_logs": [],
        "final_decision": "",
        "adverse_media_results": [],
        "adverse_media_score": 0
    }

    save_case(case_id,state)

    return {
        "case_id":case_id,
        "status": "Ready"
    }

class StartInvestigationRequest(BaseModel):
    case_id:str


@router.post("/start-investigation") 
async def start_investigation(request: StartInvestigationRequest): 
    state = get_case(request.case_id)
    print("Case:",request.case_id)
    if not state:
        return {
            "success": False,
            "message": "Case not found"
        }

    final_state = await graph.ainvoke(state)
    return {
        "successs": True,
        "case_id": request.case_id
    }

