# Copilot / Agent instructions — zhixue-multimodal

Mirror of root `AGENTS.md` for GitHub Copilot.

- Stack: FastAPI (`backend/`), Vue (`web/`), UniApp (`miniapp/`)
- Test: `cd backend && .venv\Scripts\python.exe -m pytest tests/ -q`
- Ask path: `POST /api/v1/courses/{id}/ask` — never `/api/v1/ask`
- Timeline: `GET /api/v1/courses/{id}/timeline`
- Jobs: `POST/GET /api/v1/jobs` (in-memory skeleton); upload/complete auto-creates job
- Do not implement Whisper in workers; call multimedia `transcribe_media`
- Schema SSOT: `backend/app/schemas/transcript.py`
- Course/Job PG persistence still owned by D (`#P0-2b` / `#P0-4c`)
- Do not commit dump/secrets; keep PRs scoped to your module
