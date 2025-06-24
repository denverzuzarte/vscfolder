import pygame
import math
from PIL import Image, ImageDraw
import os

class HexagonalBoard:
    def __init__(self, width=1200, height=800, hex_radius=32):
        """
        Initialize the hexagonal board game.
        
        Args:
            width (int): Screen width in pixels (default: 1200)
            height (int): Screen height in pixels (default: 800)
            hex_radius (int): Radius of each hexagon in pixels (default: 32)
        """
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Hexagonal Board Game")
        
        # Calculate hexagon dimensions based on radius
        self.hex_radius = hex_radius
        self.hex_width = hex_radius * 2
        self.hex_height = hex_radius * math.sqrt(3)
        
        # Define color palette for the game
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.BLUE = (70, 130, 180)  # Steel blue background
        self.YELLOW_OCHRE = (204, 153, 51)  # Yellow ochre for default cells
        self.RED = (220, 20, 60)  # Crimson red for UI elements
        self.GREEN = (34, 139, 34)  # Forest green for buttons
        
        # Generate the hexagonal grid layout (6 tiles per side)
        self.hexagons = self.generate_hexagonal_grid(6)
        self.hex_images = {}  # Dictionary to store loaded images for hexagons
        
        # Player character properties
        self.player = None  # Player position as (q, r) coordinates
        self.player_image = None  # Player character image surface
        self.moves_used = 0  # Counter for moves used this turn
        self.max_moves = 4  # Maximum moves allowed per turn
        
        # UI elements
        self.reset_button_rect = pygame.Rect(self.width - 120, 20, 100, 40)
        self.button_font = pygame.font.Font(None, 24)
        
        # Game clock for controlling frame rate
        self.clock = pygame.time.Clock()
        
    def generate_hexagonal_grid(self, side_length):
        """
        Generate hexagonal grid coordinates for a board with specified side length.
        Uses cube coordinates (q, r) system for hexagonal grids.
        
        Args:
            side_length (int): Number of tiles per side of the hexagonal board
            
        Returns:
            list: List of tuples (x, y, q, r) where x,y are pixel coordinates
                  and q,r are cube coordinates
        """
        hexagons = []
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Generate coordinates in hexagonal pattern using cube coordinate system
        # q and r are the two main axes in hexagonal cube coordinates
        for q in range(-side_length + 1, side_length):
            # Calculate the range of r values for this q
            r1 = max(-side_length + 1, -q - side_length + 1)
            r2 = min(side_length - 1, -q + side_length - 1)
            for r in range(r1, r2 + 1):
                # Convert cube coordinates to pixel coordinates
                # Formula for hexagonal grid positioning
                x = center_x + self.hex_radius * 1.5 * q
                y = center_y + self.hex_radius * math.sqrt(3) * (r + q / 2)
                hexagons.append((x, y, q, r))
        
        return hexagons
    
    def hex_corners(self, center_x, center_y):
        """
        Calculate the 6 corner points of a hexagon given its center.
        
        Args:
            center_x (float): X coordinate of hexagon center
            center_y (float): Y coordinate of hexagon center
            
        Returns:
            list: List of 6 (x, y) tuples representing the hexagon corners
        """
        corners = []
        # Calculate each corner using trigonometry
        # Hexagon has 6 corners, each 60 degrees apart
        for i in range(6):
            angle = i * math.pi / 3  # 60 degrees in radians
            x = center_x + self.hex_radius * math.cos(angle)
            y = center_y + self.hex_radius * math.sin(angle)
            corners.append((x, y))
        return corners
    
    def create_hexagon_mask(self, size):
        """
        Create a hexagonal mask for cropping images into hexagon shape.
        The mask defines which pixels should be visible (hexagon) vs transparent.
        
        Args:
            size (int): Size of the square mask image
            
        Returns:
            PIL.Image: RGBA image with hexagonal transparency mask
        """
        # Create a new image with white background
        mask = Image.new('RGBA', (size, size), (255, 255, 255, 255))
        draw = ImageDraw.Draw(mask)
        
        # Calculate hexagon points within the square
        center = size // 2
        radius = size // 2 - 2  # Slightly smaller to avoid edge issues
        points = []
        for i in range(6):
            angle = i * math.pi / 3
            x = center + radius * math.cos(angle)
            y = center + radius * math.sin(angle)
            points.append((x, y))
        
        # Draw transparent hexagon (this creates the cutout shape)
        draw.polygon(points, fill=(0, 0, 0, 0))
        return mask
    
    def crop_image_to_hexagon(self, image_path, output_size=None):
        """
        Load an image and crop it to fit within a hexagonal boundary.
        This creates the hexagonal tiles that appear on the board.
        
        Args:
            image_path (str): Path to the image file to crop
            output_size (int, optional): Size of the output image. 
                                       Defaults to hex_radius * 2
            
        Returns:
            pygame.Surface or None: Cropped hexagonal image as pygame surface,
                                   or None if processing failed
        """
        if output_size is None:
            output_size = int(self.hex_radius * 2)
        
        try:
            # Load and prepare the source image
            img = Image.open(image_path)
            img = img.convert('RGBA')  # Ensure RGBA format for transparency
            img = img.resize((output_size, output_size), Image.Resampling.LANCZOS)
            
            # Create hexagon mask for cropping
            mask = self.create_hexagon_mask(output_size)
            
            # Start with the original image
            result = Image.new('RGBA', (output_size, output_size), (0, 0, 0, 0))
            result.paste(img, (0, 0))
            
            # Apply mask: make everything outside hexagon transparent
            for x in range(output_size):
                for y in range(output_size):
                    mask_pixel = mask.getpixel((x, y))
                    if mask_pixel[3] == 255:  # If mask is opaque (outside hexagon)
                        result.putpixel((x, y), (0, 0, 0, 0))  # Make transparent
            
            # Convert PIL image to pygame surface
            mode = result.mode
            size = result.size
            data = result.tobytes()
            surface = pygame.image.fromstring(data, size, mode)
            
            return surface
            
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            return None
    
    def load_hex_image(self, hex_id, image_path):
        """
        Load and process an image for display on a specific hexagon.
        
        Args:
            hex_id (str): Unique identifier for the hexagon (e.g., "hex_0")
            image_path (str): Path to the image file to load
        """
        surface = self.crop_image_to_hexagon(image_path)
        if surface:
            self.hex_images[hex_id] = surface
    
    def load_player_character(self, image_path):
        """
        Load the player character image and place player at random corner.
        
        Args:
            image_path (str): Path to the player character image file
        """
        self.player_image = self.crop_image_to_hexagon(image_path)
        if self.player_image:
            # Start player at a random corner hexagon
            corner_hexes = self.get_corner_hexagons()
            if corner_hexes:
                import random
                start_hex = random.choice(corner_hexes)
                self.player = (start_hex[2], start_hex[3])  # Store as (q, r) coordinates
                print(f"Player started at coordinates {self.player}")
    
    def get_corner_hexagons(self):
        """
        Identify and return the 6 corner hexagons of the board.
        Corner hexagons are at the extremes of the hexagonal grid.
        
        Returns:
            list: List of corner hexagon tuples (x, y, q, r)
        """
        corners = []
        for x, y, q, r in self.hexagons:
            # Corner hexagons are at the extremes of the coordinate system
            # They satisfy the condition that at least one coordinate is at maximum value
            if (abs(q) == 5 and abs(r) <= 5 and abs(q + r) <= 5) or \
               (abs(r) == 5 and abs(q) <= 5 and abs(q + r) <= 5) or \
               (abs(q + r) == 5 and abs(q) <= 5 and abs(r) <= 5):
                corners.append((x, y, q, r))
        return corners
    
    def get_hex_pixel_position(self, q, r):
        """
        Convert hexagon cube coordinates to pixel coordinates.
        
        Args:
            q (int): Q coordinate in cube coordinate system
            r (int): R coordinate in cube coordinate system
            
        Returns:
            tuple or None: (x, y) pixel coordinates, or None if not found
        """
        for x, y, hq, hr in self.hexagons:
            if hq == q and hr == r:
                return (x, y)
        return None
    
    def move_player(self, dq, dr):
        """
        Move the player character by the specified coordinate offset.
        Handles move limits and boundary checking.
        
        Args:
            dq (int): Change in Q coordinate
            dr (int): Change in R coordinate
        """
        if not self.player:
            return
            
        # Check if player has moves remaining
        if self.moves_used >= self.max_moves:
            print(f"No moves left! Used {self.moves_used}/{self.max_moves} moves. Click Reset to continue.")
            return
            
        # Calculate new position
        new_q = self.player[0] + dq
        new_r = self.player[1] + dr
        
        # Verify the new position exists on the board
        if self.get_hex_pixel_position(new_q, new_r):
            self.player = (new_q, new_r)
            self.moves_used += 1
            print(f"Player moved to {self.player} - Moves used: {self.moves_used}/{self.max_moves}")
        else:
            print(f"Cannot move to {(new_q, new_r)} - outside board")
    
    def reset_moves(self):
        """
        Reset the move counter to allow the player to move again.
        Called when the reset button is clicked.
        """
        self.moves_used = 0
        print(f"Moves reset! {self.moves_used}/{self.max_moves} moves available")
    
    def draw_hexagon(self, center_x, center_y, color=None, filled=False):
        """
        Draw a single hexagon on the screen.
        
        Args:
            center_x (float): X coordinate of hexagon center
            center_y (float): Y coordinate of hexagon center
            color (tuple, optional): RGB color tuple for filled hexagons
            filled (bool): Whether to draw filled hexagon or just outline
        """
        corners = self.hex_corners(center_x, center_y)
        
        if filled and color:
            # Draw filled hexagon with specified color
            pygame.draw.polygon(self.screen, color, corners)
        else:
            # Draw hexagon outline in black
            pygame.draw.polygon(self.screen, self.BLACK, corners, 2)
    
    def draw_board(self):
        """
        Draw the complete hexagonal board including all hexagons, images, 
        player character, and UI elements.
        """
        # Clear screen with blue background
        self.screen.fill(self.BLUE)
        
        # Draw each hexagon on the board
        for i, (x, y, q, r) in enumerate(self.hexagons):
            # Draw filled hexagon with default yellow ochre color
            self.draw_hexagon(x, y, color=self.YELLOW_OCHRE, filled=True)
            
            # Draw black border around hexagon
            self.draw_hexagon(x, y)
            
            # Draw custom image if one is loaded for this hexagon
            hex_id = f"hex_{i}"
            if hex_id in self.hex_images:
                img_surface = self.hex_images[hex_id]
                img_rect = img_surface.get_rect()
                img_rect.center = (int(x), int(y))
                self.screen.blit(img_surface, img_rect)
            
            # Draw coordinate labels for debugging (optional)
            font = pygame.font.Font(None, 24)
            text = font.render(f"({q},{r})", True, self.BLACK)
            text_rect = text.get_rect()
            text_rect.center = (int(x), int(y + self.hex_radius - 10))
            self.screen.blit(text, text_rect)
        
        # Draw player character if present
        if self.player and self.player_image:
            player_pos = self.get_hex_pixel_position(self.player[0], self.player[1])
            if player_pos:
                player_rect = self.player_image.get_rect()
                player_rect.center = (int(player_pos[0]), int(player_pos[1]))
                self.screen.blit(self.player_image, player_rect)
        
        # Draw user interface elements
        self.draw_ui()
    
    def draw_ui(self):
        """
        Draw user interface elements including move counter and reset button.
        """
        # Draw move counter in top-left corner
        moves_text = f"Moves: {self.moves_used}/{self.max_moves}"
        # Change color to red if no moves left
        text_color = self.RED if self.moves_used >= self.max_moves else self.BLACK
        moves_surface = self.button_font.render(moves_text, True, text_color)
        self.screen.blit(moves_surface, (20, 20))
        
        # Draw reset button
        # Button color changes based on whether moves have been used
        button_color = self.GREEN if self.moves_used > 0 else self.GRAY
        pygame.draw.rect(self.screen, button_color, self.reset_button_rect)
        pygame.draw.rect(self.screen, self.BLACK, self.reset_button_rect, 2)
        
        # Draw button text
        button_text = self.button_font.render("RESET", True, self.WHITE)
        text_rect = button_text.get_rect()
        text_rect.center = self.reset_button_rect.center
        self.screen.blit(button_text, text_rect)
    
    def handle_button_click(self, mouse_pos):
        """
        Handle mouse clicks on UI buttons.
        
        Args:
            mouse_pos (tuple): (x, y) coordinates of mouse click
            
        Returns:
            bool: True if a button was clicked, False otherwise
        """
        if self.reset_button_rect.collidepoint(mouse_pos):
            self.reset_moves()
            return True
        return False

    def get_hex_at_position(self, mouse_pos):
        """
        Determine which hexagon was clicked based on mouse position.
        Uses simple distance calculation for hit detection.
        
        Args:
            mouse_pos (tuple): (x, y) coordinates of mouse click
            
        Returns:
            tuple: (hex_index, (q, r)) or (None, None) if no hexagon clicked
        """
        mx, my = mouse_pos
        for i, (x, y, q, r) in enumerate(self.hexagons):
            # Calculate distance from mouse to hexagon center
            distance = math.sqrt((mx - x)**2 + (my - y)**2)
            # If mouse is within hexagon radius, consider it a hit
            if distance <= self.hex_radius:
                return i, (q, r)
        return None, None
    
    def run(self):
        """
        Main game loop that handles events, updates game state, and renders.
        This is the core function that keeps the game running.
        """
        running = True
        
        # Example image loading (commented out - uncomment and modify paths as needed)
        # self.load_hex_image("hex_0", "path/to/your/image1.png")
        # self.load_hex_image("hex_1", "path/to/your/image2.png")
        
        # Load player character (commented out - uncomment and provide path)
        # self.load_player_character("path/to/your/character.png")
        
        while running:
            # Process all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check UI button clicks first
                    if self.handle_button_click(event.pos):
                        continue  # Skip hex click checking if button was clicked
                    
                    # Check for hexagon clicks
                    hex_id, coords = self.get_hex_at_position(event.pos)
                    if hex_id is not None:
                        print(f"Clicked on hexagon {hex_id} at coordinates {coords}")
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    # Player movement controls using hexagonal coordinate system
                    # Each key corresponds to one of the 6 hexagonal directions
                    elif event.key == pygame.K_d:
                        self.move_player(1, 0)      # Move right
                    elif event.key == pygame.K_e:
                        self.move_player(1, -1)     # Move up-right
                    elif event.key == pygame.K_w:
                        self.move_player(0, -1)     # Move up-left
                    elif event.key == pygame.K_x:
                        self.move_player(0, 1)      # Move down-right
                    elif event.key == pygame.K_a:
                        self.move_player(-1, 0)     # Move left
                    elif event.key == pygame.K_z:
                        self.move_player(-1, 1)     # Move down-left
            
            # Render the game
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(60)  # Maintain 60 FPS
        
        pygame.quit()

