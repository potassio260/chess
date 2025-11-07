# Imports
import pygame

# Game loop
class GameUI():
    def __init__(self):
        # Initialize pygame 
        pygame.init()
        
        # colours
        self.background_colour = (77, 77, 77)
        self.yellow_rgb = (108, 156, 98)
        self.green_rgb = (249, 246, 225)
        self.button_colour = (60, 60, 60)
        self.button_hover = (80, 80, 80)
        self.button_text = (255, 255, 255)

        # set screen
        self.Screen = pygame.display.set_mode((640, 640))
        self.Surface = pygame.Surface((640, 640), pygame.SRCALPHA)
        self.Clock = pygame.time.Clock()
        
        # declare variables
        self.piece_moving = None
        self.game_mode = None  # 'local', 'multiplayer', or 'bot'
        self.player_colour = None  # 'white' or 'black' (only for bot mode)
        
    def show_intro_screen(self):
        font_large = pygame.font.Font(None, 60)
        font_medium = pygame.font.Font(None, 40)
        
        # Button dimensions
        button_width = 300
        button_height = 60
        button_spacing = 20
        start_y = 200
        
        # Create buttons
        local_button = pygame.Rect(170, start_y, button_width, button_height)
        multiplayer_button = pygame.Rect(170, start_y + button_height + button_spacing, button_width, button_height)
        bot_button = pygame.Rect(170, start_y + 2 * (button_height + button_spacing), button_width, button_height)
        
        selected_mode = None
        
        while True:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None, None
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if local_button.collidepoint(mouse_pos):
                        return 'local', None
                    elif multiplayer_button.collidepoint(mouse_pos):
                        return 'multiplayer', None
                    elif bot_button.collidepoint(mouse_pos):
                        selected_mode = 'bot'
                        colour = self.show_colour_selection()
                        if colour:
                            return 'bot', colour
            
            # Draw background
            self.Screen.fill(self.background_colour)
            
            # Draw title
            title = font_large.render("Chess Game", True, self.green_rgb)
            title_rect = title.get_rect(center=(320, 100))
            self.Screen.blit(title, title_rect)
            
            # Draw buttons
            buttons = [
                (local_button, 'Local Play'),
                (multiplayer_button, 'Multiplayer'),
                (bot_button, 'Play vs Bot')
            ]
            
            for button, text in buttons:
                # Button colour changes on hover
                if button.collidepoint(mouse_pos):
                    pygame.draw.rect(self.Screen, self.button_hover, button, border_radius=10)
                else:
                    pygame.draw.rect(self.Screen, self.button_colour, button, border_radius=10)
                
                # Draw button border
                pygame.draw.rect(self.Screen, self.green_rgb, button, 3, border_radius=10)
                
                # Draw text
                text_surf = font_medium.render(text, True, self.button_text)
                text_rect = text_surf.get_rect(center=button.center)
                self.Screen.blit(text_surf, text_rect)
            
            pygame.display.flip()
            self.Clock.tick(60)
    
    def show_colour_selection(self):
        font_large = pygame.font.Font(None, 50)
        font_medium = pygame.font.Font(None, 40)
        
        # Button dimensions
        button_width = 200
        button_height = 80
        button_spacing = 20
        
        white_button = pygame.Rect(220, 200, button_width, button_height)
        black_button = pygame.Rect(220, 200 + button_height + button_spacing, button_width, button_height)
        back_button = pygame.Rect(220, 500, 200, 50)
        
        while True:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if white_button.collidepoint(mouse_pos):
                        return 'white'
                    elif black_button.collidepoint(mouse_pos):
                        return 'black'
                    elif back_button.collidepoint(mouse_pos):
                        return None
            
            # Draw background
            self.Screen.fill(self.background_colour)
            
            # Draw title
            title = font_large.render('Choose Your colour', True, self.green_rgb)
            title_rect = title.get_rect(center=(320, 150))
            self.Screen.blit(title, title_rect)
            
            # Draw white button
            if white_button.collidepoint(mouse_pos):
                pygame.draw.rect(self.Screen, self.button_hover, white_button, border_radius=10)
            else:
                pygame.draw.rect(self.Screen, self.button_colour, white_button, border_radius=10)

            pygame.draw.rect(self.Screen, self.green_rgb, white_button, 3, border_radius=10)
            white_text = font_medium.render('White', True, (255, 255, 255))
            white_text_rect = white_text.get_rect(center=white_button.center)
            self.Screen.blit(white_text, white_text_rect)
            
            # Draw black button
            if black_button.collidepoint(mouse_pos):
                pygame.draw.rect(self.Screen, self.button_hover, black_button, border_radius=10)
            else:
                pygame.draw.rect(self.Screen, self.button_colour, black_button, border_radius=10)

            pygame.draw.rect(self.Screen, self.green_rgb, black_button, 3, border_radius=10)
            black_text = font_medium.render('Black', True, (255, 255, 255))
            black_text_rect = black_text.get_rect(center=black_button.center)
            self.Screen.blit(black_text, black_text_rect)
            
            # Draw back button
            if back_button.collidepoint(mouse_pos):
                pygame.draw.rect(self.Screen, self.button_hover, back_button, border_radius=10)
            else:
                pygame.draw.rect(self.Screen, self.button_colour, back_button, border_radius=10)

            pygame.draw.rect(self.Screen, self.green_rgb, back_button, 2, border_radius=10)
            back_text = font_medium.render('Back', True, self.button_text)
            back_text_rect = back_text.get_rect(center=back_button.center)
            self.Screen.blit(back_text, back_text_rect)
            
            pygame.display.flip()
            self.Clock.tick(60)

    def run(self, board: dict, turn: str):
        running, dragging = True, False
        start_pos, clicked_pos = None, None
        
        while running:
            self.Screen.fill(self.background_colour)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    quit()

                # Detect Mouse Click (Press)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    start_pos = self.get_pressed_cord(board=board, turn=turn)
                    if start_pos:
                        piece = board[start_pos]["piece"]
                        if piece:
                            if piece.colour == turn:
                                dragging = True
    
                elif event.type == pygame.MOUSEMOTION:
                    if dragging:
                        self.update_screen(board=board)

                # Detect Drop / Click Release
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    end_pos = self.get_unpressed_cord(board=board)
                    dragging = False 
                    if start_pos:
                        if (start_pos != end_pos):
                            if board[start_pos]["piece"]!=None:
                                if board[start_pos]["piece"].colour==turn:
                                    self.piece_moving = None
                                    self.Surface = pygame.Surface((640, 640), pygame.SRCALPHA)
                                    return start_pos, end_pos
                        else:
                            if board[start_pos]["piece"]!=None:
                                if board[start_pos]["piece"].colour==turn:
                                    clicked_pos = end_pos
                            if clicked_pos == end_pos:
                                end_pos = None
                            elif clicked_pos and end_pos:
                                self.piece_moving = None
                                self.Surface = pygame.Surface((640, 640), pygame.SRCALPHA)
                                return clicked_pos, end_pos
                            
                        self.piece_moving = None  # Reset piece_moving when dropped

            # Update the screen every frame
            self.update_screen(board=board)
            self.Screen.blit(self.Surface, (0,0))
            pygame.display.flip()
            self.Clock.tick(60)

    def update_screen(self, board: dict):
        self.draw_board(board=board)
        self.draw_pieces(board=board, piece_to_move=self.piece_moving)
    
    def draw_board(self, board: dict):
        squares = [s["square"] for s in board.values()]
        curr_colour = self.green_rgb
        count = 0
        for square in squares:
            pygame.draw.rect(self.Screen, curr_colour, square)
            if count != 7:
                if curr_colour == self.yellow_rgb:
                    curr_colour = self.green_rgb
                else:
                    curr_colour = self.yellow_rgb
                count += 1
            else:
                count = 0

    def draw_pieces(self, board: dict, piece_to_move=None):
        for sub_dict in board.values():
            if sub_dict["piece"] is not None:
                piece = sub_dict["piece"]
                piece_image = piece.img
                piece_hitbox = piece.hitbox 

                if piece_hitbox != piece_to_move:
                    # Move the piece's hitbox to the square position
                    piece_hitbox.center = sub_dict["square"].center
                    # pygame.draw.rect(self.Screen, (0, 0, 0), piece_hitbox) if hitbox wanted
                else:
                    # If it's the moving piece, center it on mouse position
                    piece_hitbox.center = pygame.mouse.get_pos()
                
                # Draw the piece image
                self.Screen.blit(piece_image, piece_hitbox)

    def get_pressed_cord(self, board: dict, turn : str):
        mouse_pos = pygame.mouse.get_pos()
        for cords, sub_dict in board.items():
            if sub_dict["square"].collidepoint(mouse_pos):
                if sub_dict["piece"] is not None:
                    if sub_dict["piece"].colour == turn:
                        self.piece_moving = sub_dict["piece"].hitbox
                return cords

                    
    def get_unpressed_cord(self, board: dict):
        mouse_pos = pygame.mouse.get_pos()
        for cords, sub_dict in board.items():
            if sub_dict["square"].collidepoint(mouse_pos):
                return cords