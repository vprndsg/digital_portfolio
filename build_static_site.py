from __future__ import annotations

import copy
import json
import posixpath
import shutil
from calendar import monthrange
from datetime import date, datetime
from pathlib import Path, PurePosixPath

from jinja2 import Environment, FileSystemLoader, select_autoescape
from jinja2.utils import htmlsafe_json_dumps
from markupsafe import Markup

from editorial import BLOG_ENTRIES
from engine import LOS_ANGELES, build_experience, normalize_appetite, normalize_party_mode
from portfolio_data import (
    OWNER,
    PROJECTS,
    SIGNAL_STATS,
    get_project,
    get_related_projects,
)


BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "docs"
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

DEFAULT_PARTY_MODE = normalize_party_mode(None)
DEFAULT_APPETITE = normalize_appetite(None)
PARTY_MODES = ("solo", "pair", "crowd")
APPETITES = ("comfort", "electric", "curious")


def tojson_filter(value):
    return Markup(htmlsafe_json_dumps(value, separators=(",", ":")))


env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=select_autoescape(["html", "xml"]),
)
env.filters["tojson"] = tojson_filter


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


def route_target(endpoint: str, **values) -> PurePosixPath:
    if endpoint == "portfolio_home":
        return PurePosixPath("index.html")
    if endpoint == "project_detail":
        return PurePosixPath("projects") / values["slug"] / "index.html"
    if endpoint == "chronicles_live":
        return PurePosixPath("projects") / "biodynamic-chronicles" / "live" / "index.html"
    if endpoint == "static":
        return PurePosixPath("static") / values["filename"]
    raise ValueError(f"Unsupported endpoint: {endpoint}")


def relative_href(current_page: PurePosixPath, target: PurePosixPath) -> str:
    current_dir = current_page.parent
    if target.name == "index.html":
        target_dir = target.parent
        relative_dir = posixpath.relpath(target_dir.as_posix(), current_dir.as_posix())
        return "./" if relative_dir == "." else f"{relative_dir}/"
    return posixpath.relpath(target.as_posix(), current_dir.as_posix())


def relative_path(current_page: PurePosixPath, target: PurePosixPath) -> str:
    return posixpath.relpath(target.as_posix(), current_page.parent.as_posix())


def format_american_date(value: str) -> str:
    return date.fromisoformat(value).strftime("%m/%d/%Y")


def trimmed_experience(day: date, party_mode: str, appetite: str) -> dict[str, object]:
    state = build_experience(day, party_mode, appetite)
    return {
        "requested_date": state["requested_date"],
        "party_mode": state["party_mode"],
        "appetite": state["appetite"],
        "decision": {
            key: state["decision"][key]
            for key in ("verdict", "headline", "summary")
        },
        "today": {
            "date": state["today"]["date"],
            "day_type": state["today"]["day_type"],
            "moon_phase": state["today"]["moon_phase"],
            "motion": state["today"]["motion"],
            "signal_name": state["today"]["signal_name"],
            "palette_primary": state["today"]["palette"]["primary"],
            "pizza_name": state["today"]["table_plan"]["pizza"]["name"],
            "wine_name": state["today"]["table_plan"]["wine"]["name"],
        },
        "future_forecast": [
            {
                "date": item["date"],
                "day_type": item["day_type"],
                "moon_phase": item["moon_phase"],
                "drinking_well": item["drinking_well"],
                "top_axis": item["top_axis"],
                "motion": item["motion"],
            }
            for item in state["week_horizon"]["nights"][1:4]
        ],
    }


def blog_entries_json(current_page: PurePosixPath) -> list[dict[str, object]]:
    entries = copy.deepcopy(BLOG_ENTRIES)
    for entry in entries:
        for media in entry["media"]:
            media["image"] = relative_href(current_page, route_target("static", filename=media["image"]))
    return entries


def render_template(template_name: str, output_rel: PurePosixPath, **context) -> None:
    template = env.get_template(template_name)

    def local_url_for(endpoint: str, **values) -> str:
        return relative_href(output_rel, route_target(endpoint, **values))

    output_path = DOCS_DIR / output_rel
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        template.render(url_for=local_url_for, **context),
        encoding="utf-8",
    )


