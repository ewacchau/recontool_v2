# ReconTool – Automated Enumeration Web App

**ReconTool** is a lightweight Flask application that automates common reconnaissance tasks and stores the results in a relational database. Its goals are:

* **Simplicity** – run it with a single `docker-compose up` or local venv.
* **Modularity** – each recon stage is a standalone helper you can swap out.
* **Security‑minded defaults** – CSRF, rate‑limiting, and no secrets in source.
* **Learnability** – small, annotated codebase (~300 LOC) ideal for study.

## Stack

| Component | Reason |
|-----------|--------|
| Flask 3   | Minimal, batteries‑included web framework |
| SQLAlchemy + PostgreSQL (or SQLite) | Persist scan runs & JSON results |
| Celery + Redis | Off‑load long‑running scans asynchronously |
| WTForms / Flask‑WTF | Secure form handling, built‑in CSRF |
| Flask‑Limiter | Prevent abuse (30 req/min, 10 scans/min) |
| Docker Compose | One‑command reproducible dev env |

## Project layout
```text
.
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── requirements.txt
├── .env.example
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── models.py
│   ├── utils.py
│   ├── tasks.py
│   ├── scans/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── forms.py
│   └── templates/
│       ├── layout.html
│       ├── index.html
│       ├── status.html
│       └── results.html
└── README.md
```

## Quick start (Docker)

```bash
cp .env.example .env           # fill in SECRET_KEY, SHODAN_API_KEY, etc.
docker-compose up --build      # builds web + worker + redis + db
docker-compose exec web flask db upgrade  # apply DB migrations
open http://localhost:5000
```

## Quick start (local venv)

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env           # edit secrets
redis-server &                 # start redis locally
flask db upgrade               # create DB (SQLite default)
flask --app manage.py run &    # start web
celery -A app.extensions.celery worker --loglevel=info &
```

## Environment variables

| Var | Default | Notes |
|-----|---------|-------|
| `SECRET_KEY` | `changeme` | Replace before prod |
| `DATABASE_URL` | `sqlite:///recon.db` | Use Postgres for multiuser |
| `SHODAN_API_KEY` | _none_ | Optional Shodan enrichment |
| `CELERY_BROKER_URL` | `redis://redis:6379/0` | Broker |
| `CELERY_RESULT_BACKEND` | same as broker | Results |

## How it works

1. User submits a domain/IP ➜ `/`
2. `ScanRun` row (`pending`) created.
3. Celery picks job ➜ `running`, executes recon tools.
4. Results dict saved as JSONB ➜ `finished`.
5. Front‑end polls `/status/<id>` then links to `/results/<id>`.

## Security considerations

* **CSRF enabled** on all forms.
* **Rate limiting** to mitigate abuse.
* **Secrets** via `.env`, never committed.
* **Command execution** uses whitelist (`utils.run_cmd`) with timeouts.
* **Consent** checkbox recommended before launching scans in prod.

## Extending

* Add new recon step in `tasks.py` and merge output into `results`.
* Drop‑in replacement for DB (`DATABASE_URL`) or broker (`CELERY_BROKER_URL`).
* Swap meta refresh in `status.html` for SSE/WebSocket for realtime streams.

## License

MIT (see `LICENSE`).
