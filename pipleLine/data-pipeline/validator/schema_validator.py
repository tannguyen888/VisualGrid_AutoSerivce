"""
TODO:
Schema validator.

What this file does:
- Validates transformed records before they are persisted.

Input:
- Normalized record payloads.

Output:
- Validation result or exception.

Dependencies:
- pydantic or custom schema definitions

Future implementation steps:
- Add per-entity validation rules
- Add error reporting details
"""


class SchemaValidator:
    def validate(self, payload: dict) -> bool:
        # Bước 1: tạo biến validation_errors.
        # validation_errors = []
        # Bước 2: kiểm tra từng field bắt buộc.
        # Bước 3: return True/False theo kết quả.
        return True
