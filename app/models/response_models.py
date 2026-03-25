from pydantic import BaseModel
from typing import List

class FileScanResult(BaseModel):
    file: str
    score: float
    issues: List[str]

class ScanResponse(BaseModel):
    files: List[FileScanResult]
