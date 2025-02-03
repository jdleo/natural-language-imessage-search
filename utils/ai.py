from openai import OpenAI
from os import getenv
from typing import Optional


def get_openai_client() -> OpenAI:
    """Get configured OpenAI client for OpenRouter"""
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=getenv("OPENROUTER_API_KEY"),
    )


def get_sql_query(natural_query: str, prompt_template: str) -> Optional[str]:
    """Convert natural language query to SQL using the AI model"""
    try:
        client = get_openai_client()
        model = getenv("MODEL", "anthropic/claude-3.5-sonnet")

        # Replace placeholder in prompt template
        full_prompt = prompt_template.replace(":::query:::", natural_query)

        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "localhost:7860",  # Gradio default port
                "X-Title": "iMessage Search",
            },
            model=model,
            messages=[{"role": "user", "content": full_prompt}],
        )

        sql_query = completion.choices[0].message.content.strip()

        # Basic validation that we got a SQL query
        if not any(keyword in sql_query.upper() for keyword in ["SELECT", "FROM"]):
            return None

        print(f"SQL query: {sql_query}")
        return sql_query
    except Exception as e:
        print(f"Error getting SQL query: {str(e)}")
        return None
