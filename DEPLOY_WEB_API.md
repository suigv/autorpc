# Web/API Only Branch Deployment

This branch contains only server-side API and web console runtime files.

## One-Click Deploy Command (Debian)

```bash
git clone --depth 1 -b web-api-only https://github.com/suigv/autorpc.git demo_py_x64 && cd demo_py_x64 && chmod +x deploy_debian.sh && ./deploy_debian.sh
```

After deployment, open:

- `http://<server-ip>:8000/web`

## Service Management

```bash
sudo systemctl status myt-rpa-api
sudo journalctl -u myt-rpa-api -n 200 --no-pager
sudo systemctl restart myt-rpa-api
```
