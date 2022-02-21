import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URI"
) or "sqlite:///" + os.path.join(basedir, "minimalnews.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from models import News


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "News": News}
