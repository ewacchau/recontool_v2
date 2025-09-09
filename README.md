# ReconTool — Automated Enumeration Web App

ReconTool is a lightweight Flask application that automates common reconnaissance tasks and stores the results in a relational database.

Goals:
- Simplicity: run with a single docker-compose up or a local venv.
- Modularity: each recon stage is a swappable helper.
- Secure defaults: CSRF, rate limiting, no secrets in source.
- Learnability: small, easy-to-read codebase (~300 LOC).

## Stack

| Component | Reason |
|-----------|--------|
| Flask 3 | Minimal, batteries-included web framework |
| SQLAlchemy + Postgres/SQLite | Persist scan runs & JSON results |
| Celery + Redis | Offload long-running scans asynchronously |
| WTForms / Flask-WTF | Secure form handling, built-in CSRF |
| Flask-Limiter | Prevent abuse (30 req/min, 10 scans/min) |
| Docker Compose | One-command reproducible dev env |

## Project layout
```text
.
├─ docker-compose.yml
├─ Dockerfile
├─ manage.py
├─ requirements.txt
├─ .env.example
├─ app/
│  ├─ __init__.py
│  ├─ config.py
│  ├─ extensions.py
│  ├─ models.py
│  ├─ utils.py
│  ├─ tasks.py
│  └─ scans/
│     ├─ __init__.py
│     ├─ routes.py
│     └─ forms.py
└─ app/templates/
   ├─ layout.html
   ├─ index.html
   ├─ status.html
   └─ results.html
```

## Quick start (Docker)

```bash
cp .env.example .env                    # fill in SECRET_KEY, etc.
docker-compose up --build               # builds web + worker + redis + db
docker-compose exec web flask db upgrade  # apply DB migrations
Open http://localhost:5000 in your browser
```

## Quick start (local venv)

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env                    # edit for local (see comments)
redis-server &                          # start redis locally
flask db upgrade                        # create DB (SQLite default)
flask --app manage.py run &             # start web
celery -A app.extensions.celery worker --loglevel=info &
```

Note: The Docker image installs recon tools (nmap, amass, Sublist3r, theHarvester). In a local venv, those tools are not installed by default; tasks will gracefully skip missing tools. You can install them manually if desired.

## Configuration

The app supports environment-based config classes in `app/config.py`:
- `DevelopmentConfig`: Debug-friendly defaults.
- `ProductionConfig`: Secure cookies and https scheme; requires `SECRET_KEY`.

Select a config class via env var:
- `APP_CONFIG=app.config.ProductionConfig`

### Environment variables

| Var | Default | Notes |
|-----|---------|-------|
| `SECRET_KEY` | `changeme` (dev), required in prod | Replace before prod |
| `DATABASE_URL` | `sqlite:///recon.db` | Use Postgres for multi-user |
| `SHODAN_API_KEY` | _none_ | Optional Shodan enrichment |
| `CELERY_BROKER_URL` | `redis://redis:6379/0` | Broker (Docker default) |
| `CELERY_RESULT_BACKEND` | same as broker | Results backend |
| `RATELIMIT_STORAGE_URI` | `redis://redis:6379/1` | Persistent rate limits |
| `SESSION_COOKIE_SAMESITE` | `Lax` | Cookie setting |
| `SESSION_COOKIE_SECURE` | `false` (prod sets true) | Set `true` behind TLS |
| `REMEMBER_COOKIE_SECURE` | `false` (prod sets true) | Set `true` behind TLS |

## How it works

1. User submits a domain/IP on `/`.
2. A `ScanRun` row (`pending`) is created.
3. Celery picks the job, sets `running`, and executes recon tools.
4. Results are saved as JSON into the database, status becomes `finished`.
5. The UI polls `/status/<id>` and then links to `/results/<id>`.

## Notes on storage types

- The `ScanRun.result` column uses a portable `JSON` type for compatibility with SQLite and Postgres.
- For high-concurrency or advanced querying, consider Postgres JSONB via a migration.

## Security considerations

- CSRF enabled on all forms.
- Redis-backed rate limiting for reliable, shared limits across processes.
- Secrets via `.env`, never committed.
- Command execution uses `utils.run_cmd` with timeouts and return-code checks.
- Consider an explicit consent checkbox before launching scans in production.

## Extending

- Add a new recon step in `app/tasks.py` and merge output into `results`.
- Swap meta refresh in `status.html` for SSE/WebSocket for realtime updates.
- Use `APP_CONFIG` to select different configs per environment.

## Recon tools included (Docker image)

- nmap (via apt)
- amass (downloaded latest release)
- Sublist3r (pip)
- theHarvester (pip)

## License

MIT (see `LICENSE`).
