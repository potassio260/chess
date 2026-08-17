# Imports
from abc import ABC, abstractmethod
import torch, random

# Bot class
class Bot(ABC):
    def __init__(self):
            self.piece_cost = {
                "Pawn": 1,
                "Rook": 5,
                "Knight": 3,
                "Bishop": 3,
                "Queen": 9,
                "King": 100
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
    
class RandoBot(Bot):
    def __init__(self):
            super().__init__()
            
    def generate_move(self, possible_moves, board, turn, game):
        (sourceSquare, targetSquare) = random.choice(possible_moves)
        print(sourceSquare, targetSquare)
        return sourceSquare, targetSquare

class ValueBot(Bot):
    def __init__(self):
            super().__init__()
            
    def generate_move(self, possible_moves, board, turn, game):
        best_move = None
        best_value = 0

        for sourceSquare, targetSquare in possible_moves:
            captured = board[targetSquare]['piece']
            if captured is None:
                continue

            value = self.piece_cost[captured.piece_type]
            if value > best_value:
                best_value = value
                best_move = (sourceSquare, targetSquare)

        # Nothing to capture, so just play something legal
        if best_move is None:
            best_move = random.choice(possible_moves)

        return best_move

class SelfAwareBot(Bot):
    
    def __init__(self):
        super().__init__()
        
    # future sight -> repeat twice, get value for current moves, recursive
    def generate_move(self, possible_moves, board, turn, game):
        best_move = None
        best_value = float('-inf')

        for sourceSquare, targetSquare in possible_moves:
            value = self.evaluate_move(targetSquare, board)
            loss = self.loss_function(sourceSquare, targetSquare, board, turn, game)
            valueSum = value - loss

            if valueSum > best_value:
                best_value = valueSum
                best_move = (sourceSquare, targetSquare)

        # Only reachable if there were no moves to choose from
        if best_move is None:
            best_move = random.choice(possible_moves)

        return best_move

    def loss_function(self, sourceSquare, targetSquare, board, turn, game):
        best_value = 0

        # simulate_move returns a new position, it does not change ours
        new_board, new_en_passant, new_castling = game.simulate_move(sourceSquare, targetSquare, board)

        # Change turn
        turn = "black" if turn == "white" else "white"

        possible_moves = game.all_possible_moves(turn, new_board, new_en_passant, new_castling)

        for replySource, replyTarget in possible_moves:
            value = self.evaluate_move(replyTarget, new_board)
            if value > best_value:
                best_value = value

        return best_value

    def evaluate_move(self, targetSquare, board):
        captured = board[targetSquare]['piece']
        if captured is None:
            value = 0
        else:
            value = self.piece_cost[captured.piece_type]

        return value

MATE = 10000


class FutureSightBot(Bot):
    def __init__(self, depth=3):
        super().__init__()
        self.depth = depth

    # The game asks for a move, so this is the only method that returns one
    def generate_move(self, possible_moves, board, turn, game):
        # The root IS the live position, so the game's own state is correct here
        position = (board, turn, game.en_passant_square, game.castling_rights)

        best_move = None
        best_score = float('-inf')

        for sourceSquare, targetSquare in possible_moves:
            after = self.play(sourceSquare, targetSquare, position, game)
            # after our move it is their turn, so their best score is our worst
            score = -self.search(after, self.depth - 1, game)

            if score > best_score:
                best_score = score
                best_move = (sourceSquare, targetSquare)

        if best_move is None:
            best_move = random.choice(possible_moves)

        return best_move

    # Returns a SCORE, always from the point of view of whoever is to move
    def search(self, position, depth, game):
        board, turn, en_passant, castling = position
        possible_moves = game.all_possible_moves(turn, board, en_passant, castling)

        # No legal moves: we are either mated or stalemated
        if not possible_moves:
            if game.is_in_check(turn, board, en_passant, castling):
                return -MATE
            return 0

        if depth == 0:
            return self.evaluate_board(board, turn)

        best_score = float('-inf')
        for sourceSquare, targetSquare in possible_moves:
            after = self.play(sourceSquare, targetSquare, position, game)
            score = -self.search(after, depth - 1, game)
            if score > best_score:
                best_score = score

        return best_score

    # One position in, one position out - the only place a board is built
    def play(self, sourceSquare, targetSquare, position, game):
        board, turn, en_passant, castling = position

        new_board, new_en_passant, new_castling = game.simulate_move(
            sourceSquare, targetSquare, board, en_passant, castling)

        next_turn = "black" if turn == "white" else "white"
        return (new_board, next_turn, new_en_passant, new_castling)

    # Material on the whole board, positive meaning good for `turn`
    def evaluate_board(self, board, turn):
        score = 0
        for square_data in board.values():
            piece = square_data['piece']
            if piece is None:
                continue

            if piece.colour == turn:
                score += self.piece_cost[piece.piece_type]
            else:
                score -= self.piece_cost[piece.piece_type]

        return score