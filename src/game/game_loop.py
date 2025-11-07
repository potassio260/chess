# Imports
from .ui import GameUI
from .board import ChessBoard
import pygame

# Chess 
class Chess():
    def __init__(self, ui:GameUI, mode:str, colour:str):
        # UI
        self.ui = ui

        # Initialize game values
        self.player_turn = 'white'
        self.checkmate = False
        self.stalemate = False
        self.check = False
        self.move_history = []
        self.mode = mode
        self.player_colour = colour

        # create board
        self.chessboard = ChessBoard().initialize_board(colour)
        self.ui.update_screen(board=self.chessboard)
        pygame.display.update()

        # start mode
        self.mainloop()

    def mainloop(self):
        while not self.checkmate and not self.stalemate:
            is_valid_move = False
            while not is_valid_move:
                # Check for checkmate or stalemate
                if self.is_game_over():
                    quit()
                
                # check who is next to move
                if self.player_colour == self.player_turn: 
                    # Human move
                    self.all_possible_moves(colour = self.player_turn, board=self.chessboard)
                    sourceSquare, targetSquare = self.ui.run(board=self.chessboard, turn=self.player_turn)
                    if sourceSquare and targetSquare:
                        is_valid_move = self.validate_move(sourceSquare, targetSquare)

                else:
                    match self.mode:
                        case 'local':
                            # Human move
                            self.all_possible_moves(colour = self.player_turn, board=self.chessboard)
                            sourceSquare, targetSquare = self.ui.run(board=self.chessboard, turn=self.player_turn)
                            if sourceSquare and targetSquare:
                                is_valid_move = self.validate_move(sourceSquare, targetSquare)

                        case 'multiplayer':
                            pass

                        case 'bot':
                            pass
                        
            # Save move in history
            self.move_history.append((sourceSquare, targetSquare))
            
            # Change turn
            self.player_turn = "black" if self.player_turn == "white" else "white"
            
            # Update interface
            self.ui.update_screen(board=self.chessboard)
            pygame.display.update()

    def is_game_over(self):
        return False
    
    def all_possible_moves(self, colour, board):
        pass

    def validate_move(self, sourceSquare, targetSquare):
        pass

    