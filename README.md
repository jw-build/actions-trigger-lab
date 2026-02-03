# actions-trigger-lab

Trigger GitHub Actions via `workflow_dispatch` and `repository_dispatch` (PAT or GitHub App). Protocol v1: `action` / `env` / `request_id` with allowlist.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
source local.env
python3 dispatch_via_app.py
```
