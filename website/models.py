from libs.orm import db


class WEB(db.Model):
    __tablename__ = 'web'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(20), nullable=False)
    word = db.Column(db.Text)
