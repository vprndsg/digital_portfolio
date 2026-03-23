# Portfolio Foundation

This Flask app is now a portfolio foundation with one live interactive project inside it.

## Routes

- `/` = portfolio homepage
- `/projects/<slug>` = case-study pages for email campaigns, event work, splash pages, product pages, and the biodynamic project
- `/projects/biodynamic-chronicles/live` = the live Biodynamic Chronicles demo
- `/api/forecast` and `/api/journal` = forecast and journal endpoints used by the live demo

## Content structure

- Portfolio content lives in `portfolio_data.py`.
- The live biodynamic forecast logic still lives in `engine.py`.
- The seeded editorial stories for the live biodynamic project live in `editorial.py`.
- `templates/index.html` is the portfolio homepage.
- `templates/project_detail.html` is the case-study template.
- `templates/chronicles.html` is the live biodynamic project page.

## Media

- Portfolio preview art lives in `static/media/`.
- The seeded chronicle stories currently include:
  - one wine write-up
  - one adventure story
  - one photo essay

## Run it

```bash
cd biodynamic_moon_table
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Test

```bash
source .venv/bin/activate
python -m unittest discover -s tests
node --check static/portfolio.js
node --check static/app.js
```

## Notes

- The app ships with its own copy of `de421.bsp`.
- The portfolio pages and the biodynamic demo intentionally use separate templates and client-side scripts so the case-study shell can evolve without breaking the live interactive build.
