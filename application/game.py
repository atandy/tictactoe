import uuid
from application import models
from flask_sqlalchemy import SQLAlchemy
import os
from application import db
import sqlalchemy

import logging
logging.basicConfig(
    filename='game.log', 
    filemode='w', 
    format='%(asctime)s:%(levelname)s:%(message)s', 
    level=logging.DEBUG)

class Player:
    def __init__(self, player_id, marker_type):
        self.id = player_id
        # marker only relevant on a per game basis.
        # this is why it doesn't exist on the Player model.
        self.marker_type = marker_type 
    
    def create(self):
        '''Create a player if they don't already exist'''
        player = db.session.query(models.Player).filter(models.Player.id == self.id).first()
        if not player:
            player = models.Player(id=self.id)
            db.session.add(player)
            db.session.commit()

class Game:
    def __init__(self, game_uuid=None):
        if not game_uuid:
            self.uuid = self.generate_uuid()
        elif game_uuid:
            self.uuid = game_uuid
            self.update()
        return

    @staticmethod
    def generate_uuid():
        return str(uuid.uuid4())

    def create(self, player_one_id, player_two_id, x_marker):
        '''Create a new game'''
        game = models.Game(
            uuid=self.uuid, 
            player_one=player_one_id, 
            player_two=player_two_id,
            x_marker=x_marker)
        db.session.add(game)
        db.session.commit()

    #TODO: better ways to assign their player markers.
    def start_new_game(self, player_one_id, player_two_id, x_marker):
        '''Create new game between player one and player two'''
        if x_marker == 'one':
            self.p1 = Player(player_one_id, 'X')
            self.p2 = Player(player_two_id, 'O')
        elif x_marker == 'two':
            self.p1 = Player(player_one_id, 'O')
            self.p2 = Player(player_one_id, 'X')

        # create the players if they don't exist. 
        # TODO: fix ?
        self.p1.create()
        self.p2.create()

        # create the game in the backend
        self.create(player_one_id, player_two_id, x_marker)

        # when you start a new game, create a new board with all spaces unoccopied.
        self.board = Board()
        return 

    def make_move(self, board_position, marker_type):
        self.board.occupy_space(board_position, marker_type)
        # every time a move is made, check if there is a winner. 
        self.game_status = self.board.check_permutations()
        return

    def update(self):
        '''
        This loads the board from the backend if an existing game_uuid is
        passed in on the init of Game.
        TODO: add relationships to the models and make this way easier.
        '''
        game = db.session.query(models.Game).filter(models.Game.uuid == self.uuid).first()
        player_one = db.session.query(models.Player).filter(models.Player.id == game.player_one).first()
        player_two = db.session.query(models.Player).filter(models.Player.id == game.player_two).first()

        #TODO: ew.
        if game.x_marker == 'one':
            self.markers = { 
                player_one.id: 'X',
                player_two.id: 'O'
            }
        elif game.x_marker == 'two':
            self.markers = {
                player_one.id: 'O',
                player_two.id: 'X'
            }
            
        self.p1 = player_one
        self.p2 = player_two

        self.players = [self.p1, self.p2]
        self.board = Board()

        db_board = db.session.query(models.Board).filter(models.Board.game_uuid==self.uuid).all()
        
        # populate all positions on the Game->Board 
        for board_row in db_board:
            for player in self.players:
                if player.id == board_row.player_id:
                    logging.info("Occupying space: {}".format(board_row.space))
                    self.board.occupy_space(board_row.space, self.markers[player.id])

            current_status = self.board.check_permutations()
            self.game_status = current_status
                        
class Board:
    def __init__(self):
        self.id = None
        self.A = None
        self.B = None
        self.C = None
        self.D = None
        self.E = None
        self.F = None
        self.G = None
        self.H = None
        self.I = None
        return
    
    '''
    def create():
        board = models.Board(game_uuid)
        db.session.add(board)
        db.session.commit()
    '''
    def occupy_space(self, position, marker_type):
        '''Set the board position attribute'''
        setattr(self, position, marker_type)
    
    def check_permutations(self):
        ''' Determines if the game has been won'''
        self.winning_groups = [
            [self.A, self.B, self.C],
            [self.A, self.D, self.G],
            [self.A, self.E, self.I],
            [self.C, self.F, self.I],
            [self.C, self.E, self.G],
            [self.B, self.E, self.H],
            [self.D, self.E, self.F],
            [self.G, self.H, self.I]
        ]
        def detect_winning_group(group):
            for position in group:
                # if any positions are still none, then we can skip this group
                if position is None:
                    return None
                else:
                    continue
            # if all three of the positions are populated and are 
            # populated by the same character, then we have a winner. 
            if len(set(group)) <= 1:
                return group[0]

        # iterate through all of the possible winning groups and 
        # detect if there are any winners.
        for wg in self.winning_groups:
            res = detect_winning_group(wg)
            if res == None:
                continue
            else:
                return res

# Play the game locally (worked at least before I added bunch of server stuff.)
'''
g = Game()
g.start_new_game(1, 2, 'one') 
g.make_move(g.p1, 'A')
g.make_move(g.p2, 'B')
g.make_move(g.p1, 'A')
g.make_move(g.p2, 'E')
g.make_move(g.p1, 'C')
g.make_move(g.p2, 'B')
g.make_move(g.p1, 'I')
g.make_move(g.p2, 'H')
g.board.check_permutations()
'''