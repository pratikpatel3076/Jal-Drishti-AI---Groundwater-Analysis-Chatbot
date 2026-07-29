import os
import re
import io
import json
import difflib
from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

DATA_PATH = Path(__file__).parent / "ingres_clone.json"
CHART_DIR = Path(__file__).parent / "static" / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)

df = None
USE_OPENAI = False
openai = None

def load_data():
    global df
    if not DATA_PATH.exists():
        print(f"WARNING: Data file not found at {DATA_PATH}")
        return
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        df = pd.DataFrame(data)
    elif isinstance(data, dict):
        for v in data.values():
            if isinstance(v, list) and (len(v) == 0 or isinstance(v[0], dict)):
                df = pd.DataFrame(v)
                break
    if df is not None:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['year'] = df['date'].dt.year

def init_openai():
    global USE_OPENAI, openai
    api_key = os.getenv("OPENAI_API_KEY", "")
    if api_key:
        try:
            import openai as _openai
            openai = _openai
            openai.api_key = api_key
            USE_OPENAI = True
            print("OpenAI enabled (GPT-3.5-turbo)")
        except ImportError:
            print("OpenAI package not installed; falling back to TF-IDF")

def parse_query(query: str):
    years = [int(y) for y in re.findall(r'(19\d{2}|20\d{2})', query)]
    place = None
    tokens = query.split()
    for kw in ['at', 'in']:
        if kw in tokens:
            idx = tokens.index(kw)
            if idx + 1 < len(tokens):
                place = tokens[idx + 1]
                break
    return {'raw': query, 'place': place, 'years': years}

def match_place(place: str):
    if not place or df is None:
        return None
    candidates = (
        df['district_name'].dropna().unique().tolist()
        + df['station_name'].dropna().unique().tolist()
    )
    match = difflib.get_close_matches(place, candidates, n=1, cutoff=0.6)
    return match[0] if match else None

def point_lookup(place: str, year: int):
    m = match_place(place)
    if not m:
        return None, f"Sorry, I couldn't find a match for '{place}'. Please check the spelling or try a different location."
    sub = df[(df['year'] == year) & ((df['district_name'] == m) | (df['station_name'] == m))]
    if sub.empty:
        return None, f"No water level data available for {m} in {year}. Try a different year."
    row = sub.iloc[0]
    level_diff = float(row['level_diff'])
    if level_diff > 0:
        trend = f"increased by {level_diff:.2f}m"
    elif level_diff < 0:
        trend = f"decreased by {abs(level_diff):.2f}m"
    else:
        trend = "remained stable"
    response = (
        f"**Water Level Information for {m} in {year}**\n\n"
        f"**Location Details:**\n"
        f"- Station: {row['station_name']}\n"
        f"- District: {row['district_name']}\n"
        f"- State: {row['state_name']}\n\n"
        f"**Water Level Data:**\n"
        f"- Current Level: {float(row['currentlevel']):.2f} meters\n"
        f"- Change from Previous Year: {trend}\n\n"
        f"This data represents the groundwater level measurements for the specified location and year."
    )
    return None, response

