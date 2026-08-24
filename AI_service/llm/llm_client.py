"""
Purpose:
- Provide async LLM generation interface for diagnosis and repair guidance.

Input:
- Prompt text and optional generation parameters.

Output:
- Generated assistant text.

Dependencies:
- os
- openai (optional runtime)

Future implementation:
- Add retry, timeout controls, and output schema validation.
"""

from __future__ import annotations

import os


class LLMClient:
    def __init__(self, model: str = "gpt-4o-mini") -> None:
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY", "")

    async def generate(self, prompt: str) -> str:
        if not self.api_key:
            return (
                "Problem: Unable to call external LLM (missing API key).\n"
                "Possible causes:\n- Missing inference provider configuration\n"
                "Recommended steps:\n1. Configure OPENAI_API_KEY\n2. Retry with RAG context\n"
                "Safety warnings:\n- Verify all procedures with official manual before repair"
            )

        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=self.api_key)
        response = await client.responses.create(
            model=self.model,
            input=prompt,
            temperature=0.2,
        )
        return response.output_text or ""
