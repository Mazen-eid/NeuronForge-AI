# NeuronForge AI

**An honest, open-source toolkit for running automated YouTube / short-form video channels.**
Discover trends → write scripts with an LLM → narrate with free TTS → compose videos with FFmpeg → upload to YouTube on a schedule.

> 🇪🇬 للعربية: راجع [README.ar.md](README.ar.md).

---

## What this project is — and is not

**It IS:**
- A working pipeline (`trends → script → TTS → video → upload`) that you can run on your own machine.
- Modular so you can swap each stage (different LLM, different TTS, different trend source).
- Designed to degrade gracefully: if you have **zero API keys**, everything still runs in dry-run mode and produces a playable MP4.

**It is NOT:**
- A magic "zero-capital passive income" machine. You will still need:
  - Your own YouTube channel (free to create).
  - A Google Cloud project with OAuth credentials for uploading (free quota, enough for ~6 uploads/day/channel).
  - Optionally, a free Groq API key for the LLM (~$0/month at low volume), or a paid OpenAI key.
- A substitute for creative direction. Automated channels that never get human review are the fastest way to get terminated by YouTube's spam/AI-content policies. **Supervise your channels.**

**Honest cost table** (what it actually takes to run 1 channel, ~3 uploads/day):

| Service | Free tier enough? | Notes |
|---|---|---|
| LLM (Groq) | ✅ Yes | 14,400 requests/day free at the time of writing |
| LLM (OpenAI `gpt-4o-mini`) | ❌ Paid | ~$0.50–2 / month for this volume |
| TTS (Edge TTS) | ✅ Yes | Uses Microsoft Edge's public neural voices |
| Stock media (Pexels / Pixabay) | ✅ Yes | Free API keys with no credit card |
| YouTube upload | ✅ Yes | Free quota is 10,000 "units"/day; one upload ≈ 1,600 |
| Compute | ✅ Yes | Runs on any laptop; no GPU required |

---

## Architecture

```
┌──────────────┐   ┌────────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ trends/      │→  │ llm/       │→  │ tts/     │→  │ video/   │→  │ uploader/│
│ google_trends│   │ groq/ollama│   │ edge_tts │   │ FFmpeg   │   │ youtube  │
│ reddit       │   │ openai/mock│   │          │   │ + subs   │   │          │
│ youtube_rss  │   └────────────┘   └──────────┘   └──────────┘   └──────────┘
└──────────────┘         ↑                                              ↓
                         │             orchestrator.py                  │
                         └──────────────────┬───────────────────────────┘
                                            │
                                  scheduler.py (APScheduler, cron)
                                            │
                                  SQLite DB (runs, used_topics)
                                            │
                                  FastAPI API  ⇆  frontend/ dashboard
```

---

## Quick start

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Dry run with mock LLM — no keys needed. Produces an MP4 under data/runs/<id>/video.mp4
neuronforge run example-en-tech --dry-run

# Start the API for the web dashboard
neuronforge api
# In another terminal, open frontend/index.html (or serve it with `python -m http.server -d frontend 5173`)
```

### Upload for real

1. Create a channel config under `backend/channels/<your-channel>.yaml` (copy one of the examples).
2. Get a Groq key (free): <https://console.groq.com/keys>. Put it in `backend/.env` as `GROQ_API_KEY=…`, set `LLM_PROVIDER=groq`.
3. Set up YouTube upload credentials (one-time, free):
   - <https://console.cloud.google.com/> → new project → **Enable API** → "YouTube Data API v3".
   - **OAuth consent screen** → External → Testing → add your Gmail as a test user.
   - **Credentials** → "Create credentials" → OAuth client ID → Desktop app → download JSON.
   - Save it to `backend/secrets/youtube_client_secret.json`.
   - Run `neuronforge youtube-auth <channel_id>` once per channel. A browser window completes the flow.
4. Run: `neuronforge run <channel_id> --upload`.
5. Schedule it: `neuronforge schedule` (uses the `cron:` field from each channel YAML).

---

## Channel config (YAML)

```yaml
id: example-en-tech
language: en                 # en | ar | fr | es
niche: AI and technology news
platform: youtube_shorts     # youtube_shorts | youtube_long | tiktok
target_duration_seconds: 45
resolution: [1080, 1920]
fps: 30
tone: punchy, curious, accurate
tts_voice: null              # auto-selected by language if null
youtube_category_id: "28"
youtube_privacy: private     # start private, flip to public when reviewed
cron: "0 */6 * * *"          # every 6 hours
trend_sources:
  - { kind: reddit,         query: artificial }
  - { kind: google_trends,  query: united_states }
  - { kind: youtube_rss,    query: UC... }     # another channel's ID
```

To add more channels, drop more YAML files into `backend/channels/`. They're picked up automatically by the API, the CLI, and the scheduler.

---

## Safety & ToS

This repo uses only **official APIs** for uploading (YouTube Data API v3 with your own OAuth credentials). TikTok does not offer an open upload API for individual creators — there is intentionally no TikTok uploader in this repo. Manually post the generated `data/runs/<id>/video.mp4` files to TikTok until Meta/TikTok open their APIs.

**Do not** pipe raw AI output to a public channel. YouTube actively enforces against spammy/low-quality automation. Start every channel on `privacy: private`, review samples, then promote to public.

---

## Development

```bash
cd backend
pip install -e ".[dev]"
ruff check .
pytest -q
```

CI runs the same two commands on every PR.

---

## License

MIT. See `LICENSE`.
