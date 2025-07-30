import pygame
import math
import random
import json
import os
from PIL import Image, ImageOps
import io
# Uncomment when Player class is available
# from .player import Player

class HexBoard:
    """A hexagonal board with simple and difficult terrain"""
    
    def __init__(self, width=1200, height=800, hex_radius=40):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Hexagonal Board - Simple & Difficult Terrain")
        
        self.hex_radius = hex_radius
        
        # Terrain colors - made more contrasting
        self.SIMPLE_TERRAIN = (255, 255, 200)   # Very light yellow/ochre
        self.DIFFICULT_TERRAIN = (100, 50, 0)   # Dark brown
        self.WATER_COLOR = (25, 100, 200)       # Blue for surrounding
        self.BLACK = (0, 0, 0)                  # Border color
        self.WHITE = (255, 255, 255)            # Text color
        self.GRAY = (127,127,127) 
        
        # Generate hexagonal board (6 hexes per side)
        self.board_radius = 6
        self.hexagons = self.generate_hexagonal_board()
        
        # Data storage
        self.difficult_terrain = set()  # Set of (q, r) coordinates
        self.walls = set()  # Set of ((q1, r1), (q2, r2)) coordinate pairs
        
        # JSON file path
        self.terrain_file = r"D:\vsc folder\LoyalAndTheLawless\src\terrain.json"
        
        # Player selection state
        self.game_state = "alignment_selection"  # alignment_selection, player_selection, playing
        self.selected_alignment = 0
        self.selected_player_index = 0
        self.available_players = []
        self.player_images = {}
        self.player = None
        
        # Load player data
        self.load_player_data() 
        
        # Load existing data
        self.load_terrain_data()
        
        # Apply loaded terrain data to hexagons
        self.apply_terrain_data()
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 18)
        self.coord_font = pygame.font.Font(None, 16)
        self.title_font = pygame.font.Font(None, 48)
        self.menu_font = pygame.font.Font(None, 36)
        
        # Alignment options
        self.alignments = [
            ("Loyal", (65, 105, 225)),    # Royal Blue
            ("Lawless", (139, 0, 0))      # Blood Red
        ]
        
        # Initialize player data storage
        self.all_players = []
        self.player_images = {}
        
        # Generate hexagonal board (for backdrop)
        self.hexagons = self.generate_hexagonal_board()
        
        # Data storage for terrain
        self.difficult_terrain = set()
        self.walls = set()
    
    def draw_alignment_selection(self):
        self.screen.fill(self.BLACK)
        
        # Draw title
        title = self.title_font.render("Choose Your Alignment", True, self.WHITE)
        title_rect = title.get_rect()
        title_rect.centerx = self.width // 2
        title_rect.y = 200
        self.screen.blit(title, title_rect)
        
        # Draw alignment options
        for i, (name, color) in enumerate(self.alignments):
            y_pos = 300 + i * 100
            
            # Highlight selected alignment
            if i == self.selected_alignment:
                highlight_rect = pygame.Rect(self.width//2 - 150, y_pos - 10, 300, 80)
                pygame.draw.rect(self.screen, self.WHITE, highlight_rect, 3)
            
            # Draw alignment name
            alignment_text = self.menu_font.render(name, True, color)
            alignment_rect = alignment_text.get_rect()
            alignment_rect.centerx = self.width // 2
            alignment_rect.y = y_pos
            self.screen.blit(alignment_text, alignment_rect)
            
            # Draw color preview
            color_rect = pygame.Rect(self.width//2 - 50, y_pos + 40, 100, 20)
            pygame.draw.rect(self.screen, color, color_rect)
            pygame.draw.rect(self.screen, self.WHITE, color_rect, 2)
        
        # Draw instructions
        instructions = [
            "Use UP/DOWN arrows to select alignment",
            "Press ENTER to continue"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.font.render(instruction, True, self.WHITE)
            text_rect = text.get_rect()
            text_rect.centerx = self.width // 2
            text_rect.y = 600 + i * 25
            self.screen.blit(text, text_rect)
    
    def draw_player_selection(self):
        self.screen.fill(self.BLACK)
        
        alignment_name, alignment_color = self.alignments[self.selected_alignment]
        
        # Draw title
        title = self.title_font.render(f"Choose Your Player ({alignment_name} + Neutral)", True, alignment_color)
        title_rect = title.get_rect()
        title_rect.centerx = self.width // 2
        title_rect.y = 30
        self.screen.blit(title, title_rect)
        
        if not self.available_players:
            no_players_text = self.menu_font.render("No players available for this alignment", True, self.WHITE)
            text_rect = no_players_text.get_rect()
            text_rect.centerx = self.width // 2
            text_rect.centery = self.height // 2
            self.screen.blit(no_players_text, text_rect)
            return
        
        # Display high-quality character images in a grid
        start_x = 80
        start_y = 120
        image_width = 160   # 1:1.5 ratio - width (20% smaller)
        image_height = 240  # 1:1.5 ratio - height (20% smaller)
        spacing = 50
        
        for i, player_data in enumerate(self.available_players):
            x = start_x + (i % 4) * (image_width + spacing)  # 4 columns
            y = start_y + (i // 4) * (image_height + spacing + 60)  # Extra space for name
            
            # Highlight selected player with a border
            if i == self.selected_player_index:
                highlight_rect = pygame.Rect(x - 5, y - 5, image_width + 10, image_height + 50)
                pygame.draw.rect(self.screen, alignment_color, highlight_rect, 4)
            
            # Draw high-quality player image
            if player_data['name'] in self.player_images and self.player_images[player_data['name']]:
                # Scale image with smooth scaling for clarity and maintain 1:1.5 ratio
                original_image = self.player_images[player_data['name']]
                scaled_image = pygame.transform.smoothscale(original_image, (image_width, image_height))
                self.screen.blit(scaled_image, (x, y))
            else:
                # Placeholder for missing images
                placeholder_rect = pygame.Rect(x, y, image_width, image_height)
                pygame.draw.rect(self.screen, self.GRAY, placeholder_rect)
                pygame.draw.rect(self.screen, self.WHITE, placeholder_rect, 2)
                no_img_text = self.menu_font.render("No Image", True, self.WHITE)
                text_rect = no_img_text.get_rect()
                text_rect.center = placeholder_rect.center
                self.screen.blit(no_img_text, text_rect)
            
            # Draw player name below the image
            name_text = self.menu_font.render(player_data['name'].title(), True, self.WHITE)
            name_rect = name_text.get_rect()
            name_rect.centerx = x + image_width // 2
            name_rect.y = y + image_height + 5
            self.screen.blit(name_text, name_rect)
        
        # Draw instructions at the bottom
        instructions = [
            "Use ARROW KEYS to navigate",
            "Press ENTER to select player",
            "Press ESC to go back"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.font.render(instruction, True, self.WHITE)
            text_rect = text.get_rect()
            text_rect.centerx = self.width // 2
            text_rect.y = 720 + i * 20
            self.screen.blit(text, text_rect)
    
    def compress_image_with_pillow(self, image_path, max_size=(160, 240), quality=85):
        """Compress and resize image using Pillow, return pygame surface"""
        try:
            # Open image with Pillow
            with Image.open(image_path) as pil_image:
                # Convert to RGB if necessary (handles RGBA, P mode, etc.)
                if pil_image.mode in ('RGBA', 'LA', 'P'):
                    # Create white background for transparency
                    background = Image.new('RGB', pil_image.size, (255, 255, 255))
                    if pil_image.mode == 'P':
                        pil_image = pil_image.convert('RGBA')
                    background.paste(pil_image, mask=pil_image.split()[-1] if pil_image.mode in ('RGBA', 'LA') else None)
                    pil_image = background
                elif pil_image.mode != 'RGB':
                    pil_image = pil_image.convert('RGB')
                
                # Resize while maintaining aspect ratio
                pil_image = ImageOps.fit(pil_image, max_size, Image.Resampling.LANCZOS)
                
                # Compress by saving to BytesIO buffer
                buffer = io.BytesIO()
                pil_image.save(buffer, format='JPEG', quality=quality, optimize=True)
                buffer.seek(0)
                
                # Load compressed image into pygame
                pygame_image = pygame.image.load(buffer)
                return pygame_image
                
        except Exception as e:
            print(f"Error compressing image {image_path}: {e}")
            return None
    
    def load_player_data(self):
        """Load player data and compressed images"""
        try:
            # Try new format first
            player_file_path = r"D:\vsc folder\LoyalAndTheLawless\src\players.json"
            if not os.path.exists(player_file_path):
                # Fallback to old format
                player_file_path = r"D:\vsc folder\LoyalAndTheLawless\src\player.json"
            
            with open(player_file_path, 'r') as f:
                players_data = json.load(f)
            
            # Handle both old and new JSON formats
            if isinstance(players_data, dict) and any(isinstance(v, dict) and 'name' in v for v in players_data.values()):
                # Old format: keys are player IDs, values are player data
                self.all_players = []
                for player_key, player_data in players_data.items():
                    player_data['key'] = player_key
                    self.all_players.append(player_data)
            elif isinstance(players_data, list):
                # New format: direct list of player objects
                self.all_players = players_data
            else:
                print("Unknown player data format")
                self.all_players = []
            
            # Load and compress player images
            base_path = r"D:\vsc folder\LoyalAndTheLawless\src\Images"
            for player_data in self.all_players:
                image_filename = player_data.get('Photo', player_data.get('image', ''))
                if image_filename:
                    # Handle both absolute and relative paths
                    if os.path.isabs(image_filename):
                        image_path = image_filename
                    else:
                        image_path = os.path.join(base_path, image_filename)
                    
                    if os.path.exists(image_path):
                        # Use Pillow compression
                        compressed_image = self.compress_image_with_pillow(image_path)
                        if compressed_image:
                            self.player_images[player_data['name']] = compressed_image
                            print(f"Loaded and compressed image for {player_data['name']}")
                        else:
                            self.player_images[player_data['name']] = None
                    else:
                        print(f"Image not found for {player_data['name']}: {image_path}")
                        self.player_images[player_data['name']] = None
                else:
                    self.player_images[player_data['name']] = None
        
        except Exception as e:
            print(f"Error loading player data: {e}")
            self.all_players = []
            self.player_images = {}
    
    def filter_players_by_alignment(self):
        """Filter players by selected alignment + neutral characters"""
        alignment_name = self.alignments[self.selected_alignment][0].lower()
        
        # Include both the selected alignment and neutral characters
        self.available_players = [p for p in self.all_players 
                                if p.get('alignment', '').lower() == alignment_name 
                                or p.get('alignment', '').lower() == 'neutral']
        
        print(f"Available players for {alignment_name}: {[p['name'] for p in self.available_players]}")
        self.selected_player_index = 0
        
        # Safety check for empty player list
        if not self.available_players:
            print(f"Warning: No players found for alignment '{alignment_name}'. Available alignments:")
            for p in self.all_players:
                print(f"  - {p['name']}: {p.get('alignment', 'Unknown')}")
            # Add all players as fallback
            self.available_players = self.all_players.copy()
    
    def generate_hexagonal_board(self):
        """Generate hexagonal board for backdrop"""
        hexagons = []
        center_x = self.width // 2
        center_y = self.height // 2
        
        for q in range(-self.board_radius + 1, self.board_radius):
            r1 = max(-self.board_radius + 1, -q - self.board_radius + 1)
            r2 = min(self.board_radius - 1, -q + self.board_radius - 1)
            for r in range(r1, r2 + 1):
                # Convert cube coordinates to pixel coordinates
                standard_x = self.hex_radius * 1.5 * q
                standard_y = self.hex_radius * math.sqrt(3) * (r + q / 2)
                
                # Rotate by 30 degrees anticlockwise
                cos30 = math.cos(math.pi / 6)
                sin30 = math.sin(math.pi / 6)
                
                rotated_x = standard_x * cos30 - standard_y * sin30
                rotated_y = standard_x * sin30 + standard_y * cos30
                
                x = center_x + rotated_x
                y = center_y + rotated_y
                
                terrain_type = 'simple'
                color = self.SIMPLE_TERRAIN
                
                hexagons.append({
                    'q': q, 'r': r,
                    'x': x, 'y': y,
                    'terrain_type': terrain_type,
                    'color': color
                })
        
        return hexagons
    
    def load_terrain_data(self):
        """Load terrain data from JSON - stub for secondary screen"""
        pass
    
    def apply_terrain_data(self):
        """Apply terrain data to hexagons - stub for secondary screen"""
        pass
    
    def draw_board(self):
        """Draw basic board for playing state - placeholder"""
        self.screen.fill(self.WATER_COLOR)
        
        # Draw message that player was selected
        if hasattr(self, 'selected_player_data'):
            text = self.title_font.render(f"Selected: {self.selected_player_data['name']}", True, self.WHITE)
            text_rect = text.get_rect()
            text_rect.center = (self.width // 2, self.height // 2)
            self.screen.blit(text, text_rect)
            
            instruction = self.menu_font.render("Press ESC to go back", True, self.WHITE)
            inst_rect = instruction.get_rect()
            inst_rect.center = (self.width // 2, self.height // 2 + 50)
            self.screen.blit(instruction, inst_rect)

    def draw_player_card(self):
        """Draw selected player card at bottom right"""
        if not self.player:
            return
            
        # Card dimensions
        card_width = 250
        card_height = 150
        card_x = self.width - card_width - 20
        card_y = self.height - card_height - 20
        
        # Draw card background
        card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
        pygame.draw.rect(self.screen, self.GRAY, card_rect)
        pygame.draw.rect(self.screen, self.WHITE, card_rect, 2)
        
        # Draw player image
        if self.player.name in self.player_images and self.player_images[self.player.name]:
            image = pygame.transform.scale(self.player_images[self.player.name], (80, 80))
            self.screen.blit(image, (card_x + 10, card_y + 10))
        
        # Draw player stats
        info_x = card_x + 100
        name_text = self.font.render(self.player.name, True, self.BLACK)
        self.screen.blit(name_text, (info_x, card_y + 10))
        
        health_text = self.font.render(f"Health: {self.player.current_health}/{self.player.max_health}", True, self.BLACK)
        self.screen.blit(health_text, (info_x, card_y + 30))
        
        damage_text = self.font.render(f"Damage: {self.player.damage}", True, self.BLACK)
        self.screen.blit(damage_text, (info_x, card_y + 50))
        
        moves_text = self.font.render(f"Moves: {self.player.current_moves}/{self.player.max_moves}", True, self.BLACK)
        self.screen.blit(moves_text, (info_x, card_y + 70))
        
        range_text = self.font.render(f"Range: {self.player.range}", True, self.BLACK)
        self.screen.blit(range_text, (info_x, card_y + 90))
        
        # Draw turn instructions
        turn_text = self.font.render("Press N for new turn", True, self.BLACK)
        self.screen.blit(turn_text, (info_x, card_y + 120))
    

    def handle_alignment_input(self, event):
        """Handle input for alignment selection"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_alignment = (self.selected_alignment - 1) % len(self.alignments)
            elif event.key == pygame.K_DOWN:
                self.selected_alignment = (self.selected_alignment + 1) % len(self.alignments)
            elif event.key == pygame.K_RETURN:
                self.filter_players_by_alignment()
                self.game_state = "player_selection"
            elif event.key == pygame.K_ESCAPE:
                return False
        return True
    
    def handle_player_input(self, event):
        """Handle input for player selection"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_player_index = max(0, self.selected_player_index - 1)
            elif event.key == pygame.K_RIGHT:
                self.selected_player_index = min(len(self.available_players) - 1, self.selected_player_index + 1)
            elif event.key == pygame.K_UP:
                self.selected_player_index = max(0, self.selected_player_index - 3)
            elif event.key == pygame.K_DOWN:
                self.selected_player_index = min(len(self.available_players) - 1, self.selected_player_index + 3)
            elif event.key == pygame.K_RETURN:
                # Create player from selected data
                player_data = self.available_players[self.selected_player_index]
                self.selected_player_data = player_data
                # TODO: Uncomment when Player class is available
                # self.player = Player(player_data)
                print(f"Selected player: {player_data['name']}")
                self.game_state = "playing"
            elif event.key == pygame.K_ESCAPE:
                self.game_state = "alignment_selection"
        return True
    
    def handle_game_input(self, event):
        """Handle input during gameplay"""
        if event.type == pygame.KEYDOWN:
            # Handle ability screen input first
            if self.player and self.player.handle_ability_input(event):
                return True
            
            if event.key == pygame.K_ESCAPE:
                return False
            elif event.key == pygame.K_n:
                # New turn - reset moves
                if self.player:
                    self.player.new_turn()
            elif event.key == pygame.K_s:
                if self.player:
                    self.player.toggle_ability_screen()
            # Handle player movement
            elif self.player and event.key in self.player.movement_keys:
                self.player.move(event.key, self.difficult_terrain, self.walls)
        return True
    
    def run(self):
        """Main display loop"""
        print("Hexagonal Board - Simple & Difficult Terrain")
        print("Terrain loaded from difficult_terrain.json")
        print("Press ESC to quit")
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                else:
                    if self.game_state == "alignment_selection":
                        running = self.handle_alignment_input(event)
                    elif self.game_state == "player_selection":
                        running = self.handle_player_input(event)
                    elif self.game_state == "playing":
                        running = self.handle_game_input(event)
            
            # Draw appropriate screen
            if self.game_state == "alignment_selection":
                self.draw_alignment_selection()
            elif self.game_state == "player_selection":
                self.draw_player_selection()
            elif self.game_state == "playing":
                self.draw_board()
                
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    board = HexBoard()
    board.run()