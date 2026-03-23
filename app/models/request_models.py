from pydantic import BaseModel
from typing import List

class ScanRequest(BaseModel):
    files: List[str]