from abc import ABC, abstractmethod

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
    def move(cls): # Upper limits of the playable squares, ex: 9 for tic tac toe (starts at 1)
        raise NotImplementedError

    board: list[
        int]  # Current game, updated after the computer/player plays, not when the computer is trying to make predictions.
    player: int  # Currently playing player.
    depth: int  # Number of level down to go for the heuristic algorithm.

    def __init__(self, first_player, depth):
        self.board = self.init_board
        self.player = first_player
        self.depth = depth

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

    def min_max_heuristic(self, m, depth: int, board):
        """
        Computer is player 1

        :param m: Either -1 or 1, indicates wether to take the min (-1) or the max (1) of the possible outcomes.
        :param depth:
        :param board: Board used to calculate the euristic.
        :return:
        """

        winner = self.check_win(board)
        if winner == 1:
            return 1, 0
        elif winner == 2:
            return -1, 0

        if depth == 0 or 0 not in board:
            return 0, 0

        free = self.get_free_space(board)
        mini = None
        minicoup = []
        maxi = None
        maxicoup = []
        for i in free:
            bp = board.copy()
            self.place_for(int(((1 - m) / 2) + 1), i, bp)
            a, _ = self.min_max_heuristic((-1) * m, depth - 1, bp)

            if mini == None or a <= mini:

                if a == mini:
                    minicoup.append(i)
                else:
                    mini = a
                    minicoup = [i]

            if maxi == None or a >= maxi:

                if a == maxi:
                    maxicoup.append(i)
                else:
                    maxi = a
                    maxicoup = [i]
        if m == -1:
            return mini, self.choose_among(minicoup)
        else:
            return maxi, self.choose_among(maxicoup)

    def play(self):
        winner = 0
        while winner == 0 or 0 not in self.board:
            if self.player == 1:
                _, best = self.min_max_heuristic(1, self.depth, self.board)
                success = self.place_for(1, best, self.board)
                if not success:
                    self.display()
                    raise Exception(f"Problem with the AI : {best} tried to be played but was not succesful.")
            else:
                self.display()
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