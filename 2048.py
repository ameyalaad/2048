# Imports
import random
import os
from copy import deepcopy
import platform


# Seeding the random number generator for consistent results
# random.seed(42)


def _find_getch():
    try:
        import termios
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch

    # POSIX system. Create and return a getch that manipulates the tty.
    import sys
    import tty

    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    return _getch


getch = _find_getch()

# Game class
# max score, Storage class, GUI(if needed)
# On arrow key -> perform move
# init function -> 2x generate random -> update gui/ print current state
# waitformove -> perform move -> update score -> generate random -> check max score ->update GUI/ print current state
# checkgameover


class Game:
    """The class to keep track of Game sessions"""

    def __init__(self):
        self.max_score = 0
        self.storage = None
        self.moves = ["w", "a", "s", "d", "n"]

    def new_game(self):
        self.storage = Storage()

        # Generate two initial tiles
        self.storage.generate_update()
        self.storage.generate_update()

        # Clean the screen
        os.system('cls' if os.name == 'nt' else 'clear')

        self.loop()

    def loop(self):
        self.game_running = True
        while self.game_running:
            print("Do a move: ", self.moves)
            print(f"Anything else exits...\nScore = {self.storage.get_score()}, High Score = {self.max_score}")

            # fetch the possible outcomes before hand
            scores = self.storage.generate_moves()
            score_val = -1
            self.storage.show_state()
            move = getch()

            # set the current state based on user input
            if move == b'w':
                if scores[0] != -1:
                    self.storage.set_previous_state(self.storage.get_state())
                    self.storage.set_state(self.storage.get_move_state(0))
                    score_val = scores[0]
            elif move == b'a':
                if scores[1] != -1:
                    self.storage.set_previous_state(self.storage.get_state())
                    self.storage.set_state(self.storage.get_move_state(1))
                    score_val = scores[1]
            elif move == b"s":
                if scores[2] != -1:
                    self.storage.set_previous_state(self.storage.get_state())
                    self.storage.set_state(self.storage.get_move_state(2))
                    score_val = scores[2]
            elif move == b"d":
                if scores[3] != -1:
                    self.storage.set_previous_state(self.storage.get_state())
                    self.storage.set_state(self.storage.get_move_state(3))
                    score_val = scores[3]
            elif move == b"n":
                self.new_game()
            else:
                self.game_running = False
                print("Exiting...")
                break

            # TODO: Implement Undo functionality
            # TODO: Possible combinations

            os.system('cls' if os.name == 'nt' else 'clear')

            if score_val == -1:
                print(f"No changes, try another move")
            else:
                self.storage.generate_update()
                new_score = self.storage.get_score() + score_val
                self.storage.set_score(new_score)

                if new_score > self.max_score:
                    self.max_score = new_score

            if self.check_game_over():
                # TODO : Implement endgame
                print("Press 'n' for a new game, Anything else to exit")
                move = getch()
                if move == b'n':
                    self.new_game()
                else:
                    self.game_running = False
                    break

    def check_game_over(self):
        if max(self.storage.get_state()) == 2048:
            print(f"Congratulations!! You Won!\nScore = {self.storage.get_score()}, High Score = {self.max_score}")
            return True

        num_empty_tiles = 0
        for i in range(4):
            for j in range(4):
                if self.storage.state[i][j] == -1:
                    num_empty_tiles += 1

        if num_empty_tiles == 0:
            # checking for merging tiles
            # temporary soln until lookahead is implemented
            # generate moves again and check if all moves_scores = -1?
            for i in range(3):
                for j in range(3):
                    if(self.storage.state[i][j] == self.storage.state[i + 1][j] or self.storage.state[i][j] == self.storage.state[i][j + 1]):
                        return False

            for j in range(3):
                if(self.storage.state[3][j] == self.storage.state[3][j + 1]):
                    return False

            for i in range(3):
                if(self.storage.state[i][3] == self.storage.state[i + 1][3]):
                    return False

            os.system('cls' if os.name == 'nt' else 'clear')
            print("Game Over :(")
            print("Current state:")

            self.storage.show_current_state()

            print(f"Your Score: {self.storage.get_score()}\nHigh Score: {self.max_score}")
            return True

        return False


# Storage Class
# current score, state, previous state, move_states, move_scores
# getstate, getpreviousstate, generaterandom, setpreviousstate, setstate, getscore, setscore
# get_num_empty_tiles, increament_empty_tiles, decreament_empty_tiles
# generate_update -> internally updates current state


