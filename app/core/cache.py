import time
from typing import Dict, Tuple

# Cache dictionary: key -> (timestamp, answer)
cache: Dict[Tuple[str, str], Tuple[float, str]] = {}
CACHE_EXPIRY = 300  # 5 minutes in seconds


def get_cached_answer(pdf_text: str, question: str):
    key = (pdf_text, question)
    if key in cache:
        timestamp, answer = cache[key]
        if time.time() - timestamp < CACHE_EXPIRY:
            return answer
        else:
            del cache[key]  # Remove expired cache
    return None


def set_cache(pdf_text: str, question: str, answer: str):
    key = (pdf_text, question)
    cache[key] = (time.time(), answer)
