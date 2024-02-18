from openai import OpenAI
from convo import config

SYSTEM_PROMPT_TEMPLATE = """\
You are a transcript summarization assistant. Your job is to extract key pieces of information from a transcript of a professional conversation.

Focus your summary on the following:
1. The person being interviewed, not the interviewer
2. Professional information, like company details and product specifications

Keep your summary succinct and clear.
"""


def summarize(transcript: str) -> str:
    open_ai_config = config.get_ai_config_or_raise("open_ai")
    client = OpenAI(api_key=open_ai_config["api_key"])

    completion = client.chat.completions.create(
        model=open_ai_config["model"],
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT_TEMPLATE},
            {"role": "user", "content": transcript},
        ],
    )

    return completion.choices[0].message.content or ""
