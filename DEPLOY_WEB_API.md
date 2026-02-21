# Web/API Only Branch Deployment (Debian)

`web-api-only` is the server-only branch, used for API + Web console deployment.

## Option A: Single Command Remote Install (Recommended)

Run this on a brand-new Debian/Ubuntu server:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/suigv/autorpc/web-api-only/install_debian_webapi.sh)"
```

What it does:

- Installs bootstrap dependencies (`curl`, `git`)
- Clones `web-api-only` branch
- Runs `deploy_debian.sh` automatically

## Option B: Clone + Local Deploy Script

```bash
git clone --depth 1 -b web-api-only https://github.com/suigv/autorpc.git demo_py_x64 && cd demo_py_x64 && chmod +x deploy_debian.sh && ./deploy_debian.sh
```

## Optional Installer Variables

```bash
REPO_URL=https://github.com/suigv/autorpc.git BRANCH=web-api-only TARGET_DIR=demo_py_x64 bash -c "$(curl -fsSL https://raw.githubusercontent.com/suigv/autorpc/web-api-only/install_debian_webapi.sh)"
```

## Optional Deploy Variables

```bash
APP_NAME=myt-rpa-api APP_HOST=0.0.0.0 APP_PORT=8000 PYTHON_BIN=python3 VENV_DIR=.venv ./deploy_debian.sh
```

## Branch Safety

`deploy_debian.sh` validates the current branch and expects `web-api-only` by default.

- Skip check only when needed: `SKIP_BRANCH_CHECK=1 ./deploy_debian.sh`
- Override expected branch: `EXPECTED_BRANCH=web-api-only ./deploy_debian.sh`

## Verify Deployment

- Health API: `curl http://127.0.0.1:8000/health`
- Web console: `http://<server-ip>:8000/web`

## Service Management

```bash
sudo systemctl status myt-rpa-api
sudo journalctl -u myt-rpa-api -n 200 --no-pager
sudo systemctl restart myt-rpa-api
```
