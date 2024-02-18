import os
import yaml
from convo import config
from convo._utils import utils
from . import deepgram, open_ai

TRANSCRIPT_TEMPLATE = """\
---
{yaml_metadata}
---

# {title}

## Summary

{summary}

## Transcript

{transcript}

"""


def list_to_str(values: list[str]) -> str:
    result = ", ".join(values)

    last_comma_index = result.rfind(",")
    if last_comma_index != -1:
        result = (
            result[:last_comma_index] + " and" + result[last_comma_index + 1 :]
        )

    return result


def create_title(speakers: list[str], date: str) -> str:
    return f"Conversation between {list_to_str(speakers)} ({date})"


def create_transcript(
    audio_file_path: str,
    speakers: list[str],
    keywords: list[str],
    date: str,
    cache=False,
) -> None:
    # TODO: When you have time you can make this prettier.
    # Seems unnecessarily weird how the response is handled here.
    if not cache:
        deepgram_api_response = deepgram.transcribe(
            audio_file_path, speakers, keywords
        )
        transcript = deepgram.get_transcript(deepgram_api_response)
    else:
        deepgram_api_response = deepgram.get_response(audio_file_path)
        transcript = deepgram.get_transcript(deepgram_api_response)

    transcript = deepgram.replace_speaker_placeholders(transcript, speakers)

    summary = open_ai.summarize(transcript)

    metadata = {
        "audio_file_path": audio_file_path,
        "date": date,
        "speakers": speakers,
        "keywords": keywords,
    }

    transcript_file_content = TRANSCRIPT_TEMPLATE.format(
        yaml_metadata=yaml.dump(metadata),
        title=create_title(speakers, date),
        transcript=transcript,
        summary=summary,
    )
    transcript_file_name = (
        f"{utils.get_file_name(audio_file_path)}_transcript.md"
    )
    transcript_file_path = os.path.join(
        config.TRANSCRIPTS_DIR_PATH, transcript_file_name
    )

    if cache and os.path.exists(transcript_file_path):
        os.remove(transcript_file_path)

    with open(
        transcript_file_path,
        "w",
    ) as file:
        file.write(transcript_file_content)
