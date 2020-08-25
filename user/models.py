from libs.orm import db


class USER(db.Model):
    __tablename__ = 'user'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True, nullable=False)
    password=db.Column(db.String(128),nullable=True)