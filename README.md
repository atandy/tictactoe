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
* Make a move: 
  * `curl -X POST "http://127.0.0.1:5000/move?game_uuid=0ee0c8ab-19d9-4cb0-acbe-ad48b3a85fd7&player_id=1&space=A"`