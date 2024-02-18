import os
import json
from deepgram import DeepgramClient, FileSource, PrerecordedOptions
from convo import config
from convo._utils import utils
from .types import DeepgramApiResponse
from .errors import CacheMissError


def transcribe(
    audio_file_path: str, speakers: list[str], keywords: list[str]
) -> DeepgramApiResponse:
    config_data = config.get_config_data()
    deepgram_config = config.get_ai_config_or_raise("deepgram")

    response_file_path = get_response_file_path(audio_file_path)
    if os.path.exists(response_file_path):
        raise Exception(
            f"Audio file has already been transcribed: '{audio_file_path}'."
        )

    deepgram = DeepgramClient(deepgram_config["api_key"])
    with open(audio_file_path, "rb") as file:
        buffer_data = file.read()

    payload: FileSource = {
        "buffer": buffer_data,
    }
    options = PrerecordedOptions(
        model=deepgram_config["model"],
        language="en",
        smart_format=True,
        punctuate=True,
        paragraphs=True,
        utterances=True,
        diarize=True,
        keywords=keywords + speakers + config_data["common_words"],
    )

    response = deepgram.listen.prerecorded.v("1").transcribe_file(
        payload, options
    )

    with open(
        response_file_path,
        "w",
    ) as file:
        file.write(response.to_json(indent=4))

    # TODO: Writing to disk and reading from it... This can be improved!
    return get_response(audio_file_path)


def get_response_file_path(audio_file_path: str) -> str:
    audio_file_name = utils.get_file_name(audio_file_path)
    response_file_name = f"{audio_file_name}.json"
    return os.path.join(config.CACHE_DIR_PATH, response_file_name)


def get_response(audio_file_path: str) -> DeepgramApiResponse:
    response_file_path = get_response_file_path(audio_file_path)
    if not os.path.exists:
        raise CacheMissError(audio_file_path)
    with open(response_file_path, "rb") as file:
        response: DeepgramApiResponse = json.load(file)

    return response


def get_transcript(response: DeepgramApiResponse) -> str:
    return response["results"]["channels"][0]["alternatives"][0]["paragraphs"][
        "transcript"
    ].strip()


def replace_speaker_placeholders(transcript: str, speakers: list[str]) -> str:
    for idx, speaker in enumerate(speakers):
        transcript = transcript.replace(f"Speaker {idx}", speakers[idx])

    return transcript
