from flask import Flask, request
from application.game import Game
from application import models
from flask_sqlalchemy import SQLAlchemy
import os
from application import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

#db = SQLAlchemy(app)

# assume that we are pulling the player ids by first having them log in. 


#curl -X POST "http://127.0.0.1:5000/create_game?p1id=1&p2id=2&x_marker=one"
@app.route("/create_game", methods=['GET','POST'])
def create_game():
    if request.method == 'POST':
        player_one_id = request.args.get('p1id')
        player_two_id = request.args.get('p2id')
        x_marker = request.args.get('x_marker')
        g = game.Game()
        g.start_new_game(player_one_id, player_two_id, x_marker)

        return "Created new game with uuid: {}".format(g.id)


#curl -X POST "http://127.0.0.1:5000/create_game?p1id=1&p2id=2&x_marker=one"
#&game_uuid=0c0badf9-d5ec-44e2-8bc9-e87cdd44a7b7
@app.route("/move", methods=['GET', 'POST'])
    if request.method =='POST':
        game_uuid = request.args.get('game_uuid')
        game = db.session.query(models.Game).filter(models.Game.uuid == game_uuid).first()
        
        if not game:
            return 'Game either does not exist or is no longer active'

        g = game.Game(game_uuid) 
        
        g.make_move(g.p1, 'A')
