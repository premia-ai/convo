# Convo

A user friendly CLI for generating meeting transcripts and summaries using Deepgram and OpenAI.

## API Overview

```
convo
  setup            USER_NAME       -g/--gender
  config
    get                            -p/--path, -j/--json
    set
      user                         -u/--user-name, -g/--gender
      common-words WORD [WORD ...]
      deepgram                     -a/--api-key, -m/--model
      open-ai                      -a/--api-key, -m/--model
    add
      common-words WORD [WORD ...]
  ai
    context
    query       QUERY
    transcribe  AUDIO_FILE_PATH -s/--speaker, -k/--keyword, -d/--date
  transcripts
    list                  -p/--path, -m/--metadata, -s/--speakers, -k/--keywords, -d/--date, -j/--json
    ls (alias)            -p/--path, -m/--metadata, -S/--summary, -s/--speakers, -k/--keywords, -d/--date, -j/--json
    show   TRANSCRIPT_NAME -p/--path, -m/--metadata, -f/--full, -s/--summary, -j/--json
    remove TRANSCRIPT_NAME -y/--yes, -c/--clear-cache
```

## Important

This repo is still under quick iterative development. Things might change quickly and are probably incomplete.
