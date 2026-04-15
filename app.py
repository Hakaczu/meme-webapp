import os
from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

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

if __name__ == '__main__':
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug, host="0.0.0.0", port=5050)
