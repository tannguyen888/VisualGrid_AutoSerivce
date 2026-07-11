"""
TODO:
VIN source connector.

What this file does:
- Fetches raw vehicle details from an external VIN provider.

Input:
- VIN string.

Output:
- Raw JSON/dict from provider.

Dependencies:
- requests

Future implementation steps:
- Add authentication
- Add timeout/retry handling
- Normalize response shape
"""


class VinSource:
    def fetch(self, vin: str) -> dict:
        # Bước 1: tạo biến request cho VIN provider.
        # base_url = ""
        # headers = {}
        # params = {"vin": vin}
        # response = None
        # Bước 2: gọi API lấy dữ liệu thô.
        # Bước 3: trả về dict JSON chưa xử lý.
        return {}
