from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os 

db = SQLAlchemy()

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    def __repr__(self):
        return '<User %r>' % self.id

class Game(db.Model):
    uuid = db.Column(db.Text, nullable=False, primary_key=True)
    player_one = db.Column(db.Integer, db.ForeignKey('player.id'))
    player_two = db.Column(db.Integer, db.ForeignKey('player.id'))
    x_marker = db.Column(db.Text, nullable=False)
    complete = db.Column(db.Boolean) # should be nullable=False
    winner = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_uuid = db.Column(db.Text, db.ForeignKey('game.uuid'))
    space = db.Column(db.String(1), nullable=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)