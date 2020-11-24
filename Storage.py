from Move import Move
import random


class Storage:
    """
    This class stores all necessary information for one Game.
    """

    def __init__(self):
        self._score = 0
        self._state = [[-1 for _ in range(4)] for _ in range(4)]
        self._previous_states = []
        self._move_states = [None]*4  # [Up, Left, Down, Right]
        self._move_scores = None

    def get_state(self):
        return self._state

    def set_state(self, new_state):
        self._state = new_state

    def push_previous_state(self, state, score):
        self._previous_states.append((state, score))

    def pop_previous_state(self):
        return self._previous_states.pop()   

    def get_move_state(self, move):
        return self._move_states[move]

    def set_move_state(self, move, new_state):
        self._move_states[move] = new_state

    def get_score(self):
        return self._score

    def set_score(self, new_score):
        self._score = new_score

    def set_move_scores(self, scores):
        self._move_scores = scores

    def get_sum_tiles(self):
        _sum = 0
        for x in self._state:
            for j in x:
                if j>0:
                    _sum += j
        return _sum            

    def get_max_tiles(self):
        return max([max(x) for x in self._state])

    def get_max_tiles_attainable(self):
        return max([max(x) for move in self._move_states for x in move])

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
                if self._state[i][j] == -1:
                    empty_indices.append(i*4+j)

        try:
            location = random.choice(empty_indices)
        except IndexError as error:
            print("No empty tiles available. Game should now end")
            # Implement move, will check the previous state comparision then

            return

        self._state[location//4][location % 4] = tile_value
        # print(self._state)

    def generate_moves(self):
        """
        Generate the 4 possible outcome states
        Uses the Move class to set itself up
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

        self._move_scores = scores
        return scores

    def show_current_state(self):
        """Helper function to pretty-print the current states"""
        for i in self._state:
            print("\t"*5, end="")
            for j in i:
                if j == -1:
                    print("_\t", end="")
                else:
                    print(f"{j}\t", end="")
            print()

    def show_states(self):
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

        print(f"\t\t\t\t\t\tUp score: {self._score + (0 if self._move_scores[0] == -1 else self._move_scores[0])}")

        print()

        # Move left, current state, right state
        for left, curr, right in zip(self.get_move_state(1), self._state, self.get_move_state(3)):
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

        tab_ = '\t' if (self._score + (0 if self._move_scores[1] == -1 else self._move_scores[1])) < 1000 else ""
        print(
            f"\tLeft Score: {self._score + (0 if self._move_scores[1] == -1 else self._move_scores[1])}{tab_}\t\t\tScore: {self._score}\t\t\t\tRight Score: {self._score + (0 if self._move_scores[3] == -1 else self._move_scores[3])}")

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

        print(f"\t\t\t\t\t\tDown score: {self._score + (0 if self._move_scores[2] == -1 else self._move_scores[2])}")

    def check_game_over(self):
        """
        Checks and returns: 
            0 - Game Not Over
            1 - Game Won
            2 - Game Lost
        """
        if self.get_max_tiles() == 2048:
            return 1

        num_empty_tiles = 0
        for i in range(4):
            for j in range(4):
                if self._state[i][j] == -1:
                    num_empty_tiles += 1

        if num_empty_tiles == 0:
            # checking for merging tiles
            for i in range(3):
                for j in range(3):
                    if(self._state[i][j] == self._state[i + 1][j] or self._state[i][j] == self._state[i][j + 1]):
                        return 0

            for j in range(3):
                if(self._state[3][j] == self._state[3][j + 1]):
                    return 0

            for i in range(3):
                if(self._state[i][3] == self._state[i + 1][3]):
                    return 0
            return 2
        return 0
