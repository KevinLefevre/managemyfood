import os
import json
import calendar
from datetime import datetime
from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI(title="ManageMyFood")
templates = Jinja2Templates(directory="app/templates")

def shift_month(year: int, month: int, shift: int):
    """
    Move the current month by 'shift' (e.g. -1 for prev, +1 for next).
    If month goes below 1 or above 12, adjust the year accordingly.
    Returns (new_year, new_month).
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
    month: int = Query(None),
    n_box: int = 36
):
    # Default year/month if none provided
    now = datetime.now()
    if year is None:
        year = now.year
    if month is None:
        month = now.month

    # Build path to JSON: data/<year>/<month>/meals.json
    data_folder = os.path.join("data", f"{year}", f"{month:02d}")
    json_file = os.path.join(data_folder, "meals.json")

    # Create a list of length n_box to store meal info or None
    day_list = [None] * n_box

    try:
        with open(json_file, "r", encoding="utf-8") as f:
            meals_data = json.load(f)
    except FileNotFoundError:
        # If we don't find a JSON file, use empty data
        meals_data = {
            "year": year,
            "month": calendar.month_name[month],
            "days": []
        }

    # Fill day_list with lunch/dinner from the JSON
    for item in meals_data.get("days", []):
        day_num = item["day"]
        index = day_num - 1
        if 0 <= index < n_box:
            day_list[index] = {
                "lunch": item.get("lunch", ""),
                "dinner": item.get("dinner", "")
            }

    # Month name for display, e.g. "February 2025"
    month_name = f"{calendar.month_name[month]} {year}"

    # Compute previous/next month for arrow links
    prev_year, prev_month = shift_month(year, month, -1)
    next_year, next_month = shift_month(year, month, 1)

    # Build the href for each arrow, preserving n_box
    prev_link = f"/?year={prev_year}&month={prev_month}&n_box={n_box}"
    next_link = f"/?year={next_year}&month={next_month}&n_box={n_box}"

    return templates.TemplateResponse(
        "boxes_calendar.html",
        {
            "request": request,
            "month_name": month_name,
            "day_list": day_list,    
            "prev_link": prev_link,
            "next_link": next_link
        }
    )
