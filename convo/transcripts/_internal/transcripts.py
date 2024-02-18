import os
import yaml
import json
from convo import config
from convo._utils import utils
from .types import Transcript

TRANSCRIPT_MARKDOWN_TEMPLATE = """\
---
{yaml_metadata}
---

# {title}

## Summary

{summary}

## Transcript

{transcript}

"""


def create_title(speakers: list[str], date: str) -> str:
    return f"Conversation between {utils.list_to_str(speakers)} ({date})"


def to_markdown(transcript: Transcript) -> str:
    return TRANSCRIPT_MARKDOWN_TEMPLATE.format(
        yaml_metadata=yaml.dump(transcript["metadata"]).strip(),
        title=create_title(
            transcript["metadata"]["speakers"], transcript["metadata"]["date"]
        ),
        transcript=transcript["content"],
        summary=transcript["summary"],
    )


def list(path=False) -> list[str]:
    """
    Collect transcript file names or paths.

    Args:
        path (bool, optional): If True, include the complete path of each transcript. If False, include only the file name. Default is False.
    Returns:
        list[str]: List of transcript file names or paths.
    """
    transcript_names = []
    for transcript_name in os.listdir(config.TRANSCRIPTS_DIR_PATH):
        if path:
            file_path = os.path.join(
                config.TRANSCRIPTS_DIR_PATH, transcript_name
            )
            transcript_names.append(file_path)
        else:
            transcript_names.append(transcript_name)
    return transcript_names


def show(
    transcript_name: str,
    summary=False,
    content=False,
    metadata=False,
    path=False,
    as_json=False,
) -> str:
    """
    Retrieve the contents of a transcript file.

    Args:
        transcript_name (str): Name of the transcript file.
        summary (bool, optional): If True, return summary of transcript. Default is False.
        content (bool, optional): If True, return content of transcript. Default is False.
        metadata (bool, optional): If True, return metadata of transcript. Default is False.
        as_json (bool, optional): If True, return transcript data as JSON string. Default is False.
        path (bool, optional): If True, return path of transcript. Default is False.
    Returns:
        str: Content of the transcript file.
    Raises:
        FileNotFoundError: If transcript file with specified name doesn't exist.
    """
    transcript_path = os.path.join(config.TRANSCRIPTS_DIR_PATH, transcript_name)

    if os.path.exists(transcript_path):
        if path:
            return transcript_path

        with open(transcript_path, "r") as file:
            if as_json:
                return file.read()

            transcript_data: Transcript = json.load(file)

        if summary:
            return transcript_data["summary"]
        if content:
            return transcript_data["content"]
        if metadata:
            return json.dumps(transcript_data["metadata"], indent=4)

        return to_markdown(transcript_data)

    raise FileNotFoundError(f"Transcript '{transcript_name}' does not exist.")
