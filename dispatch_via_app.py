"""
用 GitHub App 触发 repository_dispatch（替代 PAT）。
需要环境变量：APP_ID, OWNER, REPO, PRIVATE_KEY_PEM
"""
import os
import time
import json
import jwt  # PyJWT
import requests

APP_ID = os.environ["APP_ID"]
OWNER = os.environ["OWNER"]
REPO = os.environ["REPO"]
PEM = os.environ["PRIVATE_KEY_PEM"]

with open(PEM, "r", encoding="utf-8") as f:
    private_key = f.read()

now = int(time.time())
payload = {
    "iat": now - 60,
    "exp": now + 600,
    "iss": APP_ID,
}

app_jwt = jwt.encode(payload, private_key, algorithm="RS256")

# 1) 找到安装在该 repo 的 installation id
headers = {
    "Authorization": f"Bearer {app_jwt}",
    "Accept": "application/vnd.github+json",
}
r = requests.get(f"https://api.github.com/repos/{OWNER}/{REPO}/installation", headers=headers)
r.raise_for_status()
installation_id = r.json()["id"]

# 2) 用 installation id 换 installation access token
r = requests.post(
    f"https://api.github.com/app/installations/{installation_id}/access_tokens",
    headers=headers,
)
r.raise_for_status()
inst_token = r.json()["token"]

# 3) 用 installation token 触发 repository_dispatch
headers2 = {
    "Authorization": f"Bearer {inst_token}",
    "Accept": "application/vnd.github+json",
}
body = {
    "event_type": "dispatch",
    "client_payload": {
        "action": "ping",
        "env": "dev",
        "request_id": "req-001",
    },
}
r = requests.post(
    f"https://api.github.com/repos/{OWNER}/{REPO}/dispatches",
    headers=headers2,
    data=json.dumps(body),
)
if r.status_code != 204:
    print(f"HTTP {r.status_code}: {r.text}")
r.raise_for_status()
print("OK: dispatched (Protocol v1)")
