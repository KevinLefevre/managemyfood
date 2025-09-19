"""FastAPI entry point for the ManageMyFood application."""

import calendar
from datetime import datetime

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .box import DayMeal


# Start the week on Monday when rendering the calendar.
calendar.setfirstweekday(calendar.MONDAY)

app = FastAPI(title="ManageMyFood")

# Mount the folder that contains your static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Adjust the path as needed to match your folder structure.
templates = Jinja2Templates(directory="app/templates")


def shift_month(year: int, month: int, shift: int) -> tuple[int, int]:
    """Return the year and month after applying ``shift`` months."""

    new_month = month + shift
    new_year = year
    if new_month < 1:
        new_year -= 1
        new_month = 12
    elif new_month > 12:
        new_year += 1
        new_month = 1
    return new_year, new_month


@app.get("/", response_class=HTMLResponse)
def show_calendar(
    request: Request,
    year: int | None = Query(default=None),
    month: int | None = Query(default=None),
):
    """Render a calendar with meal information for ``year``/``month``."""

    now = datetime.now()
    if year is None:
        year = now.year
    if month is None:
        month = now.month

    # Build the calendar grid aligned on weeks (Monday first)
    cal = calendar.Calendar(firstweekday=calendar.MONDAY)
    raw_weeks = cal.monthdayscalendar(year, month)

    calendar_grid: list[list[DayMeal | None]] = []
    total_lunches = 0
    total_dinners = 0
    days_with_both = 0

    for raw_week in raw_weeks:
        week: list[DayMeal | None] = []
        for day_value in raw_week:
            if day_value == 0:
                week.append(None)
                continue

            dm = DayMeal(year, month, day_value)
            dm.load_data()

            if dm.lunch:
                total_lunches += 1
            if dm.dinner:
                total_dinners += 1
            if dm.lunch and dm.dinner:
                days_with_both += 1

            week.append(dm)

        calendar_grid.append(week)

    month_name = f"{calendar.month_name[month]} {year}"

    month_summary = {
        "total_lunches": total_lunches,
        "total_dinners": total_dinners,
        "days_with_both": days_with_both,
        "planned_meals": total_lunches + total_dinners,
    }

    weekday_labels = []
    for offset in range(7):
        weekday_index = (calendar.firstweekday() + offset) % 7
        weekday_labels.append(calendar.day_name[weekday_index])

    prev_year, prev_month = shift_month(year, month, -1)
    next_year, next_month = shift_month(year, month, 1)
    prev_link = f"/?year={prev_year}&month={prev_month}"
    next_link = f"/?year={next_year}&month={next_month}"

    current_day: int | None = None
    if now.year == year and now.month == month:
        current_day = now.day

    return templates.TemplateResponse(
        "calendar.html",
        {
            "request": request,
            "month_name": month_name,
            "calendar_grid": calendar_grid,
            "weekday_labels": weekday_labels,
            "month_summary": month_summary,
            "current_day": current_day,
            "prev_link": prev_link,
            "next_link": next_link,
        },
    )


@app.get("/api/day_details")
def get_day_details(year: int, month: int, day: int):
    dm = DayMeal(year, month, day)
    dm.load_data()
    return {
        "lunch": dm.lunch,
        "dinner": dm.dinner,
    }