def trend_lookup(place: str, year_from: int, year_to: int):
    m = match_place(place)
    if not m:
        return None, f"Sorry, I couldn't find a match for '{place}'."
    sub = df[(df['year'] >= year_from) & (df['year'] <= year_to) & ((df['district_name'] == m) | (df['station_name'] == m))]
    if sub.empty:
        return None, f"No water level data available for {m} between {year_from} and {year_to}."
    years = sub['year'].tolist()
    values = sub['currentlevel'].tolist()
    min_level = min(values)
    max_level = max(values)
    avg_level = sum(values) / len(values)
    total_change = values[-1] - values[0]
    if total_change > 0.5:
        overall_trend = "rising significantly"
    elif total_change > 0:
        overall_trend = "slightly rising"
    elif total_change < -0.5:
        overall_trend = "declining significantly"
    elif total_change < 0:
        overall_trend = "slightly declining"
    else:
        overall_trend = "relatively stable"
    plt.figure(figsize=(8, 5))
    plt.plot(years, values, marker='o', linewidth=2, markersize=6, color='#2563eb')
    plt.xlabel("Year", fontsize=12)
    plt.ylabel("Water Level (meters)", fontsize=12)
    plt.title(f"Water Level Trend at {m} ({year_from}-{year_to})", fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    fname = f"{m.replace(' ', '_')}_trend_{year_from}_{year_to}.png"
    chart_path = CHART_DIR / fname
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    response = (
        f"**Water Level Trend Analysis for {m} ({year_from}-{year_to})**\n\n"
        f"- **Location:** {m}\n"
        f"- **Period:** {year_from} to {year_to}\n\n"
        f"**Trend Summary:**\n"
        f"- Overall Trend: {overall_trend}\n"
        f"- Total Change: {total_change:+.2f} meters\n"
        f"- Average Level: {avg_level:.2f} meters\n"
        f"- Highest Level: {max_level:.2f} meters ({years[values.index(max_level)]})\n"
        f"- Lowest Level: {min_level:.2f} meters ({years[values.index(min_level)]})\n\n"
        + "\n".join([f"- {year}: {value:.2f}m" for year, value in zip(years, values)])
    )
    return f"/api/charts/{fname}", response

def generate_ai_response(query: str, intent: str) -> str:
    if not USE_OPENAI or openai is None:
        return None
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Jal Drishti AI, a groundwater analysis assistant. Answer concisely using provided data. The dataset covers Indian groundwater levels from 2018-2020 (CGWB)."},
                {"role": "user", "content": f"Query: {query}. Intent: {intent}. Provide a helpful response about groundwater."}
            ],
            temperature=0.2,
            max_tokens=200
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return None

def handle_query(query: str):
    parsed = parse_query(query)
    place, years = parsed['place'], parsed['years']
    if not place:
        return {"answer": "Please specify a location in your query. For example: 'What is the water level in Mumbai in 2020?'", "chart_url": None, "ai_insights": False}
    if df is None:
        return {"answer": "Groundwater data is not loaded. Please ensure backend/ingres_clone.json exists.", "chart_url": None, "ai_insights": False}
    if len(years) == 1:
        chart, answer = point_lookup(place, years[0])
    elif len(years) >= 2:
        chart, answer = trend_lookup(place, years[0], years[1])
    else:
        return {"answer": "Please specify a year or year range. Example: 'Water level in Mumbai in 2020' or 'Trends in Delhi from 2018 to 2020'.", "chart_url": None, "ai_insights": False}
    ai_answer = generate_ai_response(query, "point_lookup" if len(years) == 1 else "trend_lookup")
    if ai_answer:
        return {"answer": ai_answer, "chart_url": chart, "ai_insights": True}
    return {"answer": answer, "chart_url": chart, "ai_insights": False}

@app.route("/api/chat", methods=["POST"])
def chat():
    body = request.get_json(force=True)
    query = (body.get("query") or "").strip()
    if not query:
        return jsonify({"error": "Query is required"}), 400
    result = handle_query(query)
    result["language"] = body.get("language", "EN")
    result["suggestions"] = [
        "What is the water level in Mumbai in 2020?",
        "Show trends in Delhi from 2018 to 2020",
        "Compare groundwater levels in Chennai",
        "What is the highest water level recorded in Bangalore?"
    ]
    return jsonify(result)

@app.route("/api/charts/<filename>")
def serve_chart(filename):
    chart_path = CHART_DIR / filename
    if not chart_path.exists():
        return jsonify({"error": "Chart not found"}), 404
    return send_file(str(chart_path), mimetype="image/png")

@app.route("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "openai": USE_OPENAI,
        "data_loaded": df is not None
    })

if __name__ == "__main__":
    load_data()
    init_openai()
    print(f"Data loaded: {df is not None}")
    print(f"OpenAI: {'enabled' if USE_OPENAI else 'disabled (TF-IDF fallback)'}")
    app.run(host="0.0.0.0", port=5000, debug=True)
