# Imports
from src.game.ui import GameUI
from src.game.game_loop import Chess

# Chess App
def main():
    ui = GameUI()
    mode, colour = ui.show_intro_screen()
    game = Chess(ui, mode, colour)



# Start Game
if __name__ == '__main__':
    main()
