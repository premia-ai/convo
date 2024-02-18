from typing import NotRequired, TypedDict, Literal

type Provider = Literal['deepgram', 'open_ai']

class AiConfig(TypedDict):
    api_key: str
    model: str


class ConfigData(TypedDict):
    version: int
    common_words: list[str]
    deepgram: NotRequired[AiConfig]
    open_ai: NotRequired[AiConfig]
