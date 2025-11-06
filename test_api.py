import os
import requests

API_KEY = os.getenv("FOOTBALL_API_KEY")
BASE_URL = "https://api.football-data.org/v4"

# Example: fetch Champions League matches
url = f"{BASE_URL}/competitions/CL/matches"
headers = {"X-Auth-Token": API_KEY}

resp = requests.get(url, headers=headers)
data = resp.json()
print("Matches:", len(data.get("matches", [])))

# Example: fetch one team squad (replace 86 with valid team id)
team_id = 86
url_team = f"{BASE_URL}/teams/{team_id}"
resp_team = requests.get(url_team, headers=headers)
print(resp_team.json())
