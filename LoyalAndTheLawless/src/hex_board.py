import pygame
import math
import random
import json
import os

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
        
        # Generate hexagonal board (6 hexes per side)
        self.board_radius = 6
        self.hexagons = self.generate_hexagonal_board()
        
        # Data storage
        self.difficult_terrain = set()  # Set of (q, r) coordinates
        self.walls = set()  # Set of ((q1, r1), (q2, r2)) coordinate pairs
        
        # JSON file path
        self.terrain_file = r"C:\Users\Denver Zuzarte\vsc folder\LoyalAndTheLawless\PDA\src\terrain.json"
        
        # Load existing data
        self.load_terrain_data()
        
        # Apply loaded terrain data to hexagons
        self.apply_terrain_data()
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 18)
        self.coord_font = pygame.font.Font(None, 16)
    
    def generate_hexagonal_board(self):
        """Generate hexagonal board with terrain types"""
        hexagons = []
        center_x = self.width // 2
        center_y = self.height // 2
        
        for q in range(-self.board_radius + 1, self.board_radius):
            r1 = max(-self.board_radius + 1, -q - self.board_radius + 1)
            r2 = min(self.board_radius - 1, -q + self.board_radius - 1)
            for r in range(r1, r2 + 1):
                # Convert cube coordinates to pixel coordinates
                x = center_x + self.hex_radius * 1.5 * q
                y = center_y + self.hex_radius * math.sqrt(3) * (r + q / 2)
                
                # All hexes are now land terrain (simple by default)
                #if :
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
        """Load terrain data from unified JSON file"""
        try:
            if os.path.exists(self.terrain_file):
                with open(self.terrain_file, 'r') as f:
                    data = json.load(f)
                    
                    # Handle different data structures
                    if isinstance(data, dict):
                        # If it's a dictionary with separate sections
                        terrain_list = data.get('difficult terrain', [])
                        print(terrain_list)
                        walls_list = data.get('walls', [])
                    elif isinstance(data, list):
                        # If it's just a list of difficult terrain coordinates
                        terrain_list = data
                        walls_list = []
                    else:
                        terrain_list = []
                        walls_list = []
                    
                    self.difficult_terrain = set(tuple(coord) for coord in terrain_list)
                    self.walls = set(tuple(tuple(coord) for coord in wall) for wall in walls_list)
                    
                    print(f"Loaded {len(self.difficult_terrain)} difficult terrain coordinates")
                    for coord in self.difficult_terrain:
                        print(f"  Difficult terrain at: {coord}")
                    print(f"Loaded {len(self.walls)} walls")
            else:
                print(f"Terrain file {self.terrain_file} not found, starting with empty terrain")
                self.difficult_terrain = set()
                self.walls = set()
        except Exception as e:
            print(f"Error loading terrain data: {e}")
            self.difficult_terrain = set()
            self.walls = set()
    
    def save_terrain_data(self):
        """Save difficult terrain coordinates to JSON file"""
        try:
            terrain_list = list(self.difficult_terrain)
            with open(self.terrain_file, 'w') as f:
                json.dump(terrain_list, f, indent=2)
            print(f"Saved {len(self.difficult_terrain)} difficult terrain coordinates")
        except Exception as e:
            print(f"Error saving terrain data: {e}")
    
    
    def apply_terrain_data(self):
        """Apply loaded terrain data to hexagon objects"""
        for hex_tile in self.hexagons:
            coord = (hex_tile['q'], hex_tile['r'])
            if coord in self.difficult_terrain:
                hex_tile['terrain_type'] = 'difficult'
                hex_tile['color'] = self.DIFFICULT_TERRAIN
    
    def hex_corners(self, center_x, center_y):
        """Calculate the 6 corners of a hexagon"""
        corners = []
        for i in range(6):
            angle = i * math.pi / 3
            x = center_x + self.hex_radius * math.cos(angle)
            y = center_y + self.hex_radius * math.sin(angle)
            corners.append((x, y))
        return corners
    
    def draw_hexagon(self, hex_tile):
        """Draw a single hexagon with coordinates"""
        corners = self.hex_corners(hex_tile['x'], hex_tile['y'])
        
        # Fill hexagon with terrain color
        pygame.draw.polygon(self.screen, hex_tile['color'], corners)
        
        # Draw black border
        pygame.draw.polygon(self.screen, self.BLACK, corners, 3)
        
        # Draw coordinates on all hexes
        coord_text = f"({hex_tile['q']},{hex_tile['r']})"
        text_surface = self.coord_font.render(coord_text, True, self.BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = (int(hex_tile['x']), int(hex_tile['y'] - 5))
        self.screen.blit(text_surface, text_rect)
        
        # Add "D" marker for difficult terrain
        if hex_tile['terrain_type'] == 'difficult':
            d_text = self.font.render("D", True, self.WHITE)
            d_rect = d_text.get_rect()
            d_rect.center = (int(hex_tile['x']), int(hex_tile['y'] + 10))
            self.screen.blit(d_text, d_rect)
    
    def has_wall_between(self, coord1, coord2):
        """Check if there's a wall between two coordinates (order independent)"""
        wall1 = (coord1, coord2)
        wall2 = (coord2, coord1)
        return wall1 in self.walls or wall2 in self.walls
    
    def draw_walls(self):
        """Draw all walls as thick grey lines between hexes"""
        for wall in self.walls:
            coord1, coord2 = wall
            
            # Find the hex tiles for these coordinates
            hex1 = None
            hex2 = None
            
            for hex_tile in self.hexagons:
                if (hex_tile['q'], hex_tile['r']) == coord1:
                    hex1 = hex_tile
                elif (hex_tile['q'], hex_tile['r']) == coord2:
                    hex2 = hex_tile
            
            # If both hexes exist, draw wall between them
            if hex1 and hex2:
                # Calculate midpoint between hex centers
                mid_x = (hex1['x'] + hex2['x']) / 2
                mid_y = (hex1['y'] + hex2['y']) / 2
                
                # Calculate direction vector from hex1 to hex2
                dx = hex2['x'] - hex1['x']
                dy = hex2['y'] - hex1['y']
                
                # Calculate perpendicular vector for wall thickness
                length = math.sqrt(dx*dx + dy*dy)
                if length > 0:
                    # Normalize and rotate 90 degrees
                    perp_x = -dy / length * self.hex_radius * 0.6
                    perp_y = dx / length * self.hex_radius * 0.6
                    
                    # Wall endpoints
                    wall_start = (mid_x + perp_x, mid_y + perp_y)
                    wall_end = (mid_x - perp_x, mid_y - perp_y)
                    
                    # Draw thick grey wall
                    pygame.draw.line(self.screen, (128, 128, 128), wall_start, wall_end, 8)
    
    def draw_board(self):
        """Draw the complete hexagonal board"""
        # Clear screen with dark background
        self.screen.fill(self.WATER_COLOR)
        
        # Draw all hexagons
        for hex_tile in self.hexagons:
            self.draw_hexagon(hex_tile)
        
        # Draw walls on top of hexagons
        self.draw_walls()
        
        # Draw title
        title = self.font.render("Hexagonal Board - Simple & Difficult Terrain", True, self.WHITE)
        title_rect = title.get_rect()
        title_rect.centerx = self.width // 2
        title_rect.y = 20
        self.screen.blit(title, title_rect)
        
        # Draw legend
        legend_items = [
            ("Simple Terrain (Light Ochre)", self.SIMPLE_TERRAIN),
            ("Difficult Terrain (Brown)", self.DIFFICULT_TERRAIN)
        ]
        
        for i, (name, color) in enumerate(legend_items):
            y_pos = 60 + i * 25
            # Draw colored square
            pygame.draw.rect(self.screen, color, (20, y_pos, 20, 20))
            pygame.draw.rect(self.screen, self.BLACK, (20, y_pos, 20, 20), 1)
            # Draw text
            text = self.font.render(name, True, self.WHITE)
            self.screen.blit(text, (50, y_pos))
        
        # Draw instructions
        instructions = [
            "Terrain loaded from difficult_terrain.json",
            "Press ESC to quit"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.font.render(instruction, True, self.WHITE)
            self.screen.blit(text, (20, 160 + i * 25))
    
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
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    board = HexBoard()
    board.run()