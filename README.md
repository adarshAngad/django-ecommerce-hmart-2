# Django eCommerce Website

Online shop built with Django: catalog, cart, checkout, Razorpay payments, and admin.

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

**Deploying to `https://pro-ac1o.onrender.com/`:** follow the checklist in `DEPLOY_RENDER_PRO_AC1O.md` (connect repo, fix `DATABASE_URL`, start command with `$PORT`, redeploy).

**New GitHub repo + push:** install GitHub CLI (`winget install GitHub.cli`), run `gh auth login` once, then from the repo root:

`.\scripts\Create-GitHubRepoAndPush.ps1 -RepoName "django-hmart-store"`

Or set `$env:GITHUB_TOKEN` to a [classic PAT](https://github.com/settings/tokens) with **repo** scope and run the same script (no browser).