def redirect_page(output_rel: PurePosixPath, target_rel: PurePosixPath) -> None:
    output_path = DOCS_DIR / output_rel
    output_path.parent.mkdir(parents=True, exist_ok=True)
    target_href = relative_href(output_rel, target_rel)
    output_path.write_text(
        "\n".join(
            [
                "<!DOCTYPE html>",
                "<html lang=\"en\">",
                "<head>",
                "    <meta charset=\"UTF-8\">",
                f"    <meta http-equiv=\"refresh\" content=\"0; url={target_href}\">",
                f"    <link rel=\"canonical\" href=\"{target_href}\">",
                "    <title>Redirecting</title>",
                "</head>",
                "<body>",
                f"    <p>Redirecting to <a href=\"{target_href}\">{target_href}</a>.</p>",
                "</body>",
                "</html>",
            ]
        ),
        encoding="utf-8",
    )


def render_site(data_start: date, data_end: date) -> None:
    site_today = datetime.now(LOS_ANGELES).date()
    homepage_state = build_experience(site_today, DEFAULT_PARTY_MODE, DEFAULT_APPETITE)
    header_forecast = [
        {
            **item,
            "display_date": format_american_date(item["date"]),
        }
        for item in homepage_state["week_horizon"]["nights"][:3]
    ]

    render_template(
        "index.html",
        PurePosixPath("index.html"),
        owner=OWNER,
        projects=homepage_projects(),
        signal_stats=SIGNAL_STATS,
        featured_project=get_project("biodynamic-chronicles"),
        header_forecast=header_forecast,
    )

    for project in PROJECTS:
        render_template(
            "project_detail.html",
            PurePosixPath("projects") / project["slug"] / "index.html",
            owner=OWNER,
            project=project,
            related_projects=get_related_projects(project["slug"]),
        )

    live_output = PurePosixPath("projects") / "biodynamic-chronicles" / "live" / "index.html"
    render_template(
        "chronicles.html",
        live_output,
        blog_entries=BLOG_ENTRIES,
        blog_entries_json=blog_entries_json(live_output),
        initial_state=trimmed_experience(site_today, DEFAULT_PARTY_MODE, DEFAULT_APPETITE),
        project=get_project("biodynamic-chronicles"),
        site_config={
            "forecast_data_base_url": relative_path(live_output, PurePosixPath("site-data") / "forecast"),
            "supported_min_date": data_start.isoformat(),
            "supported_max_date": data_end.isoformat(),
            "time_zone": "America/Los_Angeles",
        },
    )

    redirect_page(
        PurePosixPath("labs") / "biodynamic-chronicles" / "index.html",
        live_output,
    )


def generate_forecast_data(data_start: date, data_end: date) -> None:
    forecast_dir = DOCS_DIR / "site-data" / "forecast"
    forecast_dir.mkdir(parents=True, exist_ok=True)

    cursor = date(data_start.year, data_start.month, 1)
    while cursor <= data_end:
        days_in_month = monthrange(cursor.year, cursor.month)[1]
        month_payload: dict[str, dict[str, dict[str, dict[str, object]]]] = {}

        for day_number in range(1, days_in_month + 1):
            current_day = date(cursor.year, cursor.month, day_number)
            if current_day < data_start or current_day > data_end:
                continue

            day_key = current_day.isoformat()
            month_payload[day_key] = {}
            for party_mode in PARTY_MODES:
                month_payload[day_key][party_mode] = {}
                for appetite in APPETITES:
                    month_payload[day_key][party_mode][appetite] = trimmed_experience(
                        current_day,
                        party_mode,
                        appetite,
                    )

        file_name = f"{cursor.year:04d}-{cursor.month:02d}.json"
        (forecast_dir / file_name).write_text(
            json.dumps(month_payload, separators=(",", ":")),
            encoding="utf-8",
        )
        print(f"Built forecast data for {file_name}")

        if cursor.month == 12:
            cursor = date(cursor.year + 1, 1, 1)
        else:
            cursor = date(cursor.year, cursor.month + 1, 1)


def prepare_docs() -> None:
    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        STATIC_DIR,
        DOCS_DIR / "static",
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns(".DS_Store"),
    )
    (DOCS_DIR / ".nojekyll").write_text("", encoding="utf-8")


def main() -> None:
    site_today = datetime.now(LOS_ANGELES).date()
    data_start = date(site_today.year - 1, 1, 1)
    data_end = date(site_today.year + 4, 12, 31)

    prepare_docs()
    render_site(data_start, data_end)
    generate_forecast_data(data_start, data_end)
    print("Static site export complete.")


if __name__ == "__main__":
    main()
