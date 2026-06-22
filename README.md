# Pour Decisions 🍸

> A field guide to bad nights and worse decisions.

**Live:** https://pour-decisions.onrender.com

Pour Decisions is a humor-driven online magazine where people anonymously share their most chaotic, weird, and regrettable nights out — written up like official police **incident reports** and rated by the community on an animated **Breathalyzer** gauge. Built as a full-stack portfolio project.

---

## ⚠️ Disclaimer

Pour Decisions exists purely for **entertainment**. It does **not** encourage or endorse drinking — least of all to excess — and is intended only as a place to laugh at the stories we tell *after* the fact. The site is strictly **18+**.

The spirit of the project: *we all make pour decisions, and that doesn't make us bad people.* But please look after yourselves and each other. If the nights have stopped being funny, South Africa's SADAG runs a free, confidential, 24-hour Substance Abuse Helpline: **0800 12 13 14** (or SMS 32312).

---

## Features

- **Incident-report submissions** — file a story as an official police report: report number, Subject (alias, defaults to *Anonymous*), optional mugshot (5 MB cap), classification, drinks, and an "Officer's Assessment" of Chaos, Memory, Regret, and Lesson Learned.
- **The Breathalyzer** — an animated SVG gauge where the community rates each story from *Tipsy* to *Legendary* (1–100). AJAX-powered, one vote per session.
- **Story of the Week** — the highest-rated report is auto-featured on a full-width hero (using the poster's own photo, or a fallback banner).
- **Three colour-coded categories** — Funny, Weird, Horrific.
- **Magazine feed** — a hierarchical, scroll-revealing grid with live search, category filters, a "Spin the Bottle" random-story button, and an animated scroll cue.
- **Moderation** — every story is reviewed in the Django admin before going live (approve/reject queues + bulk actions).
- **18+ age gate** — enforced site-wide by custom middleware.
- **Strict House Rules** — a required consent step and a hard rule against posting anyone's photo without permission.
- **Auto-seeded demo content** — 21 demo stories, plus categories and companion options, seed themselves via reversible data migrations on first `migrate`.

---

## Tech Stack

| Layer | Tech |
|---|---|
| Backend | Django 5.2, Python 3.13 |
| Database | SQLite (dev) · PostgreSQL / Neon (prod) |
| Static files | WhiteNoise |
| App server | Gunicorn |
| Hosting | Render |
| Frontend | Vanilla JavaScript, SVG, CSS custom properties (no framework) |

Notable implementation details: custom request middleware (age gate), session-based anonymous rating backed by a database uniqueness constraint, an AJAX rating endpoint with CSRF protection, an animated SVG gauge, `IntersectionObserver` scroll reveals, server-side search with `Q` objects, and reversible data migrations for seeding.

---

## Design

The whole UI is themed as a **police case file inside an editorial magazine**:

- **Typography:** Playfair Display (editorial serif) for headlines; Special Elite (typewriter) for the "official" form text.
- **Texture & colour:** a subtle paper grain (inline SVG noise), category colour-coding, and rubber-stamp accents.
- **Jargon over generic UI:** you "file an incident report," not "submit a post"; you "blow into the Breathalyzer," not "leave a rating."

---

## Local Setup

```bash
# 1. Clone
git clone https://github.com/Tlotlo28/pour-decisions.git
cd pour-decisions

# 2. Virtual environment (Python 3.13)
py -3.13 -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
```

Generate a secret key with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Then set up the database and run:

```bash
python manage.py migrate          # also seeds categories, companions, and 21 demo stories
python manage.py createsuperuser
python manage.py runserver
```

Visit **http://127.0.0.1:8000/**.

---

## Deployment (Render + Neon)

- **Build command:**
  ```
  pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate && (python manage.py createsuperuser --noinput || true)
  ```
- **Start command:** `gunicorn pourdecisions.wsgi:application`
- **Environment variables:** `SECRET_KEY`, `DEBUG=False`, `DATABASE_URL` (Neon connection string), `ALLOWED_HOSTS=.onrender.com`, `CSRF_TRUSTED_ORIGINS=https://*.onrender.com`, plus `DJANGO_SUPERUSER_USERNAME` / `DJANGO_SUPERUSER_EMAIL` / `DJANGO_SUPERUSER_PASSWORD`.

---

## Roadmap

- [ ] Cloudflare R2 for persistent user-uploaded mugshots
- [ ] Hall of Shame — an all-time leaderboard of the most chaotic reports
- [ ] Optional user accounts for editing your own filings

---

## Author

**Tlotlo "Modisa" Masisi** — GitHub [@Tlotlo28](https://github.com/Tlotlo28)

## License

© 2026 Tlotlo Masisi. All rights reserved.

This code is public for viewing and evaluation as part of my portfolio.
You're welcome to explore it and run it locally. It is not licensed for
reuse, redistribution, or commercial use without my written permission.
