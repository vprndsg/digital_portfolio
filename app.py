from __future__ import annotations

from datetime import date

from flask import Flask, abort, jsonify, render_template, request, url_for

from editorial import BLOG_ENTRIES
from engine import (
    build_experience,
    normalize_appetite,
    normalize_bottle_profile,
    normalize_custom_bottle,
    normalize_party_mode,
    parse_date,
)
from journal_store import build_snapshot, init_db, save_entry
from portfolio_data import (
    OWNER,
    PROJECTS,
    SIGNAL_STATS,
    get_project,
    get_related_projects,
)


app = Flask(__name__)
init_db()


def build_page_state(args):
    experience = build_experience_state(args)
    experience["journal"] = build_snapshot()
    return experience


def build_experience_state(args):
    requested_day = parse_date(args.get("date"))
    party_mode = normalize_party_mode(args.get("party"))
    appetite = normalize_appetite(args.get("appetite"))
    bottle_profile = normalize_bottle_profile(args.get("bottle"))
    custom_bottle = normalize_custom_bottle(args)
    return build_experience(requested_day, party_mode, appetite, bottle_profile, custom_bottle)


def format_american_date(value: str) -> str:
    return date.fromisoformat(value).strftime("%m/%d/%Y")


def build_blog_entries_json():
    return [
        {
            **entry,
            "media": [
                {
                    **media,
                    "image": url_for("static", filename=media["image"]),
                }
                for media in entry["media"]
            ],
        }
        for entry in BLOG_ENTRIES
    ]


def homepage_projects():
    featured_order = (
        "harvest-weekend-email-system",
        "asado-vineyard-dinner",
        "bitter-orange-lambrusco-pdp",
    )
    featured = [project for slug in featured_order if (project := get_project(slug))]
    remaining = [
        project
        for project in PROJECTS
        if project["slug"] not in featured_order and project["slug"] != "biodynamic-chronicles"
    ]
    return [*featured, *remaining]


@app.get("/")
def portfolio_home():
    forecast_state = build_experience_state(request.args)
    featured_project = get_project("biodynamic-chronicles")
    header_forecast = [
        {
            **item,
            "display_date": format_american_date(item["date"]),
        }
        for item in forecast_state["week_horizon"]["nights"][:3]
    ]
    return render_template(
        "index.html",
        owner=OWNER,
        projects=homepage_projects(),
        signal_stats=SIGNAL_STATS,
        featured_project=featured_project,
        header_forecast=header_forecast,
    )


@app.get("/projects/biodynamic-chronicles/live")
@app.get("/labs/biodynamic-chronicles")
def chronicles_live():
    initial_state = build_page_state(request.args)
    project = get_project("biodynamic-chronicles")
    return render_template(
        "chronicles.html",
        initial_state=initial_state,
        blog_entries=BLOG_ENTRIES,
        blog_entries_json=build_blog_entries_json(),
        project=project,
        site_config={
            "mode": "api",
            "forecast_api_path": url_for("forecast_api"),
            "time_zone": "America/Los_Angeles",
        },
    )


@app.get("/projects/<slug>")
def project_detail(slug):
    project = get_project(slug)
    if project is None:
        abort(404)
    return render_template(
        "project_detail.html",
        owner=OWNER,
        project=project,
        related_projects=get_related_projects(slug),
    )


@app.get("/api/forecast")
def forecast_api():
    return jsonify(build_page_state(request.args))


@app.get("/api/journal")
def journal_api():
    limit = request.args.get("limit", type=int) or 8
    return jsonify(build_snapshot(limit=max(1, min(limit, 24))))


@app.post("/api/journal")
def journal_save_api():
    payload = request.get_json(silent=True) or {}
    entry = save_entry(payload)
    return jsonify({"saved": entry, "journal": build_snapshot()})


@app.get("/health")
def health():
    return "OK"


if __name__ == "__main__":
    app.run(debug=True)
