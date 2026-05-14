# SDE Take-Home — Submission

## Assignment selected

**Option 1: Easy Level — Basic E-commerce**

Timeline: completed within the stated 7-day window.

## Live demo

- **URL:** `https://pro-ac1o.onrender.com/` *(update after a successful deploy if your service URL differs)*

## Credentials *(fill before sending to the employer)*

| Role | Username | Password |
|------|----------|----------|
| Admin | *(your admin username)* | *(your admin password)* |
| Demo user | *(optional test user)* | *(optional test password)* |

> Create users with `python manage.py createsuperuser` (admin) or register via the storefront (user). Do **not** commit real passwords to git; paste them only in the submission email/form.

## Public repository

- **GitHub:** *(paste your public repo URL after push)*

## What was built (mapping to requirements)

| Requirement | Implementation |
|-------------|----------------|
| Storefront | Django templates: home, product list/detail, cart, auth (login/register), checkout flow; session-backed cart. |
| REST API | Django REST Framework: product CRUD; `POST /api/checkout/simulate/` records an order from the session cart without a payment gateway. |
| Database | Relational schema in `app` models: products, users (Django auth), orders, order line items, plus catalog FKs (category, brand, etc.). |
| Validation / errors | DRF serializers and view validation; Django forms on the HTML side. |
| Deployment | Render-friendly settings (`Procfile`, `render.yaml`, `build.sh`, WhiteNoise, optional `DATABASE_URL`). Frontend and backend are the **same** Django app (acceptable for Option 1); static assets served by the app. |

## Architecture overview

```text
Browser  ──►  Gunicorn + Django (Annu)
                    │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
   Templates    REST API    Admin
   (storefront)  (/api/)    (/admin/)
        │          │
        └────┬─────┘
             ▼
        PostgreSQL or SQLite
        (DATABASE_URL on Render, or local file)
```

- **Presentation:** Django views + AdminLTE-themed templates.
- **Application:** `app` views and business logic; `api` ViewSets and checkout simulation.
- **Data:** Django ORM → Postgres (production) or SQLite (fallback / local demo).

## Database schema (core entities)

High-level entities relevant to the take-home:

- **User** — Django `auth_user` (signup/login via storefront or admin).
- **Product** — catalog fields (name, price, image, FKs to category/brand/color/filter tier, etc.).
- **Order** — shipping/contact fields, `amount`, `payment_id`, `paid`, `status`, `tracking_id`, FK `user`.
- **OrderItems** — line items: `order` FK, `user`, product label, `image`, `quantity`, `price`, `total`.

Full column list is in `app/models.py` and migration files under `app/migrations/`.

## REST API (summary)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/products/` | Public | Paginated product list |
| GET | `/api/products/{id}/` | Public | Product detail |
| POST/PATCH/PUT/DELETE | `/api/products/` … | Staff | Create/update/delete products |
| POST | `/api/checkout/simulate/` | Logged-in user | Create `Order` + `OrderItems` from session cart; clears cart |

Session authentication applies when calling the API from the same browser session as the logged-in site. For scripts, use Basic Auth or session login as appropriate.

## Setup instructions

See **`README.md`**: local `pip install -r requirements.txt`, `migrate`, `createsuperuser`, `runserver`, and Render deploy table (`build.sh`, `gunicorn` with `$PORT`, env vars).

## Trade-offs / notes

- **Single deploy unit:** Option 1 does not require separate Vercel + API hosts; one Django service on Render’s free tier satisfies “deployed frontend & backend” while keeping costs at zero.
- **Simulated checkout:** `payment_id='SIMULATION'` and `paid=True` mark orders created via the API endpoint; Razorpay remains available on the HTML checkout path for a real gateway if configured.
- **SQLite fallback:** If `DATABASE_URL` is missing or invalid, the app logs a warning and uses SQLite so the demo URL still responds; production data should use a valid Render Postgres URL.
