# Docker, Compose, and local Kubernetes

This project runs as **multiple containers**: Postgres, Django (Gunicorn), and Nginx. Optional **Prometheus + Grafana** run under a Compose profile for metrics and dashboards (all free, local or any VPS with Docker).

## Prerequisites

- [Docker Engine](https://docs.docker.com/engine/install/) and [Docker Compose v2](https://docs.docker.com/compose/) on the host (Windows, Linux, or macOS).

## One-command stack (another PC or your laptop)

From the repository root:

```bash
docker compose up -d --build
```

- **Storefront + API + admin:** [http://localhost:8080](http://localhost:8080) (Nginx → Gunicorn).
- **Health:** [http://localhost:8080/health/live/](http://localhost:8080/health/live/) and [http://localhost:8080/health/ready/](http://localhost:8080/health/ready/) (readiness checks the database).

Create a superuser inside the stack:

```bash
docker compose exec web python manage.py createsuperuser
```

## Observability profile (Prometheus + Grafana)

```bash
docker compose --profile observability up -d --build
```

| Service    | URL                         | Notes                                      |
|-----------|-----------------------------|--------------------------------------------|
| Prometheus | http://localhost:9090      | Scrapes Django `/metrics` (Prometheus client middleware). |
| Grafana    | http://localhost:3001      | Login **admin** / **admin** (change in `docker-compose.yml`). Data source is provisioned automatically. |

Turn off Prometheus in the app only:

```bash
set ENABLE_PROMETHEUS=0
docker compose up -d --build
```

(PowerShell: `$env:ENABLE_PROMETHEUS='0'`.)

Structured **JSON-style** logs on stdout are enabled by default in Compose (`DOCKER_JSON_LOGS=1`) for `docker compose logs -f web`.

## Access from another device on your LAN

Set hosts your browser will use (example IP `192.168.1.50`):

```bash
set ALLOWED_HOSTS=192.168.1.50,localhost,127.0.0.1,web,nginx
set CSRF_TRUSTED_ORIGINS=http://192.168.1.50:8080
docker compose up -d --build
```

Then open `http://192.168.1.50:8080` from other machines (firewall must allow port **8080**).

## Optional env file

Copy `.env.docker.example` to `.env.docker` and adjust, then merge variables into your shell or document them for your team. The Compose file already sets sensible defaults via `environment`.

## Kubernetes (optional, local clusters)

See [k8s/README.md](k8s/README.md) and [k8s/example-stack.yaml](k8s/example-stack.yaml) for a minimal Deployment + StatefulSet Postgres example using the same `Dockerfile`.

## Free-tier cloud with containers

Push the image to **GitHub Container Registry** or **Docker Hub** (free tiers), then run the same image on **Fly.io**, **Render** (Docker deploy), **Railway**, or a small VPS with `docker compose` — keep secrets in the provider’s env UI, not in git.
