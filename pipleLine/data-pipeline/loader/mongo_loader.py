"""
TODO:
MongoDB loader.

What this file does:
- Stores documents, manuals, and knowledge payloads.

Input:
- Validated or enriched document payload.

Output:
- Stored MongoDB documents.

Dependencies:
- pymongo

Future implementation steps:
- Add collection routing
- Add version tracking
"""


class MongoLoader:
    def save(self, payload: dict) -> None:
        # Bước 1: tạo biến collection/document.
        # collection = None
        # document = payload
        # Bước 2: lưu document vào MongoDB.
        # Bước 3: trả trạng thái hoặc id nếu cần.
        pass
