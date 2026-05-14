# Run your own server with your own DNS name

## What you cannot do

**`https://pro-ac1o.onrender.com/`** is a hostname that **only Render** can serve. You cannot point that exact name at your own VPS or Docker host. “Same DNS” in practice means: **you pick a name you control** (a domain or free subdomain) and use that instead.

## What you can do

1. Rent a small **VPS** (e.g. [Hetzner](https://www.hetzner.com/cloud), [DigitalOcean](https://www.digitalocean.com/), [Oracle Cloud free tier](https://www.oracle.com/cloud/free/), or any Linux VM with a **public IPv4**).
2. Create a **DNS name** you control:
   - **Your domain:** add an **A record** `shop.example.com` → your VPS public IP.
   - **Free subdomain:** e.g. [DuckDNS](https://www.duckdns.org/) → `yourname.duckdns.org` → same A record.
3. On the VPS, install [Docker](https://docs.docker.com/engine/install/) + [Docker Compose](https://docs.docker.com/compose/install/).
4. Clone this repo, configure **`.env.vps`**, and start the **VPS stack** (Postgres + Django + **Caddy** for automatic HTTPS).

## Quick start (VPS)

```bash
sudo apt update && sudo apt install -y git
git clone https://github.com/adarshAngad/django-ecommerce-hmart-2.git
cd django-ecommerce-hmart-2
cp .env.vps.example .env.vps
nano .env.vps   # set SITE_DOMAIN, SECRET_KEY, POSTGRES_PASSWORD
```

**Wait until DNS has propagated** (A record points to this server). Then:

```bash
docker compose -f docker-compose.vps.yml --env-file .env.vps up -d --build
```

Open **`https://<SITE_DOMAIN>`** (Caddy obtains a Let’s Encrypt certificate automatically).

First admin user:

```bash
docker compose -f docker-compose.vps.yml --env-file .env.vps exec web python manage.py createsuperuser
```

## Firewall

Allow inbound **80** and **443** (and **22** for SSH):

```bash
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## Files involved

| File | Role |
|------|------|
| `docker-compose.vps.yml` | Postgres, Django, Caddy (no Render). |
| `.env.vps.example` | Template for `SITE_DOMAIN`, secrets. |
| `Dockerfile` | Same app image as local Docker. |

## Optional: keep using Render too

You can run **Render** (`*.onrender.com`) for one audience and **your VPS** for another URL — two deployments, two DNS names, same codebase from GitHub.
