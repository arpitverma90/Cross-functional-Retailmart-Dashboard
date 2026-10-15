# GitHub Setup and Push Guide
## RetailMart V3 Enterprise BI Platform

This guide walks you through pushing the clean **RetailMart V3 Enterprise BI Platform** codebase to your GitHub repository.

---

## Quick Push via Git CLI

Open PowerShell or terminal inside `retailmart_bi_github/`:

```bash
# 1. Initialize git repository
git init

# 2. Stage all files
git add .

# 3. Create initial commit
git commit -m "feat: initial release of RetailMart V3 Enterprise BI Platform (Marketing, Digital, Logistics, Cross-Functional)"

# 4. Set default branch to main
git branch -M main

# 5. Connect your GitHub repository (replace with your repo URL)
git remote add origin https://github.com/<YOUR-USERNAME>/<YOUR-REPO-NAME>.git

# 6. Push to GitHub
git push -u origin main
```

---

## Repository Structure Overview

```text
├── core/                       # Django project configuration, wsgi/asgi, settings
├── dashboard/                  # BI analytics engine: views, services, templates, tests
│   ├── services/               # Marketing, Digital, Logistics, Cross-Functional services
│   ├── templatetags/           # Custom template formatters (INR currency, metric tags)
│   ├── tests/                  # Automated test suite (19 unit & integration tests)
│   └── views/                  # Executive, Marketing, Digital, Logistics, Cross, Simulator
├── project_documents/          # Architecture, Documentation, and Authoritative Deliverables
│   └── documentation/          # Word Doc catalogue, PDF insights report, Markdown catalogues
├── scripts/                    # Query catalogue definitions, docx builders, report generators
├── sql/                        # Materialized views, schema migrations, and index definitions
├── static/                     # Tailwind CSS, Chart styling, ApexCharts controllers
├── templates/                  # Production-ready Jinja/Django dashboard templates
├── .env.example                # Example environment configuration (safe for git)
├── .gitignore                  # Git exclusions (credentials, caches, backups)
├── manage.py                   # Django CLI management script
├── Procfile                    # Production process definition (Gunicorn)
├── requirements.txt            # Python dependencies
├── runtime.txt                 # Python runtime specification (3.13.2)
└── README.md                   # Complete architectural and setup documentation
```

---

## Cleanliness & Security Checklist

- [x] **Strict Domain Scope**: Marketing, Digital, Logistics, and Cross-Functional dashboards only.
- [x] **No sensitive credentials**: `.env` is excluded; `.env.example` is provided.
- [x] **No massive database dumps**: Raw SQL backups and multi-gigabyte data dumps are excluded.
- [x] **No Python caches**: `__pycache__` and `*.pyc` are fully excluded.
- [x] **Self-contained and production-ready**: Ready to clone, configure `.env`, run tests, and launch.
