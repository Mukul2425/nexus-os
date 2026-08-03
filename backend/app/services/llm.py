
from google import genai
from app.core.config import Settings

client = genai.Client(api_key=Settings().GEMINI_API_KEY)


def generate_response(message: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=message,

    )
    return response.text
    """
    PlaceHoldeer function for LLM response.

    Later this function will be replaced with actual LLM response generation logic.
    and will call OpenAI, Gemini, Claude any other LLM API to generate response based on the prompt.
    
   """