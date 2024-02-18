from typing import NotRequired, TypedDict, Literal

type Provider = Literal['deepgram', 'open_ai']
type Gender = Literal['female', 'male', 'non-binary', 'not-specified']
GENDERS: list[Gender] = ['female', 'male', 'non-binary', 'not-specified']

class AiConfig(TypedDict):
    api_key: str
    model: str

class UserConfig(TypedDict):
    name: str
    gender: Gender


class ConfigData(TypedDict):
    version: int
    common_words: list[str]
    user: UserConfig
    deepgram: NotRequired[AiConfig]
    open_ai: NotRequired[AiConfig]
