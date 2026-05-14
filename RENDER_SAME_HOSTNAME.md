# New Render service and the `pro-ac1o.onrender.com` address

## Important (DNS on Render)

- Each Render **Web Service** gets **one** hostname: `https://<service-name>.onrender.com`.
- **Two services cannot share the same** `*.onrender.com` name. You cannot run a “separate service” and keep **identical** DNS to an existing service at the same time.

So “same DNS” for **`https://pro-ac1o.onrender.com/`** means **that hostname must belong to a single service**.

You have two real options:

---

## Option A — Reuse **`pro-ac1o.onrender.com`** (recommended if you want that exact URL)

1. In [Render Dashboard](https://dashboard.render.com), open the **current** service that already shows URL `pro-ac1o.onrender.com` (or the one you intend to keep that name).
2. **Either fix it in place** (best): connect it to the **fixed GitHub repo/branch**, set **Start** to  
   `gunicorn Annu.wsgi:application --bind 0.0.0.0:$PORT`, fix/remove bad **`DATABASE_URL`**, **Manual Deploy** → **Deploy latest commit**.  
   No new service required.

**OR** if you insist on a **brand‑new** service with the **same** URL:

1. **Delete** (or rename) the old service that currently owns `pro-ac1o.onrender.com` (only if you accept losing that service’s settings/history).
2. **Create** a new **Web Service** and set its **name** to **`pro-ac1o`** so Render issues **`https://pro-ac1o.onrender.com`** again (only works if that name is free after step 1).
3. Connect your **GitHub repo** (with the fixed code: `hero_slides` home template, valid `DATABASE_URL` or none for SQLite).
4. **Do not** paste a truncated Postgres URL. Either omit `DATABASE_URL` or use the **full Internal Database URL** from Render Postgres.
5. Deploy.

---

## Option B — **New** service = **new** URL (true “separate service”)

1. **New** → **Web Service** → pick repo/branch.
2. Pick a **new** service name, e.g. `hmart-ecommerce-live` → public URL becomes  
   `https://hmart-ecommerce-live.onrender.com`  
   (different from `pro-ac1o` — that is normal).

3. If you **own a custom domain** (e.g. `shop.example.com`), you can attach it to this new service under **Settings → Custom Domains** — that is how you reuse **your** DNS, not the built‑in `onrender.com` name.

---

## Quick checklist for a **working** deploy (any service name)

| Setting | Value |
|--------|--------|
| **Build** | `chmod +x build.sh && ./build.sh` |
| **Start** | `gunicorn Annu.wsgi:application --bind 0.0.0.0:$PORT` |
| **SECRET_KEY** | Set (or use Generate in Render). |
| **DEBUG** | `False` (or leave unset on Render; this app defaults safely when `RENDER` is set). |
| **DATABASE_URL** | Omit for SQLite **or** full internal Postgres URL only. |

See also: `DEPLOY_RENDER_PRO_AC1O.md` for the old `pro-ac1o` service checklist.
