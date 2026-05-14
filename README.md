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

## Deploy on Render

- **Build command:** `chmod +x build.sh && ./build.sh`
- **Start command:** `gunicorn Annu.wsgi:application`
- Set **`SECRET_KEY`**, **`DEBUG=False`**, and optional **`DATABASE_URL`** (Render PostgreSQL).
- **PostgreSQL:** In the Render dashboard, copy the **Internal Database URL** in full (it must end with `.render.com` or similar). If you paste a truncated value, you will see errors like `could not translate host name "dpg-..."`.
- If Postgres fails SSL on a non-Render host, set **`DATABASE_SSL_REQUIRE=False`**.
- Optional: **`RAZORPAY_KEY_ID`**, **`RAZORPAY_KEY_SECRET`**, **`EMAIL_HOST_USER`**, **`EMAIL_HOST_PASSWORD`** for email.

SQLite works for quick tests; use Render Postgres for data that must survive redeploys.
