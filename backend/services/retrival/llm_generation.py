import os
from groq import AsyncGroq
from core.config import Settings

API_KEY = Settings.LLM_API_KEY

class LLMService():
    def __init__(self):
        self.client = AsyncGroq(api_key=API_KEY)

    async def groq_stream_generator(self,user_query):
        stream = await self.client.chat.completions.create(model="llama-3.3-70b-versatile",
                                                           messages=[{"role": "user", "content": user_query}],
                                                           stream=True
                                                           )

        stream = await self.client.chat.completions.create()
        
        async for chunk in stream:
            # Groq chunks follow the OpenAI-compatible structure
            content = chunk.choices[0].delta.content
            if content:
                # Yield as plain text or SSE format
                yield content





"""
How to implement streaming in fastapi

media type- text/event-stream
use try...except blocks

import os
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from groq import AsyncGroq

app = FastAPI()

# Initialize the async client with your API key
client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY"))



@app.get("/stream-groq")
async def stream_groq(prompt: str = "Explain quantum physics in 2 sentences"):
    return StreamingResponse(groq_stream_generator(prompt), media_type="text/plain")
"""