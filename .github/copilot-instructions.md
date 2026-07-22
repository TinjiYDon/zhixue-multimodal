# Copilot / Agent instructions — zhixue-multimodal

Mirror of root `AGENTS.md` for GitHub Copilot.

- Stack: FastAPI (`backend/`), Vue (`web/`), UniApp (`miniapp/`)
- Test: `cd backend && .venv\Scripts\python.exe -m pytest tests/ -q`
- Ask path: `POST /api/v1/courses/{id}/ask` — never `/api/v1/ask`
- Timeline: `GET /api/v1/courses/{id}/timeline`
- Do not implement Whisper in workers; call multimedia `transcribe_media`
- Schema SSOT: `backend/app/schemas/transcript.py`
- Do not commit dump/secrets; keep PRs scoped to your module
