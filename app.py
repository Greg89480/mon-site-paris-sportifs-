from flask import Flask, render_template, request, jsonify
import understat
import asyncio
from datetime import datetime
import json

app = Flask(__name__)

async def get_team_data(team_name):
    from understat import Understat
    import aiohttp
    async with aiohttp.ClientSession() as session:
        understat_api = Understat(session)
        teams = await understat_api.get_teams("epl")
        team_slug = None
        for team in teams:
            if team_name.lower() in team['title'].lower():
                team_slug = team['title']
                break
        if not team_slug:
            return []
        matches = await understat_api.get_team_matches("epl", team_slug, datetime.now().year)
        return matches[-13:]  # last 13 matches

def calculate_under_prob(matches):
    total = len(matches)
    under_3_5 = sum(1 for m in matches if (float(m['goals']['h']) + float(m['goals']['a'])) < 3.5)
    under_4_5 = sum(1 for m in matches if (float(m['goals']['h']) + float(m['goals']['a'])) < 4.5)
    return {
        "under_3_5": round((under_3_5 / total) * 100, 1),
        "under_4_5": round((under_4_5 / total) * 100, 1)
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    team1 = data["team1"]
    team2 = data["team2"]

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        matches_team1 = loop.run_until_complete(get_team_data(team1))
        matches_team2 = loop.run_until_complete(get_team_data(team2))
        prob1 = calculate_under_prob(matches_team1)
        prob2 = calculate_under_prob(matches_team2)
        under_3_5 = round((prob1["under_3_5"] + prob2["under_3_5"]) / 2, 1)
        under_4_5 = round((prob1["under_4_5"] + prob2["under_4_5"]) / 2, 1)
        return jsonify({
            "under_3_5": under_3_5,
            "under_4_5": under_4_5
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500