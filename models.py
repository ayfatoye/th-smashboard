from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import TEXT, BIGINT

db = SQLAlchemy()

class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(BIGINT, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    vs = db.Column(TEXT)
    player = db.Column(TEXT)
    won = db.Column(TEXT)

class Leaderboard(db.Model):
    __tablename__ = 'leaderboard'
    id = db.Column(BIGINT, primary_key=True)
    name = db.Column(TEXT)
    wins = db.Column(TEXT)
    losses = db.Column(TEXT)