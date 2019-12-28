A basic interface, a server and a cliente for the table game Boku (Bollox) made with Python 3.

This is a fork from [Boku Engine](https://github.com/ricardoaraujo/boku-engine) and was developed as a task for the Artificial Intelligence Class of the Computer Science Masters Course at UFPel.

## Requirements
* Python 3
* Flask
* Flask-SocketIO

## Installing
pip install -r requirements.txt

## Executing

```
./python server.py
```

Use a browser to access `http://localhost:8080/visualizador.html`.

## Client

### Random Client
A simple client that makes random moves is available (`random_client.py`). To use it, run the server and then execute the client passing the player number (1 or 2) as an argument. You can run two clients simultaneosly, one with each player number.

### Dumb Client
A simple client that uses simple heuristics is available (`dumb_client.py`). To use it, run the server and then execute the client passing the player number (1 or 2) as an argument. You can run two clients simultaneosly, one with each player number.

### Another Dumb Client
A client that uses min-max with alpha-beta pruning and a LRU for optimizing recalculations is available (`another_dumb_client.py`). This client differentiates from the Dumb Client because the use of alpha-beta pruning and LRU allows the use of better heuristics that would be two costly without them.  To use it, run the server and then execute the client passing the player number (1 or 2) as an argument. You can run two clients simultaneosly, one with each player number.

## API

The API is already in development. There is some basic funcionality available through http requests:

* `/jogador`. Returns the number of the player that it's the current turn to play. Returns 0 if the game is over and the opponent won.
* `/tabuleiro`. Returns the current state of the board in the form of a list of lists. Each list represents a column, the value `0` represents an empty space, while `1` represents the first player and `2` the second.
* `/move?player=X&coluna=C&linha=L`. Puts a pice from player X in the columns C and line L. Returns the tuple `(error, msg)`. If `error<0`, `msg` will contain the error. If `error==0`, the movement ended the game and the client won.
* `/reiniciar`. Resets the game, cleaning the board..
* `/ultima_jogada`. Returns the position of the last move made (column, line).
* `/movimentos`. Return a list with all the positions (column, line) where the current player can make a valid move (place a piece or remove opponent piece).
* `/num_movimentos`. Returns the number of movements made since the game started.
