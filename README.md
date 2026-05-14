# Django eCommerce Website

Online shop built with Django: catalog, cart, checkout, Razorpay payments, and admin.

## SDE take-home (Option 1 — Basic e-commerce)

This repository is structured for **Option 1** of the take-home: storefront + REST API + relational data + free-tier deployment. A short submission checklist (demo URL, credentials placeholders, architecture, schema) lives in **`SUBMISSION.md`**.

### REST API (Django REST Framework)

After `pip install -r requirements.txt` and `runserver`, base path: **`/api/`**

| Method | Path | Notes |
|--------|------|--------|
| GET | `/api/products/` | Paginated list (public) |
| GET | `/api/products/{id}/` | Detail (public) |
| POST, PUT, PATCH, DELETE | `/api/products/`, `/api/products/{id}/` | Staff only |
| POST | `/api/checkout/simulate/` | Authenticated: creates an order from the **session cart** (no payment); clears the cart |

Use a logged-in browser session against the same origin, or Basic Auth for quick API tests.

## Local setup

1. Create a virtual environment and install dependencies:

   `pip install -r requirements.txt`

2. Run migrations:

   `python manage.py migrate`

3. Create an admin user:

   `python manage.py createsuperuser`

4. Run the server:

   `python manage.py runserver`

5. Open `http://127.0.0.1:8000/`

## Docker Compose and Kubernetes (multi-service, observability)

For a **containerized** stack you can copy to another machine or VPS (Postgres + Django + Nginx; optional Prometheus + Grafana), see **[DOCKER.md](DOCKER.md)**. Quick start:

`docker compose up -d --build` then open **http://localhost:8080**. Optional metrics stack: `docker compose --profile observability up -d --build`.

Minimal **Kubernetes** manifests live under **`k8s/`** (local clusters such as kind, minikube, or Docker Desktop Kubernetes).

## Your own server and DNS (not Render)

You **cannot** reuse **`pro-ac1o.onrender.com`** on a private VPS (Render owns that hostname). To run your own stack with **your** DNS name (domain or DuckDNS), see **[SELF_HOSTED.md](SELF_HOSTED.md)** and use **`docker-compose.vps.yml`** with **`.env.vps`**.

## Free cloud — Render (open from any phone or PC)

You do **not** install Python on other people’s devices. Render runs the app; they only open an `https://….onrender.com` link.

### New deploy from this repo (recommended)

1. Sign up at **[render.com](https://render.com)** with **GitHub**.
2. **New +** → **Blueprint** → connect **`adarshAngad/django-ecommerce-hmart-2`** (branch **`main`**).
3. Render reads **`render.yaml`**: it creates a **free Web Service** + **free PostgreSQL** (Oregon) and wires **`DATABASE_URL`** automatically.
4. Wait until the first deploy is **Live**. Open the **URL** shown on the service (e.g. `https://django-ecommerce.onrender.com` — the name comes from `render.yaml`).
5. Optional: **GitHub → Settings → Secrets → Actions** add **`RENDER_DEPLOY_HOOK_URL`** from Render (**Manual Deploy → Deploy hook**). Then every **`git push`** to **`main`** can trigger **[`.github/workflows/render-deploy.yml`](.github/workflows/render-deploy.yml)**.

Free Postgres on Render is for trials and **expires after 30 days** unless you upgrade ([changelog](https://render.com/changelog/free-postgresql-instances-now-expire-after-30-days-previously-90-days)).

### Already have a service (e.g. `pro-ac1o`)

Use **`PRO_AC1O_OPEN_THIS_URL.txt`**: connect the same GitHub repo, fix env vars, **Manual Deploy**.

## Deploy on Render (public URL)

Your service URL will look like `https://YOUR-SERVICE.onrender.com`. Anyone with the link can open it after a successful deploy.

### Render settings

| Field | Value |
|--------|--------|
| **Build command** | `chmod +x build.sh && ./build.sh` |
| **Start command** | `gunicorn Annu.wsgi:application --bind 0.0.0.0:$PORT` |

The **`$PORT`** binding is required so Render can route traffic from the internet to your app.

### Environment variables

| Variable | Required | Notes |
|----------|------------|--------|
| `SECRET_KEY` | Yes (production) | Long random string; Render can generate one. |
| `DEBUG` | Recommended `False` | If unset on Render, this project defaults to **False** when the `RENDER` env is present. |
| `DATABASE_URL` | Optional | Use the **full Internal Database URL** from your Render Postgres (hostname must contain a **dot**, e.g. `....oregon-postgres.render.com`). A truncated URL is ignored and the app falls back to **SQLite** so the site still starts. |
| `DATABASE_SSL_REQUIRE` | Optional | Default `True` for Postgres. Set `False` only if your provider needs it. |

Also set Razorpay / email variables if you use those features (see earlier sections).

### After deploy

- Open your **Render dashboard → your Web Service → URL** (or the custom domain you attach).
- First request after idle may take ~30–60 seconds on the free tier (cold start).

SQLite on a web service is fine for demos; use Render Postgres for data you need to keep across deploys.

**Deploying to `https://pro-ac1o.onrender.com/`:** follow `DEPLOY_RENDER_PRO_AC1O.md` (repo, `DATABASE_URL`, start command with `$PORT`, redeploy).

**Same hostname vs new service:** read `RENDER_SAME_HOSTNAME.md`.

**New GitHub repo under your account (no `gh login`):** create a [classic PAT](https://github.com/settings/tokens) with **repo** scope, then from the repo root:

```powershell
$env:GITHUB_TOKEN = "ghp_xxxxxxxx"
.\scripts\Create-OwnGithubRepo-ApiAndPush.ps1 -RepoName "django-ecommerce-hmart"
```

That creates `https://github.com/<you>/django-ecommerce-hmart`, saves the old `origin` as `upstream`, and pushes `main`. Connect **that** repo in Render.
