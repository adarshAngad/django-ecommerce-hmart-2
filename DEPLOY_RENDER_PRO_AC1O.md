# Deploy so https://pro-ac1o.onrender.com/ works

Your Render service is still running **old code** (error at `index.html` line 213 with `{{ product.0 }}`) and/or a **broken Postgres URL**. Fix both in the Render dashboard and redeploy.

## 0. Push from this PC when `git push` returns 403

If `git push origin main` says **Permission denied** (for example your Git credential is **AdarshAg727** but `origin` is **amaanc986/...**), pick one:

1. **Add your GitHub user as a collaborator** on `amaanc986/ECOMMERCE-PROJECT-` (repo Settings → Collaborators), then push again with `git push origin main`, or  
2. **Push with a PAT** for an account that owns or can push to that repo. In PowerShell from the repo root:

   ```powershell
   .\scripts\Push-WithGitHubToken.ps1
   ```

   Create a [classic PAT](https://github.com/settings/tokens) with **repo** scope. Set it only for the session (it is not stored in the repo):

   ```powershell
   $env:GITHUB_TOKEN = 'ghp_xxxxxxxx'
   .\scripts\Push-WithGitHubToken.ps1
   ```

3. **Change `origin`** to a repo under your user (create an empty public repo first), then push and point Render at that repo instead.

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

## 6. “Separate service” but same `pro-ac1o.onrender.com`

Render only allows **one** service to use a given `*.onrender.com` name. See **`RENDER_SAME_HOSTNAME.md`** for Option A (fix or replace the existing service) vs Option B (new URL).
