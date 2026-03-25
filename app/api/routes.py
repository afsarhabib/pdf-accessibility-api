from fastapi import APIRouter
from app.models.request_models import ScanRequest
from app.models.response_models import ScanResponse
from app.services.scanner_service import scan_files
from app.services.report_service import generate_report

router = APIRouter(prefix="/api/v1")


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/scan", response_model=ScanResponse)
def scan(request: ScanRequest):
    results = scan_files(request.fileUrls)
    return {"files": results}


@router.get("/dashboard")
def dashboard():
    return generate_report()


@router.post("/remediate")
def remediate(request: ScanRequest):
    return {
        "status": "success",
        "remediatedFiles": request.fileUrls
    }