import json
import os
import threading
from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

STATS_FILE = "/meme-app/data/stats.json"
_stats_lock = threading.Lock()


def load_stats():
    try:
        with open(STATS_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"likes": 0, "mehs": 0}


def save_stats(stats):
    os.makedirs(os.path.dirname(STATS_FILE), exist_ok=True)
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f)


def get_meme():
    url = "https://meme-api.com/gimme"
    response = requests.get(url, timeout=5).json()
    preview = response.get("preview", [])
    meme_large = preview[-2] if len(preview) >= 2 else response.get("url", "")
    subreddit = response["subreddit"]
    title = response["title"]
    author = response["author"]
    return meme_large, subreddit, title, author


@app.route("/")
def index():
    try:
        meme_pic, subreddit, title, author = get_meme()
        return render_template("meme_index.html", meme_pic=meme_pic, subreddit=subreddit, meme_title=title, author=author)
    except Exception as e:
        app.logger.error("Failed to fetch meme: %s", e)
        return render_template("error.html")


@app.route("/api/meme")
def api_meme():
    try:
        meme_pic, subreddit, title, author = get_meme()
        return jsonify({"meme_pic": meme_pic, "subreddit": subreddit, "title": title, "author": author})
    except Exception as e:
        app.logger.error("Failed to fetch meme: %s", e)
        return jsonify({"error": "API Error"}), 500


@app.route("/api/like", methods=["POST"])
def api_like():
    with _stats_lock:
        stats = load_stats()
        stats["likes"] += 1
        save_stats(stats)
    return jsonify(stats)


@app.route("/api/meh", methods=["POST"])
def api_meh():
    with _stats_lock:
        stats = load_stats()
        stats["mehs"] += 1
        save_stats(stats)
    return jsonify(stats)


@app.route("/api/stats")
def api_stats():
    with _stats_lock:
        return jsonify(load_stats())


if __name__ == '__main__':
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug, host="0.0.0.0", port=5050)
