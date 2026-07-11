"""
TODO:
Repair parser.

What this file does:
- Extracts repair procedures and warnings from raw documents.

Input:
- Raw text, XML, or PDF-derived content.

Output:
- Normalized repair schema.

Dependencies:
- models.repair_schema

Future implementation steps:
- Detect steps and tool lists
- Extract torque values and safety notes
"""


class RepairParser:
    def parse(self, raw_data: dict) -> dict:
        # Bước 1: tạo biến repair_payload.
        # repair_payload = {}
        # Bước 2: tách steps, tools, torque, warnings.
        # Bước 3: return dữ liệu chuẩn hoá.
        return {}
