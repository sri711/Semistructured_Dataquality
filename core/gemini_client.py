import os
from dotenv import load_dotenv
import httpx
import asyncio
from typing import Optional

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is not set")

BASE_URL = os.getenv("GEMINI_API_URL")
if not BASE_URL:
    raise ValueError("GEMINI_API_URL environment variable is not set")

async def gemini_flash(prompt: str, max_retries: int = 3, timeout: float = 30.0) -> Optional[str]:
    """Make API call to Gemini with retry logic and timeout handling"""
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        for attempt in range(max_retries):
            try:
                payload = {
                    "contents": [{
                        "parts": [{
                            "text": prompt
                        }]
                    }]
                }
                
                response = await client.post(
                    BASE_URL,
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                
                response.raise_for_status()
                return response.json()["candidates"][0]["content"]["parts"][0]["text"]

            except httpx.ReadTimeout:
                if attempt == max_retries - 1:
                    print(f"❌ API request timed out after {max_retries} attempts")
                    raise
                print(f"⚠️ Attempt {attempt + 1} timed out, retrying...")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
                
            except Exception as e:
                print(f"❌ Error making API call: {str(e)}")
                raise

    return None
