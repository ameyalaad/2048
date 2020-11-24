from copy import deepcopy


class Move:
    """
    This class deals with the movement of pieces around the board. The Game class passes inputs from the Storage class to this class 
    """
    @staticmethod
    def left(state):
        """
        Make a left move
        left_move
        """
        current_state = deepcopy(state)
        valid_move, new_score, new_state = Move._move_left(current_state)
        return (new_score if valid_move else -1), new_state

    @staticmethod
    def right(state):
        """
        Make a right move
        mirror -> left move 
        """
        current_state = deepcopy(state)
        current_state = Move._mirror(current_state)
        valid_move, new_score, new_state = Move._move_left(current_state)
        new_state = Move._mirror(new_state)
        return (new_score if valid_move else -1), new_state

    @staticmethod
    def up(state):
        """
        Make the up move
        transpose -> left move 
        """
        current_state = deepcopy(state)
        current_state = Move._transpose(current_state)
        valid_move, new_score, new_state = Move._move_left(current_state)
        new_state = Move._transpose(new_state)
        return (new_score if valid_move else -1), new_state

    @staticmethod
    def down(state):
        """ 
        Make the down move
        transpose -> mirror -> left move 
        """
        current_state = deepcopy(state)
        current_state = Move._transpose(current_state)
        current_state = Move._mirror(current_state)
        valid_move, new_score, new_state = Move._move_left(current_state)
        new_state = Move._mirror(new_state)
        new_state = Move._transpose(new_state)
        return (new_score if valid_move else -1), new_state

    @staticmethod
    def _move_left(current_state):
        """
        The actual code that merges the blocks in a "left move"
        This function will never be called from outside the Move class
        """
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
    def _mirror(state):
        """
        Returns the mirror of the passed state
        This function will never be called from outside the Move class
        """
        for i in range(4):
            for j in range(2):
                state[i][j], state[i][3-j] = state[i][3-j], state[i][j]
        return state

    @staticmethod
    def _transpose(state):
        """
        Returns the transpose of the passed state
        This function will never be called from outside the Move class
        """
        for i in range(4):
            for j in range(i, 4):
                state[i][j], state[j][i] = state[j][i], state[i][j]
        return state
