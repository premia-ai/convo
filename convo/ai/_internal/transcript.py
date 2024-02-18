import os
import json
from convo import config, transcripts
from convo._utils import utils
from . import deepgram, open_ai


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

    transcript_data: transcripts.Transcript = {
        "metadata": {
            "audio_file_path": audio_file_path,
            "date": date,
            "speakers": speakers,
            "keywords": keywords,
        },
        "summary": open_ai.summarize(transcript, speakers),
        "content": deepgram.replace_speaker_placeholders(transcript, speakers),
    }
    transcript_file_content = json.dumps(transcript_data, indent=4)
    transcript_file_name = (
        f"{utils.get_file_name(audio_file_path)}_transcript.json"
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
