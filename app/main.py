import os
import json
import calendar
from datetime import datetime
from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


from .box import DayMeal  # Make sure box.py is in the same folder as main.py

app = FastAPI(title="ManageMyFood")

# Mount the folder that contains your static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Adjust the path as needed to match your folder structure.
templates = Jinja2Templates(directory="app/templates")

def shift_month(year: int, month: int, shift: int):
    """
    Moves the current month by `shift` units (e.g. -1 for prev, +1 for next).
    If it goes out of bounds, adjust the year accordingly.
    """
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
    year: int = Query(None),
    month: int = Query(None)
):
    """
    Renders a 7-column calendar for the given (year, month).
    Displays minimal meal names in each day box, with full data in a modal pop-up.
    """
    now = datetime.now()
    if year is None:
        year = now.year
    if month is None:
        month = now.month

    # 1) Determine how many days in this month
    _, days_in_month = calendar.monthrange(year, month)

    # 2) We'll create up to 42 day boxes (7 columns, up to 6 rows).
    n_box = 42
    day_meals_list = []

    for day_num in range(1, n_box + 1):
        if day_num <= days_in_month:
            dm = DayMeal(year, month, day_num)
            dm.load_data()
            day_meals_list.append(dm)
        else:
            # If beyond the month's real days, store None
            day_meals_list.append(None)

    # 3) Month name for display, e.g. "February 2025"
    month_name = f"{calendar.month_name[month]} {year}"

    # 4) Build previous/next links
    prev_year, prev_month = shift_month(year, month, -1)
    next_year, next_month = shift_month(year, month, 1)
    prev_link = f"/?year={prev_year}&month={prev_month}"
    next_link = f"/?year={next_year}&month={next_month}"

    # 5) Render the "calendar.html" template
    return templates.TemplateResponse(
        "calendar.html",
        {
            "request": request,
            "month_name": month_name,
            "day_meals_list": day_meals_list,
            "prev_link": prev_link,
            "next_link": next_link
        }
    )

@app.get("/api/day_details")
def get_day_details(year: int, month: int, day: int):
    from .box import DayMeal
    dm = DayMeal(year, month, day)
    dm.load_data()
    return {
        "lunch": dm.lunch,   # e.g. { name, recipe, etc. }
        "dinner": dm.dinner
    }


