"""
TODO:
Parts provider connector.

What this file does:
- Pulls OEM number, part fitment, and assembly relationships.

Input:
- Query parameters, SKU, OEM number, or vehicle context.

Output:
- Raw provider response as dict.

Dependencies:
- requests

Future implementation steps:
- Support pagination
- Add provider mapping
- Cache lookups where needed
"""


class PartsSource:
    def fetch(self, query: str) -> dict:
        # Bước 1: tạo biến query request cho parts provider.
        # base_url = ""
        # headers = {}
        # payload = {"query": query}
        # response = None
        # Bước 2: gọi provider và nhận raw payload.
        # Bước 3: trả dữ liệu thô cho parser.
        return {}
