from typing import TypedDict


class TranscriptMetadata(TypedDict):
    audio_file_path: str
    date: str
    speakers: list[str]
    keywords: list[str]


class Transcript(TypedDict):
    metadata: TranscriptMetadata
    summary: str
    content: str
