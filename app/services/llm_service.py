import httpx
from fastapi import HTTPException
import asyncio
from app.core.config import settings


async def ask_llm_full(prompt: str) -> str:
    """
    Call LLM API and return full response as a string.
    """
    headers = {"Authorization": f"Bearer {settings.LLM_API_KEY}"}
    payload = {
        "model": "mistral-tiny",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 300,
    }

    async with httpx.AsyncClient(timeout=30) as client:
        try:
            resp = await client.post(settings.LLM_API_URL, headers=headers, json=payload)
            resp.raise_for_status()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"LLM request failed: {str(e)}")

        data = resp.json()
        return data.get("choices", [{}])[0].get("message", {}).get("content", "")


async def stream_llm_response(prompt: str, chunk_size: int = 50):
    """
    Simulate streaming by splitting full LLM response into chunks.
    """
    full_answer = await ask_llm_full(prompt)

    # Yield the answer in chunks
    for i in range(0, len(full_answer), chunk_size):
        yield full_answer[i:i + chunk_size]
        await asyncio.sleep(0.1)  # small delay to simulate streaming
