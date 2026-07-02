from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.providers.groq import GroqProvider

from core.config import Settings

groq_api_key = Settings.GROQ_API_KEY


custom_model = GroqModel(model_name='llama-3.3-70b-versatile', provider=GroqProvider(api_key=groq_api_key))

agent = Agent(custom_model, instructions='Be concise, reply with one sentence.')