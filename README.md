# DRF Menu API Optimization

Implemented the `/api/v1/foods/` endpoint for the restaurant menu.

## Features
*   Using `Prefetch` objects for nested food items.
*   Configuration managed via environment variables using `django-environ` (example of `.env` in `.env.example`).
*   Added tests for the `/api/v1/foods/` endpoint following `test_<function>__<scenario>__<expectation>` naming convention.

## Quick Start

```bash
git clone https://github.com/alxbavy/drf-menu-api-optimization
cd drf-menu-api-optimization

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env

python manage.py migrate
python manage.py test
python manage.py runserver
```

**API Endpoint:** `http://127.0.0.1:8000/api/v1/foods/`