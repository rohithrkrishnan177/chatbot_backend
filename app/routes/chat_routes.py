from fastapi.responses import StreamingResponse
from fastapi import APIRouter, File, Form, UploadFile, Depends, HTTPException
from app.helpers.validate import validate_pdf
from app.routes.auth_routes import get_current_user
from app.services.pdf_service import extract_text_from_pdf
from app.services.llm_service import stream_llm_response
from app.core.cache import get_cached_answer, set_cache
import asyncio

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/stream")
async def chat_with_pdf_stream(
    file: UploadFile = File(...),
    question: str = Form(...),
    current_user=Depends(get_current_user),
):
    # 1. Validate PDF
    validate_pdf(file)

    # 2. Extract text
    pdf_text = extract_text_from_pdf(file.file)
    if not pdf_text.strip():
        raise HTTPException(status_code=400, detail="Uploaded PDF is empty.")

    # 3. Check cache
    cached_answer = get_cached_answer(pdf_text, question)
    if cached_answer:
        async def cached_gen():
            yield cached_answer
        return StreamingResponse(cached_gen(), media_type="text/plain")

    # 4. Create prompt
    prompt = f"PDF Content:\n{pdf_text}\n\nUser Question: {question}"

    # 5. Stream response from LLM
    async def event_generator():
        full_answer = ""  # accumulate chunks for caching
        async for chunk in stream_llm_response(prompt):
            full_answer += chunk
            yield chunk  # stream chunk to client
            await asyncio.sleep(0)  # allow event loop to process
        # 6. Store full response in cache
        set_cache(pdf_text, question, full_answer)

    return StreamingResponse(event_generator(), media_type="text/plain")
