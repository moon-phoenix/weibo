from libs.orm import db


class WEB(db.Model):
    __tablename__ = 'web'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True)
    word=db.Column(db.text,nullable=True)