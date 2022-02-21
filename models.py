from app import db


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(128), unique=True, nullable=False)
    category = db.Column(db.String(16), index=True, nullable=False)
    headline = db.Column(db.String(128), nullable=False)
    summarized_body = db.Column(db.Text)
    published_date = db.Column(db.Date, index=True, nullable=False)

    def __repr__(self):
        return f"[{self.published_date}] {self.headline}"
