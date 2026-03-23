from fastapi import APIRouter
from app.models.request_models import ScanRequest
from app.models.response_models import ScanResponse
from app.services.scanner_service import scan_files
from app.services.report_service import generate_report

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/scan", response_model=ScanResponse)
def scan(request: ScanRequest):
    return scan_files(request.files)

@router.get("/report")
def report():
    return generate_report()