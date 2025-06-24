import pygame
import math
from PIL import Image, ImageDraw
import os
import players

class HexagonalBoard:
    def __init__(self, width=1200, height=800, hex_radius=32):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Hexagonal Board Game")
        
        self.hex_radius = hex_radius
        self.hex_width = hex_radius * 2
        self.hex_height = hex_radius * math.sqrt(3)
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.BLUE = (70, 130, 180)  # Steel blue background
        self.YELLOW_OCHRE = (204, 153, 51)  # Yellow ochre for default cells
        self.RED = (220, 20, 60)  # Crimson red for UI elements
        self.GREEN = (34, 139, 34)  # Forest green for buttons
        
        # Rotation angle (60 degrees counter-clockwise)
        self.rotation_angle = -math.pi / 6  # -30 degrees in radians
        
        # Generate hexagonal grid (6 tiles per side)
        self.hexagons = self.generate_hexagonal_grid(6)
        self.hex_images = {}
        
        # Player character
        self.player = None
        self.player_image = None
        self.moves_used = 0
        self.max_moves = 10000
        
        # Reset button
        self.reset_button_rect = pygame.Rect(self.width - 120, 20, 100, 40)
        self.button_font = pygame.font.Font(None, 24)
        
        # Clock for FPS
        self.clock = pygame.time.Clock()
        
    def rotate_point(self, x, y, angle):
        """Rotate a point around the origin by the given angle"""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        new_x = x * cos_a - y * sin_a
        new_y = x * sin_a + y * cos_a
        return new_x, new_y
        
    def generate_hexagonal_grid(self, side_length):
        """Generate hexagonal grid coordinates for a board with side_length tiles per side"""
        hexagons = []
        center_x = self.width // 2
        center_y = self.height // 2
        
        # For a hexagonal grid with side_length tiles per side
        # We need to generate coordinates in a hexagonal pattern
        for q in range(-side_length + 1, side_length):
            r1 = max(-side_length + 1, -q - side_length + 1)
            r2 = min(side_length - 1, -q + side_length - 1)
            for r in range(r1, r2 + 1):
                # Convert cube coordinates to pixel coordinates
                x = self.hex_radius * 1.5 * q
                y = self.hex_radius * math.sqrt(3) * (r + q / 2)
                
                # Apply rotation
                rotated_x, rotated_y = self.rotate_point(x, y, self.rotation_angle)
                
                # Translate to center of screen
                final_x = center_x + rotated_x
                final_y = center_y + rotated_y
                
                hexagons.append((final_x, final_y, q, r))
        
        return hexagons
    
    def hex_corners(self, center_x, center_y):
        """Calculate the 6 corners of a hexagon with rotation applied"""
        corners = []
        for i in range(6):
            # Calculate hexagon corner angle
            angle = i * math.pi / 3
            # Apply the board rotation to each corner
            total_angle = angle + self.rotation_angle
            x = center_x + self.hex_radius * math.cos(total_angle)
            y = center_y + self.hex_radius * math.sin(total_angle)
            corners.append((x, y))
        return corners
    
    def create_hexagon_mask(self, size):
        """Create a hexagonal mask for cropping images with rotation"""
        # Create a new image with transparency
        mask = Image.new('RGBA', (size, size), (255, 255, 255, 255))  # White background
        draw = ImageDraw.Draw(mask)
        
        # Calculate hexagon points with rotation
        center = size // 2
        radius = size // 2 - 2  # Slightly smaller to avoid edge issues
        points = []
        for i in range(6):
            angle = i * math.pi / 3 + self.rotation_angle
            x = center + radius * math.cos(angle)
            y = center + radius * math.sin(angle)
            points.append((x, y))
        
        # Draw transparent hexagon (this will be the visible part)
        draw.polygon(points, fill=(0, 0, 0, 0))
        return mask
    
    def crop_image_to_hexagon(self, image_path, output_size=None):
        """Crop an image to show only the hexagonal part"""
        if output_size is None:
            output_size = int(self.hex_radius * 2)
        
        try:
            # Load and resize the image
            img = Image.open(image_path)
            img = img.convert('RGBA')
            img = img.resize((output_size, output_size), Image.Resampling.LANCZOS)
            
            # Create hexagon mask (inverted - hexagon is transparent, outside is opaque)
            mask = self.create_hexagon_mask(output_size)
            
            # Apply inverted mask to image - this keeps the hexagon and removes the outside
            result = Image.new('RGBA', (output_size, output_size), (0, 0, 0, 0))
            result.paste(img, (0, 0))
            
            # Use the mask to make everything OUTSIDE the hexagon transparent
            # We need to invert the logic: where mask is transparent (hexagon), keep image
            # Where mask is opaque (outside), make transparent
            for x in range(output_size):
                for y in range(output_size):
                    mask_pixel = mask.getpixel((x, y))
                    if mask_pixel[3] == 255:  # If mask is opaque (outside hexagon)
                        result.putpixel((x, y), (0, 0, 0, 0))  # Make transparent
            
            # Convert to pygame surface
            mode = result.mode
            size = result.size
            data = result.tobytes()
            surface = pygame.image.fromstring(data, size, mode)
            
            return surface
            
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            return None
    
    def load_hex_image(self, hex_id, image_path):
        """Load and crop an image for a specific hexagon"""
        surface = self.crop_image_to_hexagon(image_path)
        if surface:
            self.hex_images[hex_id] = surface
    
    def get_hex_pixel_position(self, q, r):
        """Get pixel position for given hex coordinates"""
        for x, y, hq, hr in self.hexagons:
            if hq == q and hr == r:
                return (x, y)
        return None

    def draw_hexagon(self, center_x, center_y, color=None, filled=False):
        """Draw a hexagon at the specified center"""
        corners = self.hex_corners(center_x, center_y)
        
        if filled and color:
            pygame.draw.polygon(self.screen, color, corners)
        else:
            pygame.draw.polygon(self.screen, self.BLACK, corners, 2)
    
    def draw_board(self):
        """Draw the entire hexagonal board"""
        self.screen.fill(self.BLUE)  # Blue background
        
        for i, (x, y, q, r) in enumerate(self.hexagons):
            # Draw filled hexagon with yellow ochre as default
            self.draw_hexagon(x, y, color=self.YELLOW_OCHRE, filled=True)
            
            # Draw hexagon border
            self.draw_hexagon(x, y)
            
            # Draw image if available (this will overlay the yellow ochre)
            hex_id = f"hex_{i}"
            if hex_id in self.hex_images:
                img_surface = self.hex_images[hex_id]
                img_rect = img_surface.get_rect()
                img_rect.center = (int(x), int(y))
                self.screen.blit(img_surface, img_rect)
            
            # Draw coordinate text (optional, for debugging)
            font = pygame.font.Font(None, 24)
            text = font.render(f"({q},{r})", True, self.BLACK)
            text_rect = text.get_rect()
            text_rect.center = (int(x), int(y + self.hex_radius - 10))
            self.screen.blit(text, text_rect)
        
        # Draw player character
        if self.player and self.player_image:
            player_pos = self.get_hex_pixel_position(self.player[0], self.player[1])
            if player_pos:
                player_rect = self.player_image.get_rect()
                player_rect.center = (int(player_pos[0]), int(player_pos[1]))
                self.screen.blit(self.player_image, player_rect)
        
        # Draw UI elements
        self.draw_ui()
    
    def draw_ui(self):
        """Draw user interface elements"""
        # Draw move counter
        moves_text = f"Moves: {self.moves_used}/{self.max_moves}"
        text_color = self.RED if self.moves_used >= self.max_moves else self.BLACK
        moves_surface = self.button_font.render(moves_text, True, text_color)
        self.screen.blit(moves_surface, (20, 20))
        
        # Draw reset button
        button_color = self.GREEN if self.moves_used > 0 else self.GRAY
        pygame.draw.rect(self.screen, button_color, self.reset_button_rect)
        pygame.draw.rect(self.screen, self.BLACK, self.reset_button_rect, 2)
        
        # Button text
        button_text = self.button_font.render("RESET", True, self.WHITE)
        text_rect = button_text.get_rect()
        text_rect.center = self.reset_button_rect.center
        self.screen.blit(button_text, text_rect)
    
    def handle_button_click(self, mouse_pos):
        """Handle clicks on UI buttons"""
        if self.reset_button_rect.collidepoint(mouse_pos):
            self.reset_moves()
            return True
        return False

    def get_hex_at_position(self, mouse_pos):
        """Get the hexagon at the given mouse position"""
        mx, my = mouse_pos
        for i, (x, y, q, r) in enumerate(self.hexagons):
            # Simple distance check (can be improved with proper hex collision)
            distance = math.sqrt((mx - x)**2 + (my - y)**2)
            if distance <= self.hex_radius:
                return i, (q, r)
        return None, None
    
    
    def move_player(self, dq, dr):

        """Move player by the given coordinate offset"""
        if not self.player:
            return
            
        if self.moves_used >= self.max_moves:
            print(f"No moves left! Used {self.moves_used}/{self.max_moves} moves. Click Reset to continue.")
            return
            
        new_q = self.player[0] + dq
        new_r = self.player[1] + dr
        
        # Check if the new position exists on the board
        if self.get_hex_pixel_position(new_q, new_r):
            self.player = (new_q, new_r)
            self.moves_used += 1
            print(f"Player moved to {self.player} - Moves used: {self.moves_used}/{self.max_moves}")
        else:
            print(f"Cannot move to {(new_q, new_r)} - outside board")

    def load_player_character(self, image_path):
        """Load and crop the player character image"""
        self.player_image = self.crop_image_to_hexagon(image_path)
        if self.player_image:
            # Start player at a random corner of the board
            corner_hexes = self.get_corner_hexagons()
            if corner_hexes:
                import random
                start_hex = random.choice(corner_hexes)
                print(start_hex)
                self.player = (start_hex[2], start_hex[3])  # (q, r) coordinates
                print(f"Player started at coordinates {self.player}")
    
    def reset_moves(self):
        """Reset the move counter"""
        self.moves_used = 0
        print(f"Moves reset! {self.moves_used}/{self.max_moves} moves available")

    def run(self):
        """Main game loop"""
        running = True
        
        # Example: Load some images (you'll need to provide your own PNG files)
        # Uncomment and modify these lines to load your images:
        # self.load_hex_image("hex_0", "path/to/your/image1.png")
        # self.load_hex_image("hex_1", "path/to/your/image2.png")
        
        # Load player character (uncomment and provide your character image)
        # self.load_player_character("path/to/your/character.png")
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if button was clicked first
                    if self.handle_button_click(event.pos):
                        continue  # Button was clicked, don't check hex clicks
                    
                    # Check hex clicks
                    hex_id, coords = self.get_hex_at_position(event.pos)
                    if hex_id is not None:
                        print(f"Clicked on hexagon {hex_id} at coordinates {coords}")
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    # Player movement controls (adjusted for rotation)
                    elif event.key == pygame.K_d:
                        self.move_player(1, 0)      # +1,+0
                    elif event.key == pygame.K_e:
                        self.move_player(1, -1)     # +1,-1
                    elif event.key == pygame.K_w:
                        self.move_player(0, -1)     # 0,-1
                    elif event.key == pygame.K_x:
                        self.move_player(0, 1)      # 0,+1
                    elif event.key == pygame.K_a:
                        self.move_player(-1, 0)     # -1,+0
                    elif event.key == pygame.K_z:
                        self.move_player(-1, 1)     # -1,+1
                    # Taking an action
                    elif event.key == pygame.K_s:
                        players.AbilityPanel.open()
                            
            
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()

    def create_sample_images():
        
        # Create a simple player character (red circle on white background)
        player_img = Image.new('RGB', (100, 100), (255, 255, 255))
        draw = ImageDraw.Draw(player_img)
        draw.ellipse([20, 20, 80, 80], fill=(255, 0, 0))  # Red circle
        player_img.save(r"C:\Users\Denver Zuzarte\vsc folder\LoyalAndTheLawless\PDA\sample_images\player.png")
        print("Created sample_images/player.png")

print ('Board cache has been updated')

if __name__ == "__main__":
    create_sample_images() #creates image of character
    load_player_character(r"C:\Users\Denver Zuzarte\vsc folder\LoyalAndTheLawless\PDA\sample_images\player.png")
    sampleboard = HexagonalBoard(hex_radius=36) # makes the object sample board
    sampleboard.run() # uses the function run to run the board
