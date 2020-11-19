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

        # Print out the state
        self.storage.show_state()

        self.loop()

    def loop(self):
        self.game_running = True
        while self.game_running:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.storage.show_state()
            print("Do a move: ", self.moves)
            print(f"Anything else exits...\nScore = {self.storage.get_score()}, High Score = {self.max_score}")
            move = getch()

            # fetch the possible outcomes before hand
            scores = self.storage.generate_moves()
            score_val = -1

            #set the current state based on user input
            if move == b'w':
                if scores[0]!=-1:
                    self.storage.set_state(self.storage.get_up_state())
                    score_val = scores[0]
            elif move == b'a':
                if scores[1]!=-1:
                    self.storage.set_state(self.storage.get_left_state())
                    score_val = scores[1]
            elif move == b"s":
                if scores[2]!=-1:
                    self.storage.set_state(self.storage.get_down_state())
                    score_val = scores[2]
            elif move == b"d":
                if scores[3]!=-1:
                    self.storage.set_state(self.storage.get_right_state())
                    score_val = scores[3]
            elif move == b"n":
                self.new_game()
            else:
                self.game_running = False
                break

            # TODO: Implement Undo functionality
            # TODO: Possible combinations

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
            for i in range(3): 
                for j in range(3): 
                    if(self.storage.state[i][j]== self.storage.state[i + 1][j] or self.storage.state[i][j]== self.storage.state[i][j + 1]): 
                        return False

            for j in range(3): 
                if(self.storage.state[3][j]== self.storage.state[3][j + 1]): 
                    return False
        
            for i in range(3): 
                if(self.storage.state[i][3]== self.storage.state[i + 1][3]): 
                    return False

            os.system('cls' if os.name == 'nt' else 'clear')
            print("Game Over :(")

            self.storage.show_state()
            return True

        return False


# Storage Class
# current score, state, previous state, max_tile, num_empty_tiles
# getstate, getpreviousstate, generaterandom, setpreviousstate, setstate, getscore, setscore, get_max_tile, set_max_tile
# get_num_empty_tiles, increament_empty_tiles, decreament_empty_tiles
# generate_update -> internally updates current state


class Storage:
    def __init__(self):
        self.score = 0
        self.state = [[-1 for _ in range(4)] for _ in range(4)]
        self.previous_state = None
        self.left_state = None
        self.right_state = None
        self.up_state = None
        self.down_state = None

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state

    def get_previous_state(self):
        return self.previous_state

    def set_previous_state(self, new_previous_state):
        self.previous_state = new_previous_state

    def get_left_state(self):
        return self.left_state

    def set_left_state(self, new_left_state):
        self.left_state = new_left_state

    def get_right_state(self):
        return self.right_state

    def set_right_state(self, new_right_state):
        self.right_state = new_right_state   

    def get_up_state(self):
        return self.up_state

    def set_up_state(self, new_up_state):
        self.up_state = new_up_state

    def get_down_state(self):
        return self.down_state

    def set_down_state(self, new_down_state):
        self.down_state = new_down_state             

    def get_score(self):
        return self.score

    def set_score(self, new_score):
        self.score = new_score

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
        self.set_up_state(new_state)

        scores[1], new_state = Move.left(current_state)
        self.set_left_state(new_state)

        scores[2], new_state = Move.down(current_state)
        self.set_down_state(new_state)

        scores[3], new_state = Move.right(current_state)
        self.set_right_state(new_state)
        return scores    

    def show_state(self):
        """Helper function to pretty-print the state"""
        for i in self.state:
            for j in i:
                if j == -1:
                    print("_\t", end="")
                else:
                    print(f"{j}\t", end="")
            print()


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
        valid_move, new_score, new_state =  Move.move_left(current_state)
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
            state[i][0],state[i][3] = state[i][3], state[i][0]
            state[i][1],state[i][2] = state[i][2], state[i][1]
        return state    
              
    @staticmethod
    def transpose(state):
        new_mat = [] 
        for i in range(4):
            for j in range(i,4):
                state[i][j], state[j][i] = state[j][i], state[i][j]
        return state                                


def test():
    # Use this for your testing purposes
    game = Game()
    game.new_game()


if __name__ == "__main__":
    test()
