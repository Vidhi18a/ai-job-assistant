# AI Job Assistant

A small AI-assisted job search app for data and AI roles. It searches curated JSON job data, ranks matches from skills or a short background summary, and explains the fit.

## App Shape

- Frontend: static [index.html](c:/Users/shahv/OneDrive/Documents/ai-job-assistant/index.html)
- API: Vercel Python Function at [search.py](c:/Users/shahv/OneDrive/Documents/ai-job-assistant/api/search.py)
- Search logic: shared Python modules in [app](c:/Users/shahv/OneDrive/Documents/ai-job-assistant/app)
- Data pipeline: [etl.py](c:/Users/shahv/OneDrive/Documents/ai-job-assistant/scripts/etl.py) generates normalized silver data from bronze JSON
- Python runtime metadata: [requirements.txt](c:/Users/shahv/OneDrive/Documents/ai-job-assistant/requirements.txt)

## Local Checks

Run the test suite:

```powershell
pytest -q
```

Regenerate normalized job data:

```powershell
python scripts/etl.py
```

## Deploy To Vercel

This repo is set up for:

- static frontend routing from [vercel.json](c:/Users/shahv/OneDrive/Documents/ai-job-assistant/vercel.json)
- Python serverless API deployment from `api/*.py`
- explicit Python dependency metadata in [requirements.txt](c:/Users/shahv/OneDrive/Documents/ai-job-assistant/requirements.txt)

### 1. Install Vercel CLI

```powershell
npm install -g vercel
```

### 2. Log in

```powershell
vercel login
```

### 3. Deploy

From the repo root:

```powershell
vercel
```

For production:

```powershell
vercel --prod
```

## API

The deployed frontend calls:

- `GET /api/search?mode=skills&query=python,sql`
- `GET /api/search?mode=summary&query=I have worked with Python and SQL...`

Supported modes:

- `skills`
- `summary`
