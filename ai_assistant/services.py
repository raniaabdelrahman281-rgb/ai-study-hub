"""
Thin wrapper around an external AI provider's chat-completions API.
"""

import requests
from django.conf import settings


class AIServiceError(Exception):
    pass


def call_ai(system_prompt: str, user_prompt: str, max_tokens: int = 600) -> str:
    """Send a prompt to the configured AI provider and return the text reply."""

    if not settings.AI_API_KEY:
        raise AIServiceError(
            "No AI_API_KEY configured. Add one to your .env file to enable the AI features."
        )

    payload = {
        "model": settings.AI_MODEL,
        "messages": [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7,
    }

    headers = {
        "Authorization": f"Bearer {settings.AI_API_KEY}",
        "Content-Type": "application/json",
    }

    endpoint = settings.AI_API_URL.rstrip("/") + "/chat/completions"

    try:
        resp = requests.post(
            endpoint,
            json=payload,
            headers=headers,
            timeout=30,
        )
        resp.raise_for_status()

    except requests.RequestException as exc:
        raise AIServiceError(
            f"Could not reach the AI provider: {exc}"
        ) from exc

    data = resp.json()

    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise AIServiceError(
            f"Unexpected AI provider response: {data}"
        ) from exc


def chat_reply(message: str) -> str:
    return call_ai(
        system_prompt=(
            "You are a helpful study assistant. "
            "Answer the student's questions clearly and simply."
        ),
        user_prompt=message,
        max_tokens=800,
    )


def summarize_text(text: str) -> str:
    return call_ai(
        system_prompt=(
            "You are a helpful study assistant. "
            "Summarize the student's note into concise bullet points "
            "that are easy to revise from."
        ),
        user_prompt=text,
        max_tokens=600,
    )


def generate_quiz(text: str, num_questions: int = 5) -> str:
    return call_ai(
        system_prompt=(
            f"You are a helpful study assistant. Create {num_questions} "
            "multiple-choice quiz questions based on the student's text. "
            "Each question should have 4 options and clearly mark "
            "the correct answer."
        ),
        user_prompt=text,
        max_tokens=1200,
    )


def generate_flashcards(text: str, num_cards: int = 5) -> str:
    return call_ai(
        system_prompt=(
            f"You are a helpful study assistant. Create {num_cards} "
            "useful study flashcards from the student's text. "
            "Format each flashcard clearly as Question and Answer."
        ),
        user_prompt=text,
        max_tokens=1000,
    )


def explain_error(error_text: str) -> str:
    return call_ai(
        system_prompt=(
            "You are a helpful programming tutor. "
            "Explain the error simply, identify the cause, "
            "and give clear steps to fix it."
        ),
        user_prompt=error_text,
        max_tokens=800,
    )