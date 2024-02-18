import sys
from datetime import datetime
import click
import convo


@click.version_option("0.0.1", prog_name="convo")
@click.group()
def convo_cli():
    """Convo is a cli to create transcripts from recorded meetings."""
    pass


@convo_cli.group("config")
def config_group():
    """Interact with convo's configuration."""


@config_group.command("setup")
@click.argument("user_name")
@click.option(
    "-g",
    "--gender",
    type=click.Choice(convo.config.GENDERS),
    default="not-specified",
    help="Specify a gender so that the AI can use the correct pronouns.",
)
def config_setup(user_name: str, gender: convo.config.Gender):
    """Set up convo with. Specify your real name and gender so that the AIs can improve both summaries and transcripts."""
    try:
        convo.config.setup(user_name, gender)
    except Exception as e:
        click.secho(e, fg="red")
        sys.exit(1)

    click.secho("Successfully setup convo.", fg="green")


@config_group.command("get")
@click.option(
    "-p",
    "--path",
    is_flag=True,
    default=False,
    help="Show the path to the config.json file",
)
@click.option(
    "-j",
    "--json",
    is_flag=True,
    default=False,
    help="Print the content of config.json in JSON format to stdout.",
)
def config_get(path: bool, json: bool):
    """Print the convo's configuration to stdout."""
    try:
        if path:
            click.echo(convo.config.CONFIG_FILE_PATH)
            return
        if json:
            click.echo(convo.config.get_config_data_as_json())
            return
        click.echo(convo.config.get_config_data_as_str())
    except Exception as e:
        click.secho(e, fg="red")
        sys.exit(1)


@config_group.group("set")
def config_set_group():
    """Update convo's configuration."""


@config_set_group.command("user")
@click.option("-n", "--name")
@click.option(
    "-g",
    "--gender",
    type=click.Choice(convo.config.GENDERS),
    help="Specify a gender so that the AI can use the correct pronouns.",
)
def config_set_user(name: str | None, gender: convo.config.Gender | None):
    """Set up the user information in the configuration."""
    try:
        convo.config.set_config_data(user_name=name, user_gender=gender)
    except Exception as e:
        click.secho(e, fg="red")
        sys.exit(1)

    click.secho("Successfully set your user data.", fg="green")


@config_set_group.command("deepgram")
@click.option("-a", "--api-key")
@click.option(
    "-m",
    "--model",
    default=convo.config.DEFAULT_MODEL["deepgram"],
    show_default=True,
)
def config_set_deepgram(api_key: str | None, model: str):
    """Set up Deepgram in the configuration."""
    try:
        config_data = convo.config.get_config_data()
        if config_data.get("deepgram") is None and api_key is None:
            click.secho(
                "To set up Deepgram you need to add an API-Key", fg="red"
            )
            sys.exit(1)
        else:
            convo.config.set_config_data(
                deepgram_api_key=api_key, deepgram_model=model
            )
    except Exception as e:
        click.secho(e, fg="red")
        sys.exit(1)

    click.secho("Successfully set up Deepgram.", fg="green")


@config_set_group.command("open-ai")
@click.option("-a", "--api-key")
@click.option(
    "-m",
    "--model",
    default=convo.config.DEFAULT_MODEL["open_ai"],
    show_default=True,
)
def config_set_api_key(api_key: str | None, model: str):
    """Set up OpenAI in the configuration."""
    try:
        config_data = convo.config.get_config_data()
        if config_data.get("open_ai") is None and api_key is None:
            click.secho("To set up OpenAI you need to add an API-Key", fg="red")
            sys.exit(1)
        else:
            convo.config.set_config_data(
                open_ai_api_key=api_key, open_ai_model=model
            )
    except Exception as e:
        click.secho(e, fg="red")
        sys.exit(1)

    click.secho("Successfully set up OpenAI.", fg="green")


@config_set_group.command("common-words")
@click.argument("words", nargs=-1)
def config_set_common_words(words: tuple[str]):
    """Set a set of words as common words in the configuration. These should be words like company names or product names that the AI might not know and you commonly use."""
    try:
        convo.config.set_config_data(common_words=list(words))
    except Exception as e:
        click.secho(e, fg="red")
        sys.exit(1)

    click.secho(
        f"Successfully set '{', '.join(words)}' as common words", fg="green"
    )


@config_group.group("add")
def config_add_group():
    """Add values to convo's configuration."""


