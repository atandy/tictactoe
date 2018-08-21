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

        return "Created new game with uuid: {}".format(g.uuid)


#curl -X POST "http://127.0.0.1:5000/move?game_uuid=0ee0c8ab-19d9-4cb0-acbe-ad48b3a85fd7&player_id=1&space=A"
@app.route("/move", methods=['GET', 'POST'])
def move():
    if request.method =='POST':
        game_uuid = request.args.get('game_uuid')
        player_id = int(request.args.get('player_id'))
        space = request.args.get('space')

        game = db.session.query(models.Game).filter(models.Game.uuid == game_uuid).first()
        
        if not game or game.complete:
            return '\n Game either does not exist or is no longer active \n'

        g = Game(game_uuid) 
        marker = g.markers[player_id]        
        g.make_move(space, marker)
        
        board = models.Board()
        board.player_id = player_id
        board.game_uuid = game_uuid
        board.space = space
        db.session.add(board)
        db.session.commit()
        if g.game_status:
            for k, v in g.markers.items():
                if v == g.game_status:
                    game.winner = player_id
                    game.complete = True
                    db.session.add(game)
                    db.session.commit()
                    return '\n The winner is: {}s, player id: {} \n'.format(g.game_status, k)
        else:
            return "\n Move registered; there is no current winner. \n"

        