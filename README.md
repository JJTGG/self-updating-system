# Self-Updating System

A configurable, continuously updating data pipeline with automated tests, CI/CD, changelog automation, and bounded self-repair.

## What it does

1. Fetches data from `DATA_SOURCE_URL` every 30 minutes using GitHub Actions.
2. Validates and normalizes the response.
3. Writes a timestamped snapshot and a stable `data/latest.json`.
4. Runs the full test suite before deployment.
5. Appends a structured entry to `CHANGELOG.md`.
6. On failure, opens a GitHub Issue containing diagnostics; optionally generates a repair PR via the `self-repair` workflow.

## Honest scope

- The system can run on a schedule indefinitely **while the repository, runner, secrets, and external source remain healthy**.
- GitHub disables public-repository scheduled workflows after 60 days without repository activity; use a private repo, periodic commits/releases, or an external scheduler if uninterrupted operation is critical.
- "Zero bugs" is enforced as a quality gate, not a mathematical guarantee.
- Automated repair creates a reviewed pull request; it does not force-push unreviewed changes to `main`.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
pytest
python -m app.run_once
```

## Required repository secrets

| Secret | Purpose |
|---|---|
| `DATA_SOURCE_URL` | JSON API endpoint to fetch |
| `GITHUB_TOKEN` | Automatically provided by Actions; needs `issues: write` and `contents: write` |
| `OPENAI_API_KEY` | Optional; enables LLM-assisted repair PRs |

## Configuration

Edit `config/system.json` to change the schedule, output paths, validation rules, and repair behavior.

## Deployment

The default deployment target is GitHub Pages. The deploy workflow publishes `site/` after tests pass. Replace `.github/workflows/deploy.yml` for Vercel, Fly.io, Render, or another target.