@config_add_group.command("common-words")
@click.argument("words", nargs=-1)
def config_add_common_words(words: tuple[str]):
    """Add a set of words to your list of common words in the configuration. These should be words like company names or product names that the AI might not know and you commonly use."""
    try:
        config_data = convo.config.get_config_data()
        all_common_words = config_data["common_words"] + list(words)
        convo.config.set_config_data(common_words=list(all_common_words))
    except Exception as e:
        click.secho(e, fg="red")
        sys.exit(1)

    click.secho(
        f"Successfully set common words to '{', '.join(all_common_words)}'",
        fg="green",
    )


@config_group.group("remove")
def config_remove_group():
    """Remove values from convo's configuration."""


@config_remove_group.command("common-words")
@click.argument("words", nargs=-1)
def config_remove_common_words(words: tuple[str]):
    """Remove a set of words from your list of common words in the configuration."""
    try:
        config_data = convo.config.get_config_data()
        common_words_left = [
            word for word in config_data["common_words"] if word not in words
        ]
        convo.config.set_config_data(common_words=list(common_words_left))
    except Exception as e:
        click.secho(e, fg="red")
        sys.exit(1)

    click.secho(
        f"Successfully set common words to '{', '.join(common_words_left)}'",
        fg="green",
    )


@convo_cli.group("ai")
def ai_group():
    """Use an AI to transcribe your audio files."""
    pass


@ai_group.command("context")
def ai_context():
    """Print the query context the AI uses to answer questions to stdout."""
    click.echo(convo.ai.get_context())


@ai_group.command("query")
@click.argument("prompt")
def ai_query(prompt: str):
    """Question an AI about the summaries of the transcripts."""
    convo.ai.query(prompt)


@ai_group.command("transcribe")
@click.argument("audio_file_path")
@click.option(
    "-s",
    "--speaker",
    "speakers",
    multiple=True,
    help="The conversation participants in the order they join the conversation.",
)
@click.option(
    "-k",
    "--keyword",
    "keywords",
    multiple=True,
    help="Important keywords of the conversation that the AI could misunderstand.",
)
@click.option(
    "-d",
    "--date",
    help="Date of the conversation. Defaults to today.",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=datetime.now(),
)
@click.option(
    "-c",
    "--cache",
    is_flag=True,
    default=False,
    help="Use cached transcript instead of making another API call to Deepgram.",
)
def ai_transcribe(
    audio_file_path: str,
    speakers: tuple[str],
    keywords: tuple[str],
    date: datetime,
    cache: bool,
):
    """Transcribe an audio file."""
    try:
        convo.ai.create_transcript(
            audio_file_path,
            list(speakers),
            list(keywords),
            date.date().strftime("%Y-%m-%d"),
            cache=cache,
        )
    except Exception as e:
        click.secho(e, fg="red")
        sys.exit(1)

    click.secho(f"Successfully transcribed '{audio_file_path}'.", fg="green")


@convo_cli.group("transcripts")
def transcripts_group():
    """Manage existing transcripts."""


@transcripts_group.command("list")
@click.option(
    "-p",
    "--path",
    is_flag=True,
    default=False,
    help="Print file paths instead of file names.",
)
def transcripts_list(path: bool):
    """List all existing transcripts"""
    click.echo("\n".join(convo.transcripts.list(path)) + "\n")


@transcripts_group.command("show")
@click.argument("transcript_name")
@click.option(
    "-s",
    "--summary",
    is_flag=True,
    default=False,
    help="Print only summary without content and metadata.",
)
@click.option(
    "-c",
    "--content",
    is_flag=True,
    default=False,
    help="Print only transcript without summary and metadata.",
)
@click.option(
    "-m",
    "--metadata",
    is_flag=True,
    default=False,
    help="Print only metadata without summary and transcript.",
)
@click.option(
    "-j",
    "--json",
    is_flag=True,
    default=False,
    help="Print transcript data as JSON.",
)
@click.option(
    "-p",
    "--path",
    is_flag=True,
    default=False,
    help="Print file paths instead of file content.",
)
def transcripts_show(
    transcript_name: str,
    summary: bool,
    content: bool,
    metadata: bool,
    json: bool,
    path: bool,
):
    """Show the complete or a specified part of a transcripts"""
    try:
        click.echo(
            convo.transcripts.show(
                transcript_name=transcript_name,
                summary=summary,
                content=content,
                metadata=metadata,
                path=path,
                as_json=json,
            )
        )
    except Exception as e:
        click.secho(e, fg="red")
        sys.exit(1)
