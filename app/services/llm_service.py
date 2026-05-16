import httpx

from app.core.config import settings

# Сервис для взаимодействия с LLM
class LLMService:
    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    # Генерация ответа на основе вопроса и контекста
    @staticmethod
    async def generate_answer(query: str, context: str) -> str:

        prompt = f"""
You are a helpful AI assistant.

Answer the question ONLY using the provided context.

If the answer is not in the context, say:
"I could not find the answer in the documents."

Context:
{context}

Question:
{query}
"""

        headers = {
            "Authorization":
                f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": settings.OPENROUTER_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        }

        async with httpx.AsyncClient() as client:

            response = await client.post(
                LLMService.BASE_URL,
                headers=headers,
                json=payload,
                timeout=60.0,
            )

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]
