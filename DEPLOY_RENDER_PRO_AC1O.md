# Deploy so https://pro-ac1o.onrender.com/ works

Your Render service is still running **old code** (error at `index.html` line 213 with `{{ product.0 }}`) and/or a **broken Postgres URL**. Fix both in the Render dashboard and redeploy.

## 1. Point the service at code that includes the fixes

In Render: **Web Service `pro-ac1o`** (or whatever it is named) → **Settings** → **Build & Deploy**:

- **Repository**: the GitHub repo that contains **this** project (with `hero_slides` in `HOME` and `Template/Main/index.html` using `{% for hero in hero_slides %}`).
- **Branch**: usually `main`.
- Click **Manual Deploy** → **Deploy latest commit** after your GitHub branch has the fixes.

If the repo is not updated, push your local project:

```powershell
cd c:\work\Adam\ECOMMERCE-PROJECT-
git remote -v
git push origin main
```

Use an account that **has push access** to that repository.

## 2. Fix or remove `DATABASE_URL` (critical)

**Dashboard** → **Environment** → **Environment Variables**:

- If `DATABASE_URL` looks like `postgres://...@dpg-xxxxx-a` **without** `.render.com` (or similar) on the host, it is **truncated**. Either:
  - **Delete** `DATABASE_URL` (the app will use **SQLite** and the site will load), or  
  - Replace it with the **full Internal Database URL** from your Render PostgreSQL instance (host must look like `dpg-xxxxx-a.something.postgres.render.com`).

Newer versions of this project **ignore** an invalid Postgres URL and fall back to SQLite, but that only helps **after** that version is deployed.

## 3. Start command (public URL)

**Settings** → **Start Command**:

```text
gunicorn Annu.wsgi:application --bind 0.0.0.0:$PORT
```

**Build Command**:

```text
chmod +x build.sh && ./build.sh
```

## 4. Host / DNS (`pro-ac1o.onrender.com`)

Render already gives you DNS: **`https://pro-ac1o.onrender.com`**. You do **not** configure DNS yourself for that hostname.

If you ever see **DisallowedHost**, add an environment variable (comma-separated is allowed):

| Name | Value |
|------|--------|
| `ALLOWED_HOSTS` | `pro-ac1o.onrender.com` |

The app also uses `RENDER_EXTERNAL_HOSTNAME` when Render sets it; the above is a backup.

## 5. After deploy

Open **https://pro-ac1o.onrender.com/** again. On the free tier, the first load after idle can take **30–60 seconds**.

If it still fails, open **Logs** in Render and copy the **build** log and the **runtime** error (last 50 lines) for troubleshooting.
