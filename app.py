from flask import Flask, render_template
import requests
import os
import time
import json
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

API_KEY = os.getenv("FOOTBALL_API_KEY")
BASE_URL = "https://api.football-data.org/v4"
CACHE_TTL = 600
_cache = {"data": None, "timestamp": 0}

# Load teams data
with open("teams.json", "r", encoding="utf-8") as f:
    teams_info = json.load(f)


def fetch_matches():
    now = time.time()
    if _cache["data"] and now - _cache["timestamp"] < CACHE_TTL:
        return _cache["data"]

    url = f"{BASE_URL}/competitions/CL/matches"
    headers = {"X-Auth-Token": API_KEY}

    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json().get("matches", [])
        matches = []
        for m in data:
            home_name = m["homeTeam"]["name"]
            away_name = m["awayTeam"]["name"]
            matches.append({
                "home": home_name,
                "away": away_name,
                "date": m["utcDate"][:10],
                "status": m["status"],
                "score": m["score"]["fullTime"],
                "home_logo": teams_info.get(home_name, {}).get("logo", ""),
                "away_logo": teams_info.get(away_name, {}).get("logo", "")
            })
        _cache.update({"data": matches, "timestamp": now})
        return matches
    except Exception as e:
        print("Error fetching matches:", e)
        return _cache["data"] or []


@app.route("/")
def index():
    matches = fetch_matches()
    upcoming = [m for m in matches if m["status"] == "SCHEDULED"]
    finished = [m for m in matches if m["status"] == "FINISHED"]
    return render_template("index.html", upcoming=upcoming, finished=finished)


@app.route("/teams")
def teams():
    return render_template("teams.html", teams=teams_info)


@app.route("/upcoming")
def upcoming_matches():
    matches = fetch_matches()
    upcoming = [m for m in matches if m["status"] == "SCHEDULED"]
    return render_template("matches_upcoming.html", matches=upcoming)


@app.route("/finished")
def finished_matches():
    matches = fetch_matches()
    finished = [m for m in matches if m["status"] == "FINISHED"]
    return render_template("matches_finished.html", matches=finished)


@app.route("/standings")
def standings():
    url = f"{BASE_URL}/competitions/CL/standings"
    headers = {"X-Auth-Token": API_KEY}

    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        # Usually the API returns a list of standings tables
        table = data.get("standings", [])[0].get("table", [])
        return render_template("standings.html", table=table)
    except Exception as e:
        print("Error fetching standings:", e)
        return render_template("standings.html", table=[])


if __name__ == "__main__":
    app.run(debug=True)
