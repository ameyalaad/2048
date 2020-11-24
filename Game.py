from Storage import Storage
from Move import Move
import os


class Game:
    """
    The class that keeps track of a Game session
    Each game is represented by a Storage class object
    """

    def __init__(self):
        self.max_score = 0
        self.storage = None

    def new_game(self):
        """
        Starts a new game by creating a Storage object and generates 2 random tiles
        """
        self.storage = Storage()

        # Generate two initial tiles
        self.storage.generate_update()
        self.storage.generate_update()

        # Clean the screen
        os.system('cls' if os.name == 'nt' else 'clear')

    def interactive(self):
        """
        Used to start a user-controlled interactive loop
        This uses the getchar module
        """
        self.game_running = True
        while self.game_running:
            print("Do a move: ", ["w", "a", "s", "d", "n", "u"])
            print(f"Anything else exits...\nScore = {self.storage.get_score()}, High Score = {self.max_score}")

            # fetch the possible outcomes before hand
            scores = self.storage.generate_moves()
            score_val = -1
            self.storage.show_states()
            move = getch()

            # set the current state based on user input
            if move == b'w':
                if scores[0] != -1:
                    self.storage.push_previous_state(self.storage.get_state(), self.storage.get_score())
                    self.storage.set_state(self.storage.get_move_state(0))
                    score_val = scores[0]
            elif move == b'a':
                if scores[1] != -1:
                    self.storage.push_previous_state(self.storage.get_state(), self.storage.get_score())
                    self.storage.set_state(self.storage.get_move_state(1))
                    score_val = scores[1]
            elif move == b"s":
                if scores[2] != -1:
                    self.storage.push_previous_state(self.storage.get_state(), self.storage.get_score())
                    self.storage.set_state(self.storage.get_move_state(2))
                    score_val = scores[2]
            elif move == b"d":
                if scores[3] != -1:
                    self.storage.push_previous_state(self.storage.get_state(), self.storage.get_score())
                    self.storage.set_state(self.storage.get_move_state(3))
                    score_val = scores[3]
            elif move == b"n":
                self.new_game()
            elif move == b"u":
                try:
                    prev_state, prev_score = self.storage.pop_previous_state()
                    self.storage.set_state(prev_state)
                    self.storage.set_score(prev_score)
                except IndexError as error:
                    print("No previous state available. Do a move to undo")
            else:
                self.game_running = False
                print("Exiting...")
                break

            os.system('cls' if os.name == 'nt' else 'clear')

            if score_val == -1:
                print(f"No changes, try another move")
            else:
                self.storage.generate_update()
                new_score = self.storage.get_score() + score_val
                self.storage.set_score(new_score)

                if new_score > self.max_score:
                    self.max_score = new_score

            if self.check_game_over() != 0:
                # TODO : Implement endgame
                print("Press 'n' for a new game, Anything else to exit")
                move = getch()
                if move == b'n':
                    self.new_game()
                else:
                    self.game_running = False
                    break

    def check_game_over(self):
        return self.storage.check_game_over()

    # The following methods may be used by an AI agent to manipulate the Game


def _find_getch():
    """
    Gets a single character from the screen
    Used while a user is playing the Game
    """
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
