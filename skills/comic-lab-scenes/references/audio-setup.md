# Voice setup

Checked 2026-10-29. Create an API key in your own provider account and store it in a private environment file outside the downloadable skill and any public directory. Use `--env-file /absolute/private/path/voices.env`, or export variables in your shell. Do not paste keys in chat, put them in a brief, or commit them. The script sends the dialogue text to the selected provider. Cloud voice generation requires network access and the provider's billing/access; rendering remains local.

## ElevenLabs

[Create a key](https://elevenlabs.io/app/settings/api-keys) and choose two voices your account can use. Use their IDs, not display names.

```dotenv
ELEVENLABS_API_KEY=
ELEVENLABS_STUDENT_VOICE_ID=
ELEVENLABS_TUTOR_VOICE_ID=
ELEVENLABS_MODEL=eleven_multilingual_v2
```

Run preparation with `--provider elevenlabs`. The adapter calls the [Create speech endpoint](https://elevenlabs.io/docs/api-reference/text-to-speech/convert), receives MP3, converts it locally to mono WAV and measures the real duration. It does not need voice cloning or timestamp alignment. Provider access was not available for a live test; request shape and configuration were checked against the official documentation.

## Fish Audio

Create a key in your [Fish Audio API account](https://fish.audio/app/api-keys). Choose two authorized voice/reference IDs available to your account.

```dotenv
FISH_AUDIO_API_KEY=
FISH_STUDENT_REFERENCE_ID=
FISH_TUTOR_REFERENCE_ID=
FISH_MODEL=s2.1-pro-free
```

Run with `--provider fish`. The adapter uses [the official TTS endpoint](https://docs.fish.audio/api-reference/endpoint/openapi-v1/text-to-speech) with the model header and reference ID. Model availability depends on your account; adjust `FISH_MODEL` to a supported option. Do not infer that voice calls are universally free from a model ID. This adapter has not been live-tested in this package.

## OpenAI: provider used for the recorded examples

```dotenv
OPENAI_API_KEY=
OPENAI_STUDENT_VOICE=marin
OPENAI_TUTOR_VOICE=cedar
OPENAI_TTS_MODEL=gpt-4o-mini-tts
```

Run with `--provider openai`. The five recorded films use these two built-in synthetic voices, without cloning the reference narrator. Calls to `/v1/audio/speech` worked during testing. The [official TTS guide](https://developers.openai.com/api/docs/guides/text-to-speech) now lists this Speech model as deprecated, with shutdown scheduled for January 6, 2027. Its replacement uses a different Realtime API workflow; changing the model name alone will not migrate this adapter. Choose ElevenLabs/Fish, supply recorded audio, or update the adapter for the current Realtime API after that date. This limitation is explicit; no claim of a tested Realtime integration is made.

## Existing recordings and offline rerenders

Supply one mono or stereo WAV per turn, named `00.wav` through the last turn. No provider key is needed:

```sh
python3 <skill>/scripts/prepare.py brief.json --out output/recorded-01 --provider recorded --audio-dir /path/to/wavs
```

The included recordings can be reused to rerender the same example after editing camera or scene code. For changed dialogue, generate or provide matching new audio. Never claim reused speech demonstrates a new script.

Claude can write the lesson and call a connected speech service; this package does not assume native audio synthesis in Claude. Credentials are account-specific and are never supplied as part of a download.
