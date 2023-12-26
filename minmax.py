from abc import ABC, abstractmethod
import time
import multiprocessing
from multiprocessing import Value
import random
from multiprocessing.shared_memory import SharedMemory
import atexit

def worker(m, depth, bp, val, shared_mem, min_max_heuristic):
    a, best = min_max_heuristic(m * (-1), depth - 1, bp, shared_mem)
    val.value = a


class GameAbstract(ABC):
    """
    Generalization of a min max heuristic algorithm for two player games that can be boiled down to a list of int : 0, 1 and 2 where 0 is an empty square, 1 is the computer and 2 is the player.
    """

    @property
    @abstractmethod
    def init_board(cls):
        raise NotImplementedError

    @property
    @abstractmethod
    def move(cls):  # Upper limits of the playable squares, ex: 9 for tic tac toe (starts at 1)
        raise NotImplementedError

    board: list[
        int]  # Current game, updated after the computer/player plays, not when the computer is trying to make predictions.
    player: int  # Currently playing player.
    depth: int  # Number of level down to go for the heuristic algorithm.

    def __init__(self, first_player, depthmax, initdepth, maxtime):
        self.board = self.init_board
        self.player = first_player
        self.depthmax = depthmax
        self.depth = initdepth
        self.maxtime = maxtime

        self.problem_size = self.get_free_space(self.init_board)
        # Gives an approximation of the problem size.
        # The number of computation done is a O(problem_size^depth) due to the recursive approach.

    def adaptative_depth(self, last_time):
        """
        Adapts the depth parameter by adding +/- 1 to comply with maxtime and depthmax.
        :param last_time:
        :return:
        """
        print(last_time)
        if self.maxtime / (len(self.problem_size)) > last_time and self.depth < self.depthmax:
            print("Increasing depth")
            self.depth += 1
            print(f"New : {self.depth}")
        if last_time > self.maxtime and self.depth > 1:
            print("Decreasing depth")
            self.depth -= 1
            print(f"New : {self.depth}")

    @abstractmethod
    def get_free_space(self, board) -> list[int]:
        """
        Returns the playable moves.
        :return:
        """
        pass

    @abstractmethod
    def check_win(self, board) -> int:
        """
        Returns the number of the winner if there is one, otherwise 0.

        :param board: Not necesseraly the current board.
        :return:
        """
        pass

    @abstractmethod
    def place_for(self, player, place, board) -> bool:
        """
        Plays for the given player at the given place.
        :return: Wether the move could be played.
        """
        pass

    @abstractmethod
    def display(self):
        """
        Displays the current game (stored in self.board) to the console.
        :return:
        """
        pass

    @abstractmethod
    def choose_among(self, moves):
        """
        Chooses the move to plays among a list of move considered all equal.
        May be a random function.
        :param plays:
        :return:
        """

    def min_max_heuristic(self, m, depth: int, board, shared_memory):
        """
        Computer is player 1

        :param m: Either -1 or 1, indicates wether to take the min (-1) or the max (1) of the possible outcomes.
        :param depth:
        :param board: Board used to calculate the euristic.
        :param toplevel: Wether this function was called by itself (False) or by an external function (True).
        :return:
        """
        if shared_memory.buf[0] != 0:
            print("Another process found a forced move.")
            return 0, 0

        winner = self.check_win(board)
        if winner == 1:
            return 1, 0
        elif winner == 2:
            return -1, 0

        if depth == 0 or 0 not in board:
            return 0, 0

        free = self.get_free_space(board)

        value = []
        for i in free:
            bp = board.copy()
            self.place_for(int(((1 - m) / 2) + 1), i, bp)
            a, _ = self.min_max_heuristic((-1) * m, depth - 1, bp, shared_memory)
            # Optimisation alpha beta :
            # -----
            if a == m:  # Valeur maximale/minimale, inutile de calculer d'autres coups possibles.
                return a, i
            # -----
            value.append(a)

        return self._get_extremum(m, value, free)

    def _get_extremum(self, m, value, free):
        if m == 1:
            extremum = max(value)
            coups = [free[i] for i in range(len(value)) if value[i] == extremum]
        else:
            extremum = min(value)
            coups = [free[i] for i in range(len(value)) if value[i] == extremum]

        return extremum, self.choose_among(coups)

    def toplevel(self, m, depth, board):
        if depth == 0:
            raise Exception("'toplevel' call with depth = 0 is not allowed.")

        shared_mem = SharedMemory(name='Mem', create=False)
        shared_mem.buf[0] = 0
        procs = []

        free = self.get_free_space(board)

        values = []
        procs = []
        for i in free:
            bp = board.copy()
            self.place_for(int(((1 - m) / 2) + 1), i, bp)
            val = Value('i', -2)
            values.append(val)
            p = multiprocessing.Process(target=worker, args=(m, depth, bp, val, shared_mem, self.min_max_heuristic))
            procs.append(p)
            p.start()

        # All processes are started.
        while -2 in [i.value for i in values]:
            time.sleep(0.1)
            if m in [i.value for i in values]:
                print(f"Found {m} for , stopping processes")
                for p in procs:
                    p.kill()
                return m, free[[i.value for i in values].index(m)]

        # Here all processes are finished.
        return self._get_extremum(m, [i.value for i in values], free)

    def play(self):
        try:
            sh = SharedMemory("Mem", create=False)
            sh.close()
            sh.unlink()
        except:
            print("Error in deleting memory")
        finally:
            print("Creating mem")
            SharedMemory(name='Mem', size=8, create=True)
        winner = 0

        self.display()
        while winner == 0 or 0 not in self.board:
            if self.player == 1:
                start = time.time()
                a, best = self.toplevel(1, self.depth, self.board)
                if a == 1:
                    print("J'ai gagné !")
                deltat = time.time() - start
                self.adaptative_depth(deltat)

                success = self.place_for(1, best, self.board)
                if not success:
                    self.display()
                    raise Exception(f"Problem with the AI : {best} tried to be played but was not succesful.")
            else:
                place = int(input(f"Place an O (1 to {self.move}) :")) - 1
                success = self.place_for(2, place, self.board)
                if not success:
                    print("You cannot play that, please play again.")
                    continue
            self.player = 3 - self.player

            winner = self.check_win(self.board)
            self.display()

        print("The game has ended.")
        if winner == 0:
            print("No one has won !")
        elif winner == 1:
            print("The computer won...")
        else:
            print(f"You won")


def save():
    sh = SharedMemory("Mem", create=False)
    sh.close()
    sh.unlink()
if __name__ == "__main__":
    atexit.register(save)
