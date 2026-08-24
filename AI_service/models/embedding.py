"""
Purpose:
- Backward-compatible embedding/search model exports.

Input:
- Imports from legacy modules.

Output:
- Re-exported SearchResult model.

Dependencies:
- models.response_model

Future implementation:
- Remove this file once all imports use response_model directly.
"""

from models.response_model import SearchResult

__all__ = ["SearchResult"]
