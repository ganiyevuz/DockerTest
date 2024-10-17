from openai import OpenAI, AuthenticationError, RateLimitError, OpenAIError
from rest_framework.exceptions import ValidationError, ParseError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_401_UNAUTHORIZED, \
    HTTP_429_TOO_MANY_REQUESTS

from httpx import get, TimeoutException, HTTPError

from conf.settings import OPENAI_API_KEY, UZA_BASE_URL

client = OpenAI(api_key=OPENAI_API_KEY)


def get_article(slug, lang=None):
    try:
        response = get(f'{UZA_BASE_URL}/{slug}?include=theme,tags,translations&_f=json&_l={lang}')
        if response.status_code == 200:
            return response.json()
    except HTTPError:
        raise ParseError("Failed to connect to the UZA API. Please try again later.")


def summarize(text, lang):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant that summarizes text concisely and clearly."
                },
                {
                    "role": "user",
                    "content": f"Please summarize the following text:\n\n{text}"
                }
            ],
            max_tokens=150,
            temperature=0.5,
        )
        return response.choices[0].message.content.strip()

    except AuthenticationError:
        raise ValidationError("Authentication with OpenAI failed. Check your API key.")
    except RateLimitError:
        raise ValidationError("Rate limit exceeded. Please try again later.")
    except OpenAIError as e:
        raise ValidationError(f"OpenAI API error: {str(e)}")
