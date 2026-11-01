"""
The optional AI shop assistant.

This is switched off until you put an API key in your .env file. With no
key, is_enabled() returns False and the website simply never shows the
chat button.

Both NVIDIA NIM and OpenRouter speak the same language here (the
"OpenAI-compatible" chat API), so the only difference between them is the
address and the key. That is why one small file covers both.
"""

import requests

from settings import AI_API_KEY, AI_BASE_URL, AI_MODEL, SHOP_NAME

# How long to wait for the AI service before giving up, in seconds.
TIMEOUT_SECONDS = 30

# The instruction the assistant is given before it ever sees your question.
# Change this to change its personality.
SYSTEM_PROMPT = f"""
You are a friendly shop assistant for an online shop called {SHOP_NAME}.
Help customers choose a product, and answer questions about the shop.
Keep answers to two or three sentences.
If you do not know something, say so instead of inventing an answer.
""".strip()


def is_enabled():
    """True only when all three settings have been filled in."""
    return bool(AI_API_KEY and AI_BASE_URL and AI_MODEL)


def ask(conversation):
    """
    Send the conversation to the AI service and return its reply as text.

    conversation is a list of messages, each like:
        {"role": "user", "content": "do you sell hats?"}
    """
    if not is_enabled():
        return "The AI assistant is switched off. See README.md to turn it on."

    # The system prompt always goes first, then everything said so far.
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation

    try:
        response = requests.post(
            f"{AI_BASE_URL}/chat/completions",
            # The key is sent from this server, never from the browser.
            # If we put it in the page, every visitor could read it and
            # spend our money.
            headers={"Authorization": f"Bearer {AI_API_KEY}"},
            json={
                "model": AI_MODEL,
                "messages": messages,
                "max_tokens": 300,
            },
            timeout=TIMEOUT_SECONDS,
        )
        response.raise_for_status()

        # The reply is buried a few layers down in the JSON that comes back.
        return response.json()["choices"][0]["message"]["content"]

    except requests.RequestException as error:
        # Something went wrong reaching the service: no internet, a wrong
        # key, or the service being busy. Say so plainly rather than
        # showing the visitor a crash.
        print(f"[chatbot] could not reach the AI service: {error}")
        return "Sorry, I could not reach the AI service just now. Please try again."
