import os
from datetime import date

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URI"
) or "sqlite:///" + os.path.join(basedir, "minimalnews.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

import news_spider
from models import News


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "News": News}


@app.cli.command()
def scrape():
    news_spider.run_spider()


@app.route("/news")
def get_news():
    category = request.args.get("category")

    if not category:
        response = jsonify({"error": "no category specified"})
        response.status_code = 400
        return response

    serialized_news = list()
    for category in category.split():
        news_obj = News.query.filter_by(
            category=category, published_date=date.today()
        ).all()

        if news_obj:
            serialized_news.append(
                [
                    {
                        "id": news.id,
                        "url": news.url,
                        "category": news.category,
                        "headline": news.headline,
                        "body": news.summarized_body,
                        "published_date": news.published_date,
                    }
                    for news in news_obj
                ]
            )

    if not serialized_news:
        response = jsonify({"error": "no content found"})
        response.status_code = 404
        return response

    return jsonify(serialized_news)
