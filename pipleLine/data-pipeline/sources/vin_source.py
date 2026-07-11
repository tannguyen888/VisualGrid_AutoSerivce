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
        # TODO: call VIN provider and return raw response.
        return {}
