# TicTacToe

## Getting Started

### Prerequisites

#### Python 3 and Install requirements
```
* Python 3
* pip install -r requirements.txt
```

#### Set up Postgres
* Use Google

#### Set up Environment Variables

```
export SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://username_here:@localhost/database_name_here
```
## Playing

* Start the server
* python run.py
* Create a game: 
  * `curl -X POST "http://127.0.0.1:5000/create_game?p1id=1&p2id=2&x_marker=one"`
  * p1id : player one's ID
  * p2id : player two's ID
  * x_marker : can be 'one' or 'two'. refers to which player is X
* Make a move: 
  * `curl -X POST "http://127.0.0.1:5000/move?game_uuid=0ee0c8ab-19d9-4cb0-acbe-ad48b3a85fd7&player_id=1&space=A"`
  * game_uuid : determined when a new game is created.
  * player_id : the ID of the player making the move.
  * space : the board space the player moved in. options are A-I
* Board looks like this
![alt text](https://raw.githubusercontent.com/atandy/tictactoe/master/board_spaces.png)


