Agentic KYC Platform - Backend

Backend services for the Agentic KYC Platform built using FastAPI, LangGraph, and AI agents.

Features

- Document upload (Aadhaar, PAN, Passport, License, etc.)
- OCR-based data extraction
- AML screening
- Adverse Media Screening
- Risk Assessment
- Human-in-the-Loop Review
- Compliance Decision Generation
- Real-time WebSocket event streaming
- LangGraph-powered agent orchestration

Agent Workflow

Document Quality Agent → OCR Agent → AML Agent + Adverse Media Agent → Risk Agent → Human Review Agent → Approve / EDD Agent → Compliance Agent

Tech Stack

- FastAPI
- LangGraph
- Python
- WebSockets
- PaddleOCR
- ChromaDB
- Sentence Transformers

Setup

Clone Repository

git clone https://github.com/075Purushottam/Agentic-KYC-Platform-Backend.git

cd Agentic-KYC-Platform-Backend

Create Virtual Environment

python -m venv venv

venv\Scripts\activate

Install Dependencies

pip install -r requirements.txt

Run Application

uvicorn main:app --reload

Backend will start at:

http://localhost:8000

Swagger API Docs:

http://localhost:8000/docs

Frontend Integration

This backend is designed to work with the frontend application:

Frontend Repository:

https://github.com/075Purushottam/Lovable_Agentic_KYC

Ensure the frontend environment variable points to this backend:

VITE_BACKEND_URL=http://localhost:8000

Main APIs

POST /upload-documents

POST /start-investigation

POST /review-action

WS /ws

Demo Flow

1. Upload Aadhaar and PAN documents
2. Start investigation
3. Monitor agent execution in real time
4. Review analyst decision (Approve / Escalate)
5. Generate final compliance outcome

License

MIT
