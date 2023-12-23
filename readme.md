# MinMax

Defines an abstract class that can be used to quickly implement a minmax algorithm to a game. The algorithm has an adaptative depth feature to control the time it takes to compute its next move.


## Game requirements


- Two player game.
- Describable by a list of player positions (and empty places)

## How to implement
The GameAbstract class must be inherited from in a new specific class for the game. The following methods must be defined : 
- `get_free_space(self, board) -> list[int]` : Returns all the playable squares.
- `check_win(self, board) -> int` : Returns the number of the winner if there is one, otherwise 0.
- `place_for(self, player, place, board) -> bool` : Plays for the given player at the given place and returns True if the move was actually possible.
- `display(self)` : Displays the game.
- `choose_among(self, moves)` : Chooses the move to plays among a list of move considered all equal. May be a random function.

Some of those functions don't receive the `board` argument, it means the board that need to be considered is `self.board`.

## Heuristic

Currently, the heuristic for a given situation if : 
- 1 if the computer wins
- -1 if the player wins
- 0 otherwise
