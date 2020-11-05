# Imports
import random
import os
from copy import deepcopy


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
            # os.system("cls")
            self.storage.show_state()
            print("Do a move: ", self.moves)
            print(f"Anything else exits...\nScore = {self.storage.get_score()}, High Score = {self.max_score}")
            move = input()

            if move == "Up":
                score_val = Move.up(self.storage)
            elif move == "Left":
                score_val = Move.left(self.storage)
            elif move == "Down":
                score_val = Move.down(self.storage)
            elif move == "Right":
                score_val = Move.right(self.storage)
            elif move == "newgame":
                self.new_game()
            else:
                self.game_running = False
                break

            # TODO: Implement Undo functionality
            # TODO: Implement newgame functionality

            if self.storage.get_previous_state() == self.storage.get_state():
                # self.game_over()
                print(f"No changes, try another move")

            if score_val != -1:
                self.storage.generate_update()
                new_score = self.storage.get_score() + score_val
                self.storage.set_score(new_score)

                if new_score > self.max_score:
                    self.max_score = new_score


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

        try:
            location = random.choice(empty_indices)
        except IndexError as error:
            print("No empty tiles available. Game should now end")
            # Implement move, will check the previous state comparision then
            return

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
        storage.set_previous_state(deepcopy(storage.get_state()))
        score = 0  # change in score
        valid_move = False  # valid if atleast 1 shift operation takes place
        for i in range(0, 4):
            nullIndex = 0  # first null index from left
            lastMerge = 0  # index of last merge operation
            for j in range(0, 4):
                if storage.state[i][j] != -1:
                    if nullIndex >= 1:
                        # Merge Condition
                        if storage.state[i][j] == storage.state[i][nullIndex-1] and nullIndex > lastMerge:
                            storage.state[i][nullIndex-1] *= 2
                            score += 2*storage.state[i][j]
                            lastMerge = nullIndex
                        else:
                            storage.state[i][nullIndex] = storage.state[i][j]
                            nullIndex += 1
                    else:
                        storage.state[i][nullIndex] = storage.state[i][j]
                        nullIndex += 1

                    # Condition for tile shifting
                    if j != nullIndex-1:
                        storage.state[i][j] = -1
                        valid_move = True

        return score if valid_move else -1

    @staticmethod
    def up(storage):
        storage.set_previous_state(deepcopy(storage.get_state()))
        score = 0  # change in score
        valid_move = False  # valid if atleast 1 shift operation takes place
        for i in range(0, 4):
            nullIndex = 0  # first null index from top
            lastMerge = 0  # index of last merge operation
            for j in range(0, 4):
                if storage.state[j][i] != -1:
                    if nullIndex >= 1:
                        # Merge Condition
                        if storage.state[j][i] == storage.state[nullIndex-1][i] and nullIndex > lastMerge:
                            storage.state[nullIndex-1][i] *= 2
                            score += 2*storage.state[j][i]
                            lastMerge = nullIndex
                        else:
                            storage.state[nullIndex][i] = storage.state[j][i]
                            nullIndex += 1
                    else:
                        storage.state[nullIndex][i] = storage.state[j][i]
                        nullIndex += 1

                    # Condition for tile shifting
                    if j != nullIndex-1:
                        storage.state[j][i] = -1
                        valid_move = True

        return score if valid_move else -1

    @staticmethod
    def right(storage):
        storage.set_previous_state(deepcopy(storage.get_state()))
        score = 0  # change in score
        valid_move = False  # valid if atleast 1 shift operation takes place
        for i in range(0, 4):
            nullIndex = 3  # first null index from right
            lastMerge = 3  # index of last merge operation
            for j in reversed(range(0, 4)):
                if storage.state[i][j] != -1:
                    if nullIndex <= 2:
                        # Merge Condition
                        if storage.state[i][j] == storage.state[i][nullIndex+1] and nullIndex < lastMerge:
                            storage.state[i][nullIndex+1] *= 2
                            score += 2*storage.state[i][j]
                            lastMerge = nullIndex
                        else:
                            storage.state[i][nullIndex] = storage.state[i][j]
                            nullIndex -= 1
                    else:
                        storage.state[i][nullIndex] = storage.state[i][j]
                        nullIndex -= 1

                    # If tiles were shifted mark original positions as -1
                    if j != nullIndex+1:
                        storage.state[i][j] = -1
                        valid_move = True

        return score if valid_move else -1

    @staticmethod
    def down(storage):
        storage.set_previous_state(deepcopy(storage.get_state()))
        score = 0  # change in score
        valid_move = False  # valid if atleast 1 shift operation takes place
        for i in range(0, 4):
            nullIndex = 3  # first null index from bottom
            lastMerge = 3  # index of last merge operation
            for j in reversed(range(0, 4)):
                if storage.state[j][i] != -1:
                    if nullIndex <= 2:
                        # Merge Condition
                        if storage.state[j][i] == storage.state[nullIndex+1][i] and nullIndex < lastMerge:
                            storage.state[nullIndex+1][i] *= 2
                            score += 2*storage.state[j][i]
                            lastMerge = nullIndex
                        else:
                            storage.state[nullIndex][i] = storage.state[j][i]
                            nullIndex -= 1
                    else:
                        storage.state[nullIndex][i] = storage.state[j][i]
                        nullIndex -= 1

                    # Condition for tile shifting
                    if j != nullIndex+1:
                        storage.state[j][i] = -1
                        valid_move = True

        return score if valid_move else -1


def test():
    # Use this for your testing purposes
    game = Game()
    game.new_game()


if __name__ == "__main__":
    test()
