import os
import json
from typing import Literal
from .errors import MissingAiProviderError
from .types import AiConfig, ConfigData, Provider

CONFIG_DIR_NAME = ".convo"
CONFIG_DIR_PATH = os.path.expanduser(f"~/{CONFIG_DIR_NAME}")
CONFIG_FILE_NAME = "config.json"
CONFIG_FILE_PATH = os.path.join(CONFIG_DIR_PATH, CONFIG_FILE_NAME)
CACHE_DIR_NAME = "cache"
CACHE_DIR_PATH = os.path.join(CONFIG_DIR_PATH, CACHE_DIR_NAME)
TRANSCRIPTS_DIR_NAME = "transcripts"
TRANSCRIPTS_DIR_PATH = os.path.join(CONFIG_DIR_PATH, TRANSCRIPTS_DIR_NAME)
DEFAULT_MODEL = {"deepgram": "nova-2", "open_ai": "gpt-3.5-turbo"}


def get_config_data() -> ConfigData:
    """
    Retrieve data from the config.json file.

    Returns:
        ConfigData: A dictionary containing the config data.
    Raises:
        FileNotFoundError: If config.json file doesn't exist.
    """
    if not os.path.exists(CONFIG_FILE_PATH):
        raise FileNotFoundError("config.json file not found.")

    with open(CONFIG_FILE_PATH, "r") as config_file:
        config_data: ConfigData = json.load(config_file)

    return config_data


def get_config_data_as_json() -> str:
    """
    Retrieve data from the config.json file as a JSON string.

    Returns:
        str: A JSON string of the config data.
    Raises:
        FileNotFoundError: If config.json file doesn't exist.
    """
    config_data = get_config_data()
    return json.dumps(config_data, indent=4)


def get_config_data_as_str() -> str:
    """
    Retrieve data from the config.json file as a formatted string.

    Returns:
        str: A formatted string of the config data.
    Raises:
        FileNotFoundError: If config.json file doesn't exist.
    """
    config_data = get_config_data()
    data = f"""\
Version:          {config_data['version']}
Common Words:     {', '.join(config_data['common_words'])}
"""

    if deepgram_config := config_data.get("deepgram"):
        data += f"""\
Deepgram:
    API-Key:          {deepgram_config['api_key']}
    Model:            {deepgram_config['model']}
"""

    if open_ai_config := config_data.get("open_ai"):
        data += f"""\
OpenAI:
    API-Key:          {open_ai_config['api_key']}
    Model:            {open_ai_config['model']}
"""

    return data


def get_ai_config_or_raise(provider: Provider) -> AiConfig:
    ai_config = get_ai_config(provider)
    if ai_config is None:
        raise MissingAiProviderError(provider)

    return ai_config


def get_ai_config(provider: Provider) -> AiConfig | None:
    config_data = get_config_data()
    return config_data.get(provider)


def set_ai_config(
    config_data: ConfigData,
    provider: Literal["deepgram", "open_ai"],
    api_key: str | None = None,
    model: str | None = None,
):
    """
    Set the fields of an AI provider.

    Raises:
        MissingAiProviderError: If you try to set a model on a provider that has no API-Key.
    """
    ai_config = config_data.get(provider)
    if ai_config:
        if api_key:
            ai_config["api_key"] = api_key
        if model:
            ai_config["model"] = model
    elif api_key:
        config_data[provider] = {
            "api_key": api_key,
            "model": model or DEFAULT_MODEL[provider],
        }
    else:
        raise MissingAiProviderError(provider)


def set_config_data(
    deepgram_api_key: str | None = None,
    deepgram_model: str | None = None,
    open_ai_api_key: str | None = None,
    open_ai_model: str | None = None,
    common_words: list[str] = [],
):
    """
    Set the fields of the config.json file.

    Raises:
        FileNotFoundError: If config.json file doesn't exist.
        MissingAiProviderError: If you try to set a provider that has no API-Key.
    """
    config_data = get_config_data()

    if deepgram_api_key or deepgram_model:
        set_ai_config(config_data, "deepgram", deepgram_api_key, deepgram_model)
    if open_ai_api_key or open_ai_model:
        set_ai_config(config_data, "open_ai", open_ai_api_key, open_ai_model)

    if common_words:
        unique_common_words = list(set(common_words))
        config_data["common_words"] = unique_common_words

    with open(CONFIG_FILE_PATH, "w") as config_file:
        json.dump(config_data, config_file, indent=4)


def get_transcripts(path=False) -> list[str]:
    """
    Retrieve all transcript names. Alternatively they can be returned as absolute paths.

    Args:
        path: If True, returns complete path instead of filename. Defaults to False.

    Returns:
        list[str]: A list of file names or complete paths.

    Raises:
        FileNotFoundError: If the folder does not exist.
    """
    if not os.path.exists(TRANSCRIPTS_DIR_PATH):
        raise FileNotFoundError("`transcripts` directory does not exist.")

    transcripts = os.listdir(TRANSCRIPTS_DIR_PATH)

    if path:
        transcripts = [
            os.path.join(TRANSCRIPTS_DIR_PATH, filename)
            for filename in transcripts
        ]

    return transcripts


def get_transcript(filename: str, path=False) -> str:
    """
    Retrieve the content or path of a transcript file.

    Args:
        filename: The name of the transcript file.
        path: If True, returns the path of the transcript. Defaults to False.

    Returns:
        str: The content of the transcript file or the path and content of the transcript file.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    transcript_path = os.path.join(TRANSCRIPTS_DIR_PATH, filename)

    if not os.path.exists(transcript_path):
        raise FileNotFoundError(
            f"Transcript file with the name '{filename}' does not exist."
        )

    if path:
        return transcript_path

    with open(transcript_path, "r") as file:
        content = file.read()
    return content


def setup() -> ConfigData:
    """
    Setup the `.convo` config folder with the following content:
      - `config.json` file
      - `cache` folder
      - `transcripts` folder

    Raises:
        FileExistsError: If the config folder already exists.
    """
    if os.path.exists(CONFIG_DIR_PATH):
        raise FileExistsError("Config directory already exists.")

    os.makedirs(CONFIG_DIR_PATH)

    os.makedirs(CACHE_DIR_PATH)
    os.makedirs(TRANSCRIPTS_DIR_PATH)

    initial_config_data: ConfigData = {
        "version": 1,
        "common_words": [],
    }
    with open(CONFIG_FILE_PATH, "w") as config_file:
        json.dump(initial_config_data, config_file, indent=4)

    return initial_config_data
