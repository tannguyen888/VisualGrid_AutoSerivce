"""
TODO:
Repair mapper.

What this file does:
- Converts parsed repair data into database-ready records.

Input:
- Parsed repair schema.

Output:
- Storage-friendly repair record.

Dependencies:
- models.repair_schema

Future implementation steps:
- Normalize steps and warnings
- Prepare loader payloads
"""



class RepairMapper:
    def map(self, repair_data: dict) -> dict:
        # Bước 1: tạo biến mapped_repair.
        # mapped_repair = {}
        # Bước 2: map các bước sửa, torque, safety notes.
        # Bước 3: trả dữ liệu sẵn sàng lưu.
        return {}
