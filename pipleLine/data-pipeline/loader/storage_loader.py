"""
Purpose:
- Object storage loader for binary artifacts such as PDFs and diagrams.

Input:
- Binary payload and artifact name.

Output:
- Stored artifact path reference.

Responsibilities:
- Persist binary assets to storage backend.
- Return stable reference path for database linking.

TODO implementation notes:
- Add S3/GCS/Azure blob providers.
- Add checksum metadata persistence.
"""

from __future__ import annotations

from pathlib import Path

from config import settings


class StorageLoader:
    def __init__(self, root_path: str | None = None) -> None:
        self.root_path = Path(root_path or settings.object_storage_root)
        self.root_path.mkdir(parents=True, exist_ok=True)

    def save(self, artifact_name: str, payload: bytes) -> str:
        safe_name = artifact_name.replace("/", "_").replace("\\", "_")
        artifact_path = self.root_path / safe_name
        artifact_path.write_bytes(payload)
        return str(artifact_path)
