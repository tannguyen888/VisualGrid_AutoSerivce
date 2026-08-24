"""
Purpose:
- Backward-compatible model exports.

Input:
- Imports from legacy modules.

Output:
- Re-exported request/response models.

Dependencies:
- models.request_model
- models.response_model

Future implementation:
- Remove this compatibility file after full import migration.
"""

from models.request_model import ChatRequest, DiagnosisRequest
from models.response_model import ChatResponse, DiagnosisResponse

__all__ = [
    "DiagnosisRequest",
    "DiagnosisResponse",
    "ChatRequest",
    "ChatResponse",
]
