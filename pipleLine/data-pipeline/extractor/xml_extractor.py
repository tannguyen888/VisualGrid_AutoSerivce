"""
Purpose:
- XML extractor for automotive catalog and export payloads.

Input:
- XML payload as string or bytes.

Output:
- Nested dictionary representation.

Responsibilities:
- Parse XML safely.
- Convert nodes recursively into serializable structures.

TODO implementation notes:
- Add namespace-aware mapping profiles.
- Add large-file streaming parser mode.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import Any


def _node_to_dict(node: ET.Element) -> dict[str, Any]:
    children = list(node)
    payload: dict[str, Any] = {"tag": node.tag, "attributes": dict(node.attrib)}
    text = (node.text or "").strip()
    if text:
        payload["text"] = text
    if children:
        payload["children"] = [_node_to_dict(child) for child in children]
    return payload


class XmlExtractor:
    def extract(self, xml_text: str | bytes) -> dict[str, Any]:
        if isinstance(xml_text, bytes):
            xml_text = xml_text.decode("utf-8", errors="replace")
        root = ET.fromstring(xml_text)
        return _node_to_dict(root)
