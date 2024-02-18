from typing import TypedDict, Mapping, Literal


class ModelInfo(TypedDict):
    name: str
    version: str
    arch: str

type ModelInfos = Mapping[str, ModelInfo]

class Metadata(TypedDict):
    transacation_key: str
    request_id: str
    sha256: str
    created: str
    duration: float
    channels: int
    models: list[str]
    model_info: ModelInfos

class Word(TypedDict):
    word: str
    start: float
    end: float
    confidence: float
    punctuated_word: str
    speaker: int
    speaker_confidence: float

class Sentence(TypedDict):
    text: str
    start: float
    end: float

class Paragraph(TypedDict):
    sentences: list[Sentence]
    start: float
    end: float
    num_words: float
    speaker: int

class Paragraphs(TypedDict):
    transcript: str
    paragraphs: list[Paragraph]

class Alternative(TypedDict):
    transcript: str
    confidence: float
    words: list[Word]
    paragraphs: Paragraphs

class Channel(TypedDict):
    alternatives: list[Alternative]
    detected_language: str
    language_confidence: str

class Utterance(TypedDict):
    start: float
    end: float
    confidence: float
    channel: int
    transcript: str
    words: list[Word]
    speaker: int
    id: str

class Summary(TypedDict):
    result: Literal["success", "failure"]
    short: str

class Results(TypedDict):
    channels: list[Channel]
    utterances: list[Utterance] | None
    summary: Summary | None

class DeepgramApiResponse(TypedDict):
    metadata: Metadata
    results: Results
