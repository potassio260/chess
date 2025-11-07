import pygame

class Piece():
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour
        self.has_moved = False
        
        # Cargar imagen según tipo de pieza
        piece_images = {
            "white": { 
                "Pawn": r"assets\pawn_white.png",
                "Rook": r"assets\rook_white.png",
                "Knight": r"assets\knight_white.png",
                "Bishop": r"assets\bishop_white.png",
                "Queen": r"assets\queen_white.png",
                "King": r"assets\king_white.png"
            },
            "black": {
                "Pawn": r"assets\pawn_black.png",
                "Rook": r"assets\rook_black.png",
                "Knight": r"assets\knight_black.png",
                "Bishop": r"assets\bishop_black.png",
                "Queen": r"assets\queen_black.png",
                "King": r"assets\king_black.png"
            }
        }
        
        try:
            self.img = pygame.image.load(piece_images[colour][name])
        except (KeyError, pygame.error) as e:
            try:
                fallback_img = r"assets\pawn_" + colour.lower() + ".png"
                self.img = pygame.image.load(fallback_img)
            except pygame.error:
                self.img = pygame.Surface((70, 70))
                self.img.fill((255, 0, 0) if colour == "White" else (0, 0, 0))
            print(f"Advertencia: No se pudo cargar la imagen para {colour} {name}: {e}")
            
        self.hitbox = self.img.get_rect()
    
    def __repr__(self):
        return f"{self.colour} {self.name}"