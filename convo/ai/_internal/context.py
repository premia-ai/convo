import os
import json
from convo import config


# TODO: allow reducing the size of the summaries
def get_context() -> str:
    """
    Create context for an AI to use to answer questions about the transcripts.

    Returns:
        str: String of transcript file names and their summaries.
    """
    summaries = []
    for file_name in os.listdir(config.TRANSCRIPTS_DIR_PATH):
        file_path = os.path.join(config.TRANSCRIPTS_DIR_PATH, file_name)
        with open(file_path, "r") as file:
            transcript_data = json.load(file)
            summary = transcript_data["summary"]
            summaries.append(f"Name: {file_name}\nSummary: {summary}\n")
    return "\n".join(summaries)
