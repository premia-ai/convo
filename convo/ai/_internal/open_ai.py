from openai import OpenAI
from convo import config
from convo._utils import utils
from .context import get_context

SYSTEM_PROMPT_SUMMARY_TEMPLATE = """\
You are a transcript summarization assistant. Your job is to extract key pieces of information from a transcript of a work conversation between {speakers}.

The user requesting the summary is called {user_name}.

Focus your summary on the following:
1. Information mentioned by participants other than the user
2. Professional information, like company details and product specifications

Keep your summary succinct and clear.
"""

SYSTEM_PROMPT_QUERY_TEMPLATE = """\
You are a helpful text search assistant. Your job is to find transcripts based on their summary.

The user will ask you about a given transcript and you respond with possible candidates. Mention the name of the file as well as why you selected it.

List of transcripts:
{context}
"""


def query(user_prompt: str) -> str:
    open_ai_config = config.get_ai_config_or_raise("open_ai")
    client = OpenAI(api_key=open_ai_config["api_key"])

    stream = client.chat.completions.create(
        model=open_ai_config["model"],
        stream=True,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT_QUERY_TEMPLATE.format(
                    context=get_context()
                ),
            },
            {"role": "user", "content": user_prompt},
        ],
    )

    complete_response = ""
    for chunk in stream:
        token = chunk.choices[0].delta.content or ""
        print(token, end="", flush=True)
        complete_response += token

    return complete_response


def summarize(transcript: str, speakers: list[str]) -> str:
    config_data = config.get_config_data()
    open_ai_config = config.get_ai_config_or_raise("open_ai")
    client = OpenAI(api_key=open_ai_config["api_key"])

    completion = client.chat.completions.create(
        model=open_ai_config["model"],
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT_SUMMARY_TEMPLATE.format(
                    speakers=utils.list_to_str(speakers),
                    user_name=config_data["user"]["name"],
                ),
            },
            {"role": "user", "content": transcript},
        ],
    )

    return completion.choices[0].message.content or ""
