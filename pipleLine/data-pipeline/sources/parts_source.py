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
        # TODO: query the parts provider and return raw payload.
        return {}