# Example usage and helper functions
def create_sample_images():
    """
    Create sample colored images for testing the hexagonal board.
    This function generates simple colored squares and a player character.
    """
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
    
    # Create directory for sample images if it doesn't exist
    if not os.path.exists("sample_images"):
        os.makedirs("sample_images")
    
    # Create colored square images
    for i, color in enumerate(colors):
        img = Image.new('RGB', (100, 100), color)
        img.save(f"sample_images/sample_{i}.png")
        print(f"Created sample_images/sample_{i}.png")
    
    # Create a simple player character (red circle on white background)
    player_img = Image.new('RGB', (100, 100), (255, 255, 255))
    draw = ImageDraw.Draw(player_img)
    draw.ellipse([20, 20, 80, 80], fill=(255, 0, 0))  # Red circle
    player_img.save("sample_images/player.png")
    print("Created sample_images/player.png")

if __name__ == "__main__":
    """
    Main execution block - creates sample images and runs the game.
    """
    # Create sample images for testing
    create_sample_images()
    
    # Create and configure the hexagonal board
    board = HexagonalBoard(hex_radius=40)
    
    # Load sample images into the first 5 hexagons
    for i in range(5):
        if os.path.exists(f"sample_images/sample_{i}.png"):
            board.load_hex_image(f"hex_{i}", f"sample_images/sample_{i}.png")
    
    # Load player character image
    if os.path.exists("sample_images/player.png"):
        board.load_player_character("sample_images/player.png")
    
    # Display game instructions
    print("Controls:")
    print("- Click on hexagons to see their coordinates")
    print("- Use WASD + E/Z to move player (4 moves max):")
    print("  D: +1,+0  |  E: +1,-1  |  W: 0,-1")
    print("  A: -1,+0  |  Z: -1,+1  |  X: 0,+1")
    print("- Click RESET button to restore 4 moves")
    print("- Press ESC to quit")
    print(f"Board has {len(board.hexagons)} hexagons")
    
    # Start the game
    board.run()