class Storage:
    def __init__(self):
        self.score = 0
        self.state = [[-1 for _ in range(4)] for _ in range(4)]
        self.previous_state = None
        self.move_states = [None]*4
        self.move_scores = None

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state

    def get_previous_state(self):
        return self.previous_state

    def set_previous_state(self, new_previous_state):
        self.previous_state = new_previous_state

    def get_move_state(self, move):
        return self.move_states[move]

    def set_move_state(self, move, new_state):
        self.move_states[move] = new_state        

    def get_score(self):
        return self.score

    def set_score(self, new_score):
        self.score = new_score

    def set_move_scores(self, scores):
        self.move_scores = scores

    def generate_update(self):
        """
        Generates a tile in a random location, with a number 2 or 4. Directly updates the state.
        """
        # Generate a tile value (90% chance of 2)
        tile_value = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])

        # Get -1 elements as indices
        empty_indices = []
        for i in range(4):
            for j in range(4):
                if self.state[i][j] == -1:
                    empty_indices.append(i*4+j)

        try:
            location = random.choice(empty_indices)
        except IndexError as error:
            print("No empty tiles available. Game should now end")
            # Implement move, will check the previous state comparision then

            return

        self.state[location//4][location % 4] = tile_value
        # print(self.state)

    def generate_moves(self):
        """
        Generate the 4 possible outcome states
        """
        scores = [-1]*4
        current_state = self.get_state()

        scores[0], new_state = Move.up(current_state)
        self.set_move_state(0, new_state)

        scores[1], new_state = Move.left(current_state)
        self.set_move_state(1, new_state)

        scores[2], new_state = Move.down(current_state)
        self.set_move_state(2, new_state)

        scores[3], new_state = Move.right(current_state)
        self.set_move_state(3, new_state)

        self.move_scores = scores
        return scores

    def show_current_state(self):
        for i in self.state:
            print("\t"*5, end="")
            for j in i:
                if j == -1:
                    print("_\t", end="")
                else:
                    print(f"{j}\t", end="")
            print()

    def show_state(self):
        """Helper function to pretty-print the possible states"""
        # Move up
        for i in self.get_move_state(0):
            print("\t"*5, end="")
            for j in i:
                if j == -1:
                    print("_\t", end="")
                else:
                    print(f"{j}\t", end="")
            print()

        print(f"\t\t\t\t\t\tUp score: {self.score + (0 if self.move_scores[0] == -1 else self.move_scores[0])}")

        print()

        # Move left, current state, right state
        for left, curr, right in zip(self.get_move_state(1), self.state, self.get_move_state(3)):
            # print left
            for j in left:
                if j == -1:
                    print("_\t", end="")
                else:
                    print(f"{j}\t", end="")
            print("\t", end="")
            for j in curr:
                if j == -1:
                    print("_\t", end="")
                else:
                    print(f"{j}\t", end="")
            print("\t", end="")
            for j in right:
                if j == -1:
                    print("_\t", end="")
                else:
                    print(f"{j}\t", end="")
            print()

        tab_ = '\t' if (self.score + (0 if self.move_scores[1] == -1 else self.move_scores[1])) < 1000 else ""
        print(
            f"\tLeft Score: {self.score + (0 if self.move_scores[1] == -1 else self.move_scores[1])}{tab_}\t\t\tScore: {self.score}\t\t\t\tRight Score: {self.score + (0 if self.move_scores[3] == -1 else self.move_scores[3])}")

        print()

        # Move down
        for i in self.get_move_state(2):
            print("\t"*5, end="")
            for j in i:
                if j == -1:
                    print("_\t", end="")
                else:
                    print(f"{j}\t", end="")
            print()

        print(f"\t\t\t\t\t\tDown score: {self.score + (0 if self.move_scores[2] == -1 else self.move_scores[2])}")


# Move Class
# left, right, up, down (input: state 2d-Array)
# Utils: mirror, transpose, move_left
class Move:

    @staticmethod
    def left(state):
        current_state = deepcopy(state)
        valid_move, new_score, new_state = Move.move_left(current_state)
        return (new_score if valid_move else -1), new_state

    @staticmethod
    def right(state):
        """ mirror -> left move """
        current_state = deepcopy(state)
        current_state = Move.mirror(current_state)
        valid_move, new_score, new_state = Move.move_left(current_state)
        new_state = Move.mirror(new_state)
        return (new_score if valid_move else -1), new_state

    @staticmethod
    def up(state):
        """ transpose -> left move """
        current_state = deepcopy(state)
        current_state = Move.transpose(current_state)
        valid_move, new_score, new_state = Move.move_left(current_state)
        new_state = Move.transpose(new_state)
        return (new_score if valid_move else -1), new_state

    @staticmethod
    def down(state):
        """ transpose -> mirror -> left move """
        current_state = deepcopy(state)
        current_state = Move.transpose(current_state)
        current_state = Move.mirror(current_state)
        valid_move, new_score, new_state = Move.move_left(current_state)
        new_state = Move.mirror(new_state)
        new_state = Move.transpose(new_state)
        return (new_score if valid_move else -1), new_state

    @staticmethod
    def move_left(current_state):
        new_state = [[-1]*4 for _ in range(4)]
        score = 0  # change in score
        valid_move = False  # valid if atleast 1 shift operation takes place

        for i in range(0, 4):
            nullIndex = 0  # first null index from left
            for j in range(0, 4):
                if current_state[i][j] != -1:
                    if nullIndex >= 1:
                        # Merge Condition
                        if current_state[i][j] == new_state[i][nullIndex-1]:
                            new_state[i][nullIndex-1] *= 2
                            score += new_state[i][nullIndex-1]
                        else:
                            new_state[i][nullIndex] = current_state[i][j]
                            nullIndex += 1
                    else:
                        new_state[i][nullIndex] = current_state[i][j]
                        nullIndex += 1

                    # Condition for tile shifting
                    if j != nullIndex-1:
                        valid_move = True

        return valid_move, score, new_state

    @staticmethod
    def mirror(state):
        for i in range(4):
            for j in range(2):
                state[i][j], state[i][3-j] = state[i][3-j], state[i][j]
        return state

    @staticmethod
    def transpose(state):
        for i in range(4):
            for j in range(i, 4):
                state[i][j], state[j][i] = state[j][i], state[i][j]
        return state


def test():
    # Use this for your testing purposes
    game = Game()
    game.new_game()


if __name__ == "__main__":
    test()
