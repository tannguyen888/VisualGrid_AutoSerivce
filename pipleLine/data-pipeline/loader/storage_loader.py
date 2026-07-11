"""
TODO:
Storage loader.

What this file does:
- Stores files or raw artifacts in long-term storage.

Input:
- Binary file or artifact payload.

Output:
- Stored artifact reference.

Dependencies:
- local filesystem, S3, or blob storage client

Future implementation steps:
- Add storage abstraction
- Add checksum verification
"""


class StorageLoader:
    def save(self, payload: bytes) -> str:
        # Bước 1: tạo biến storage_path hoặc file_key.
        # storage_key = ""
        # artifact_bytes = payload
        # Bước 2: ghi file hoặc upload blob.
        # Bước 3: return đường dẫn/reference đã lưu.
        return ""
