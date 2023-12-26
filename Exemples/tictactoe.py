import minmax
import random

class Tictactoe(minmax.GameAbstract):
    @property
    def move(cls):
        return 9

    @property
    def init_board(cls):

        return [0 for _ in range(9)]

    win_pos = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

    def check_win(self, board) -> int:
        for i in self.win_pos:
            a = board[i[0]]
            if board[i[1]] == a == board[i[2]] and a!= 0:
                return a
        return 0

    def place_for(self, player, place, board) -> bool:
        if board[place] != 0:
            return False
        board[place] = player
        return True

    def display(self):
        display = ""
        for i in range(3):
            for j in range(3):
                a = self.board[3 * i + j]
                if a == 0:
                    display += "#"
                elif a == 1:
                    display += "X"
                else:
                    display += "O"
            display += "\n"
        print(display)

    def choose_among(self, moves):
        if moves == []:
            raise Exception("No move available.")
        return random.choice(moves)

    def get_free_space(self, board) -> list[int]:
        return [i for i in range(len(board)) if board[i] == 0]

if __name__ == "__main__":
    t = Tictactoe(first_player=2, depthmax=1, initdepth=1, maxtime=1)
    t.play()