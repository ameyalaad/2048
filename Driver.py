from Game import Game, getch
import random

def main():
    game = Game()
    game.new_game()
    moves = ['up', 'left', 'down', 'right']
    while(game.get_sum() != 8):
        while(game.get_sum() < 8):
            game.play_move(random.choice(moves))
        while(game.get_sum() > 8):
            game.play_move('undo')    


if __name__ == "__main__":
    main()
