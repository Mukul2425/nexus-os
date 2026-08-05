
from google import genai
from app.core.config import Settings
from app.schemas.chat import ChatRequest, ChatResponse, ChatMessage


client = genai.Client(api_key=Settings().GEMINI_API_KEY)


def generate_response(messages: list[ChatMessage]) -> str:
    conversation = []

    for message in messages:
        conversation.append(
            {"role": message.role,
            "parts": [{"text": message.content}]
            }
            )


    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=conversation,
    )
    return response.text
    """
    PlaceHoldeer function for LLM response.

    Later this function will be replaced with actual LLM response generation logic.
    and will call OpenAI, Gemini, Claude any other LLM API to generate response based on the prompt.
    
   """