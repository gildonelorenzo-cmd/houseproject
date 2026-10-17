"""
House Leaderboard server: serves the page and handles the admin side,
so the admin password never has to be inside the page.

    pip3 install flask
    ADMIN_PASSWORD='your-password' python3 app.py

then open http://localhost:8000 (phones on the same Wi-Fi can use
this computer's IP address instead of localhost).
"""
import hmac
import json
import math
import os
import secrets
import time
import urllib.request
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory, session

BASE = Path(__file__).resolve().parent
HOUSES = {"acrobats", "quicksilver", "druids", "bravehearts"}
DB_URL = os.environ.get("FIREBASE_DB_URL", "https://housesproject-cb92e-default-rtdb.europe-west1.firebasedatabase.app")
# a database secret, only needed once the Firebase rules stop allowing public writes
DB_AUTH = os.environ.get("FIREBASE_AUTH", "")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")

if not ADMIN_PASSWORD:
    raise SystemExit("Set ADMIN_PASSWORD first, e.g.  ADMIN_PASSWORD='your-password' python3 app.py")

# 5 wrong passwords from the same address locks it out for a minute
MAX_TRIES = 5
LOCKOUT_SECONDS = 60
failed_logins = {}

# static_folder=None so Flask can't serve app.py or anything else by accident
app = Flask(__name__, static_folder=None)
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


@app.get("/")
@app.get("/house-leaderboard-portal.html")
def page():
    return send_from_directory(BASE, "house-leaderboard-portal.html")


@app.get("/project/<path:name>")
def images(name):
    return send_from_directory(BASE / "project", name)


@app.post("/api/login")
def login():
    ip = request.remote_addr
    count, since = failed_logins.get(ip, (0, 0))
    if count >= MAX_TRIES and time.time() - since < LOCKOUT_SECONDS:
        return jsonify(error="too many tries"), 429

    password = (request.get_json(silent=True) or {}).get("password", "")
    if not isinstance(password, str) or not hmac.compare_digest(password.encode(), ADMIN_PASSWORD.encode()):
        if time.time() - since >= LOCKOUT_SECONDS:
            count, since = 0, time.time()
        failed_logins[ip] = (count + 1, since)
        return jsonify(error="wrong password"), 401

    failed_logins.pop(ip, None)
    session["admin"] = True
    return jsonify(ok=True)


@app.post("/api/scores")
def save_scores():
    if not session.get("admin"):
        return jsonify(error="not signed in"), 401
    data = request.get_json(silent=True)
    if not valid_scores(data):
        return jsonify(error="bad data"), 400

    url = f"{DB_URL}/houseScores.json"
    if DB_AUTH:
        url += "?auth=" + DB_AUTH
    req = urllib.request.Request(url, data=json.dumps(data).encode(), method="PUT",
                                 headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=10).close()
    except OSError as err:
        app.logger.error("Firebase write failed: %s", err)
        return jsonify(error="could not reach the database"), 502
    return jsonify(ok=True)


def valid_scores(data):
    # same shape the page reads: {house: {score, note}} for all four houses
    if not isinstance(data, dict) or set(data) != HOUSES:
        return False
    for house in data.values():
        if not isinstance(house, dict) or set(house) != {"score", "note"}:
            return False
        score, note = house["score"], house["note"]
        # bool is a subclass of int in python, so rule it out first
        if isinstance(score, bool) or not isinstance(score, (int, float)) or not math.isfinite(score):
            return False
        if not isinstance(note, str) or len(note) > 200:
            return False
    return True


if __name__ == "__main__":
    # port 5000 is taken by AirPlay on Macs, so default to 8000
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
