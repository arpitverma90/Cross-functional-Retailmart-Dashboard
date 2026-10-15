# GitHub Setup and Push Guide

This guide walks you through pushing the **RetailMart V3 Enterprise BI Platform** to your GitHub account in 3 minutes.

---

## Quick Push via Git CLI

Open your terminal or PowerShell inside this directory (`retailmart_bi_github`):

```bash
# 1. Initialize git repository
git init

# 2. Add all files
git add .

# 3. Create the initial commit
git commit -m "feat: initial release of RetailMart V3 Enterprise BI Platform"

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
│   ├── services/               # Modular SQL query engine, aggregations, KPIs
│   ├── templatetags/           # Custom template formatters (INR currency, metric tags)
│   ├── tests/                  # Automated test suite (views, auth, services)
│   └── views/                  # Executive, Sales, Customer, Operations, Cross-functional
├── project_documents/          # Architecture, Documentation, Notebooks, and SQL scripts
│   ├── documentation/          # Data dictionary, KPI catalogue, EDA documentation
│   ├── notebooks/              # Jupyter notebooks for profiling and data quality
│   └── sql/                    # Analytical views, database schema, index definitions
├── scripts/                    # Ingestion, validation, and maintenance automation
├── sql/                        # Setup SQL scripts
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

## Security & Cleanliness Checklist

- [x] **No sensitive credentials**: `.env` is excluded; `.env.example` is supplied.
- [x] **No massive binary dumps**: Heavy database dumps (`sql.backup`, 54MB) and raw CSV folders are excluded.
- [x] **No Python caches**: `__pycache__` and `*.pyc` are omitted.
- [x] **Zero clutter**: Scratch scripts and internal logs are omitted.
- [x] **100% self-contained**: Ready to clone, configure `.env`, run migrations, and launch.
