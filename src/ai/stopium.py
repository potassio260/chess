# Imports
from abc import ABC, abstractmethod
import random

PIECE_SQUARE_TABLES = {
    "Pawn": [
        [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [ 5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
        [ 1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
        [ 0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
        [ 0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
        [ 0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
        [ 0.5,  1.0,  1.0, -2.0, -2.0,  1.0,  1.0,  0.5],
        [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
    ],
    "Knight": [
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
        [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
        [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
        [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
        [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
        [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
        [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
    ],
    "Bishop": [
        [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
        [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
        [-1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
        [-1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
        [-1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
        [-1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
        [-1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
        [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
    ],
    "Rook": [
        [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [ 0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
        [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
        [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
        [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
        [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
        [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
        [ 0.0,  0.0,  0.0,  0.5,  0.5,  0.0,  0.0,  0.0],
    ],
    "Queen": [
        [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
        [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
        [-1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
        [-0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
        [ 0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
        [-1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
        [-1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
        [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
    ],
    "King": [
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
        [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
        [ 2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0],
        [ 2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0],
    ],
}

MATE = 10000
TOTAL_MATERIAL = 390
END_GAME = 15

# Bot class
class Bot(ABC):
    def __init__(self):
        self.piece_cost = {
            "Pawn": 10,
            "Rook": 50,
            "Knight": 30,
            "Bishop": 30,
            "Queen": 90,
            "King": 1000
        }
            
    @abstractmethod
    def generate_move(self, possible_moves, board, turn, game):
        pass

    # Which piece a promoting pawn turns into: 'q', 'n', 'b' or 'r'
    # Override this in a bot to pick something other than a queen
    def choose_promotion(self, board, targetSquare, turn, game):
        return 'q'

    def evaluate_move(self):
        pass

    def loss_function(self):
        pass
    
    def cross_entropy(self):
        pass
    
    
class Stopium(Bot):
    def __init__(self, depth=4):
        Bot.__init__(self)
        self.depth = depth
        self.turn_count = 0

    def generate_move(self, possible_moves, board, turn, game, turn_count):
        # Update turn counter
        self.turn_count = turn_count
        print(self.turn_count)

        # The root IS the live position, so the game's own state is correct here
        position = (board, turn, game.en_passant_square, game.castling_rights)

        best_move = None
        alpha = float('-inf')
        beta  = float('inf')

        for sourceSquare, targetSquare in possible_moves:
            after = self.play(sourceSquare, targetSquare, position, game)
            # after our move it is their turn, so their best score is our worst
            score = -self.search(after, self.depth - 1, game, -beta, -alpha)

            if score >= beta:
                return beta                         
            if score > alpha:
                alpha = score
                best_move = (sourceSquare, targetSquare)

        if best_move is None:
            best_move = random.choice(possible_moves)

        return best_move

    # Returns a SCORE, always from the point of view of whoever is to move
    def search(self, position, depth, game, alpha, beta, own_material = TOTAL_MATERIAL):
        board, turn, en_passant, castling = position
        possible_moves = game.all_possible_moves(turn, board, en_passant, castling) # TO-DO -> also counts total material + optimize this to be as efficient as possible 
        turn_count = self.turn_count + (self.depth - depth)

        # Calculate new value after decay
        mate_score = (own_material // TOTAL_MATERIAL) * MATE - turn_count
        # No legal moves: we are either mated or stalemated
        if not possible_moves:
            if game.is_in_check(turn, board, en_passant, castling):
                return -mate_score 
            return 0

        if depth == 0:
            return self.evaluate_board(board, turn, game)

        for sourceSquare, targetSquare in possible_moves:
            after = self.play(sourceSquare, targetSquare, position, game)
            score = -self.search(after, depth - 1, game, -beta, -alpha)
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score 

        return alpha

    # One position in, one position out - the only place a board is built
    def play(self, sourceSquare, targetSquare, position, game):
        board, turn, en_passant, castling = position

        new_board, new_en_passant, new_castling = game.simulate_move(sourceSquare, targetSquare, board, en_passant, castling)

        next_turn = "black" if turn == "white" else "white"
        return (new_board, next_turn, new_en_passant, new_castling)

    # Material on the whole board, positive meaning good for `turn`
    def evaluate_board(self, board, turn, game):
        score = 0
        for pos, square_data in board.items():
            piece = square_data['piece']
            if piece is None:
                continue
            file, rank = game.square_to_coords(pos)  
            row = 7 - rank if piece.colour == 'white' else rank
            value = self.piece_cost[piece.piece_type] + PIECE_SQUARE_TABLES[piece.piece_type][row][file]

            if piece.colour == turn:
                score += value
            else:
                score -= value

        return score
    
    
