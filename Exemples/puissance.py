import minmax
import random

class Puissance4(minmax.GameAbstract):
    @property
    def init_board(cls):
        return [0 for _ in range(7*6)] # 7 colones, 6 lignes

    @property
    def move(cls):
        return 7

    def _get_value(self, i, j, board):
        return board[7*i + j]

    def get_free_space(self, board) -> list[int]:
        return [j for j in range(self.move) if 0 in [self._get_value(i, j, board) for i in range(6)]]

    def check_win(self, board) -> int:
        # (0, 0) is at top right. --> and down
        #
        #
        for i in range(6):
            for j in range(7):
                if i <= 2: # Can check for vertical.
                    value = [self._get_value(a, j, board) for a in range(i, i+4)]
                    if value[0]!= 0 and len(set(value)) == 1:
                        return value[0]
                if j <= 3: # Can check for horizontal.
                    value = [self._get_value(i, a, board) for a in range(j, j + 4)]
                    if value[0] != 0 and len(set(value)) == 1:
                        return value[0]
                if i <= 2 and j <= 3:  # Checks for right diagonal
                    value = [self._get_value(i + a, j + a, board) for a in range(4)]
                    if value[0] != 0 and len(set(value)) == 1:
                        return value[0]

                if i <= 2 and j >= 3: # Checks for right diagonal
                    value = [self._get_value(i+a, j-a, board) for a in range(4)]
                    if value[0] != 0 and len(set(value)) == 1:
                        return value[0]

        return 0


    def place_for(self, player, place, board) -> bool:
        for i in range(5, -1, -1):
            if self._get_value(i, place, board) == 0:
                board[i*7+place] = player
                return True
        return False

    def display(self):
        display = ""

        for i in range(6):
            for j in range(7):
                val = self._get_value(i, j,self.board)
                if val == 1:
                    display += "🟥"
                if val == 2:
                    display += "🟨"
                if val == 0:
                    display+= "⬜"
            display += "\n"
        print(display)

    def choose_among(self, moves):
        return random.choice(moves)

P4 = Puissance4(first_player=2, depthmax=10, initdepth=5, maxtime=7)

P4.play()