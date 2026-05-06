# Local Setup Guide

This guide gets the full Mentora stack running on your machine so you can build and test skills locally before pushing anything to git.

---

## Prerequisites

Before you start, make sure you have:

- **Python 3.10+** — `python3 --version`
- **Node.js 18+** — `node --version`
- **Git**
- **An Anthropic API key** — get one at [console.anthropic.com](https://console.anthropic.com)

---

## 1 — Folder layout

Clone all repos into the same parent folder. The name of the parent folder doesn't matter.

```
mentora/
├── skills-registry/
├── skills-orchestrator/
├── skills-ui/
└── your-team-repo/        ← your skills repo (e.g. cs270-skills)
```

```bash
mkdir <name of the dicrectory> && cd <name of the directory> 

git clone https://github.com/NUCS338-skills-scaffolding-project/skills-registry.git
git clone https://github.com/NUCS338-skills-scaffolding-project/skills-orchestrator.git
git clone https://github.com/NUCS338-skills-scaffolding-project/skills-ui.git
git clone https://github.com/NUCS338-skills-scaffolding-project/your-team-repo.git
```

---

## 2 — Orchestrator setup

```bash
cd skills-orchestrator

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up your environment file
cp .env.example .env
```

Open `.env` and fill in your API key. You only need one — use whichever provider you have access to:

| Provider | Where to get a key | Model string |
|---|---|---|
| Anthropic | [console.anthropic.com](https://console.anthropic.com) | `claude-sonnet-4-6` |
| OpenAI | [platform.openai.com](https://platform.openai.com) | `openai/gpt-4o` |
| Gemini | [aistudio.google.com](https://aistudio.google.com) | `gemini/gemini-2.0-flash` |

For example, if you're using Gemini:

```
MODEL_PROVIDER=gemini
GEMINI_API_KEY=AI...
DEFAULT_MODEL=gemini/gemini-2.0-flash
```

Everything else works out of the box for local development.

---

## 3 — UI setup

```bash
cd ../skills-ui
npm install
```

No `.env` changes needed for local development.

---

## 4 — Build the catalog

The orchestrator reads skills from `catalog.json` in the skills-registry folder. Build it once before starting:

```bash
cd ../skills-registry
pip install pyyaml          # one-time, if not already installed
python scripts/catalog_builder.py --local ..
```

`..` points at the parent folder — the builder scans every sibling repo (including your team repo), validates all `skills.md` files, and writes `catalog.json` here. No GitHub token or account needed for this step.

Check the output for any validation errors:

```bash
cat build_report.md
```

---

## 5 — Run the stack

You need two terminals, both with the virtual env active, if you are using one.

**Terminal 1 — Orchestrator**

```bash
cd skills-orchestrator
source .venv/bin/activate
uvicorn app.main:app --port 8080 --reload
```

**Terminal 2 — UI**

```bash
cd skills-ui
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 6 — Testing your skills locally

As you write and edit skills, you don't need to push to git to test them. The loop is:

```
edit skills.md  →  rebuild catalog  →  reload orchestrator  →  test in UI
```

**Rebuild the catalog** (from `skills-registry/`):

```bash
python scripts/catalog_builder.py --local ..
```

**Reload the orchestrator** (no restart needed):

```bash
curl -X POST http://localhost:8080/registry/refresh \
  -H "Authorization: Bearer changeme-dev-token"
```

Your updated skill is now live in the UI.

For more detail on the local skill workflow, see [skills-registry/README.md](../skills-registry/README.md).

---

## 7 — Push when ready

Once your skill is working locally, push your team repo to git. The catalog rebuilds automatically within ~1 minute via the webhook, and your skill becomes available to everyone.

For the full skill authoring guide, see [Team-Guide.md](./Team-Guide.md).
