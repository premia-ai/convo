# Convo

A user friendly CLI for generating meeting transcripts and summaries using Deepgram and OpenAI.

## API Overview

```
convo
  setup
  config
    get                            -p/--path, -j/--json
    set
      common-words WORD [WORD ...]
      deepgram                     -a/--api-key  -m/--model
      open-ai                      -a/--api-key  -m/--model
    add
      common-words WORD [WORD ...]
    remove
      common-words WORD [WORD ...]
  ai
    transcribe  AUDIO_FILE_PATH -s/--speaker, -k/--keyword, -d/--date, -c/--cache
```
