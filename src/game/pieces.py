# Imports
from abc import ABC, abstractmethod

# Pieces
class Piece(ABC):
    def __init__(self, colour, side):
        self.x = 0
        self.y = 0
        self.side = side
        self.colour = colour

    @abstractmethod
    def all_moves(self):
        pass
    
    @abstractmethod
    def move(self, move):
        pass

    def update_pos(self, x:int, y:int):
        self.x = x
        self.y = y

# Pawn piece
class Pawn(Piece):
    def __init__(self, colour, side):
        super().__init__(colour, side)
        self.vectors = []

    def all_moves(self):
        pass
    
    def move(self, move):
        pass

# Rook piece
class Rook(Piece):
    def __init__(self, colour, side):
        super().__init__(colour, side)
        self.vectors = []

    def all_moves(self):
        pass
    
    def move(self, move):
        pass

# Knight piece
class Knight(Piece):
    def __init__(self, colour, side):
        super().__init__(colour, side)
        self.vectors = []

    def all_moves(self):
        pass
    
    def move(self, move):
        pass

# Bishop piece
class Bishop(Piece):
    def __init__(self, colour, side):
        super().__init__(colour, side)
        self.vectors = []

    def all_moves(self):
        pass
    
    def move(self, move):
        pass

# Queen piece
class Queen(Piece):
    def __init__(self, colour, side):
        super().__init__(colour, side)
        self.vectors = []

    def all_moves(self):
        pass
    
    def move(self, move):
        pass

# King piece
class King(Piece):
    def __init__(self, colour, side):
        super().__init__(colour, side)
        self.vectors = []

    def all_moves(self):
        pass
    
    def move(self, move):
        pass