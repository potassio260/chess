# Imports
import pygame, numpy
from .pieces import Piece

# Chess Board
class ChessBoard():
    def __init__(self):
        self.SQUARE_SIZE = 80
        self.BOARD_START_X = 0
        self.BOARD_START_Y = 0
            
    def initialize_board(self, player_1):
        # Files and ranks
        files = 'abcdefgh'
        ranks = '12345678'
        
        # Starting position of pieces (from black's perspective)
        starting_pieces = {

            # White pieces
            'a1': Piece('Rook', 'white'), 'b1': Piece('Knight', 'white'), 
            'c1': Piece('Bishop', 'white'), 'd1': Piece('Queen', 'white'), 
            'e1': Piece('King', 'white'), 'f1': Piece('Bishop', 'white'), 
            'g1': Piece('Knight', 'white'), 'h1': Piece('Rook', 'white'),
            'a2': Piece('Pawn', 'white'), 'b2': Piece('Pawn', 'white'), 
            'c2': Piece('Pawn', 'white'), 'd2': Piece('Pawn', 'white'), 
            'e2': Piece('Pawn', 'white'), 'f2': Piece('Pawn', 'white'), 
            'g2': Piece('Pawn', 'white'), 'h2': Piece('Pawn', 'white'),

            # Black pieces
            'a7': Piece('Pawn', 'black'), 'b7': Piece('Pawn', 'black'), 
            'c7': Piece('Pawn', 'black'), 'd7': Piece('Pawn', 'black'), 
            'e7': Piece('Pawn', 'black'), 'f7': Piece('Pawn', 'black'), 
            'g7': Piece('Pawn', 'black'), 'h7': Piece('Pawn', 'black'),
            'a8': Piece('Rook', 'black'), 'b8': Piece('Knight', 'black'), 
            'c8': Piece('Bishop', 'black'), 'd8': Piece('Queen', 'black'), 
            'e8': Piece('King', 'black'), 'f8': Piece('Bishop', 'black'), 
            'g8': Piece('Knight', 'black'), 'h8': Piece('Rook', 'black')

        }
        
        # Flip the board if playing as black
        if player_1 == 'white':
            ranks = ranks[::-1] 
            files = files[::-1]
        
        chessboard = {}
        for rank_index, rank in enumerate(ranks):
            for file_index, file in enumerate(files):
                square_name = f'{file}{rank}'
                x = self.BOARD_START_X + file_index * self.SQUARE_SIZE
                y = self.BOARD_START_Y + rank_index * self.SQUARE_SIZE
                chessboard[square_name] = {
                    'square': pygame.Rect(x, y, self.SQUARE_SIZE, self.SQUARE_SIZE),
                    'piece': starting_pieces.get(square_name, None)
                }
        return chessboard