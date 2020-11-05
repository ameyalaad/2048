# Imports
import random


# Seeding the random number generator for consistent results
# random.seed(42)


# Game class
# max score, Storage class, GUI(if needed)
# On arrow key -> perfoem move
# init function -> 2x generate random -> update gui/ print current state
# waitformove -> perform move -> update score -> generate random -> check max score ->update GUI/ print current state
# checkgameover
class Game:
    """The class to keep track of Game sessions"""

    def __init__(self):
        self.max_score = 0
        self.storage = None
        self.moves = ["Up", "Down", "Left", "Right"]

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
            print("Do a move: ", self.moves)
            print("Anything else exits")
            move = input()

            if move == "Up":
                Move.up(self.storage)
            elif move == "Left":
                Move.left(self.storage)
            elif move == "Down":
                Move.down(self.storage)
            elif move == "Right":
                Move.right(self.storage)
            else:
                self.game_running = False
                break

            self.storage.generate_update()
            self.storage.show_state()

# Storage Class
# current score, state, previous state
# getstate, getpreviousstate, generaterandom, setpreviousstate, setstate, getscore, setscore
# generaterandom -> internally updates current state


class Storage:
    def __init__(self):
        self.score = 0
        self.state = [[-1 for _ in range(4)] for _ in range(4)]
        self.previous_state = None

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state

    def get_previous_state(self):
        return self.previous_state

    def set_previous_state(self, new_previous_state):
        self.previous_state = new_previous_state

    def get_score(self):
        return self.score

    def set_score(self, new_score):
        self.score = new_score

    def generate_update(self):
        """
        Generates a tile in a random location, with a number 2 or 4. Directly updates the state.
        """
        # Generate a tile value
        tile_value = 2 * random.randint(1, 2)

        # Get -1 elements as indices
        empty_indices = []
        for i in range(4):
            for j in range(4):
                if self.state[i][j] == -1:
                    empty_indices.append(i*4+j)

        location = random.choice(empty_indices)

        self.state[location//4][location % 4] = tile_value

        # print(self.state)

    def show_state(self):
        """Helper function to pretty-print the state"""
        print(self.state[0])
        print(self.state[1])
        print(self.state[2])
        print(self.state[3])


# Move Class
# left, right, up, down (inputs storage class), undo
class Move:
    @staticmethod
    def left(storage):
        return

    @staticmethod
    def up(storage):
        return

    @staticmethod
    def right(storage):
        return

    @staticmethod
    def down(storage):
        return


def test():
    # Use this for your testing purposes
    game = Game()
    game.new_game()


if __name__ == "__main__":
    test()
