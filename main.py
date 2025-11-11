import arcade
from game_window import GameView
from player import Player

SCALE = 200

def main():
    player = Player(SCALE)
    window = GameView(player) 
    arcade.run()

if __name__ == "__main__":
    main()