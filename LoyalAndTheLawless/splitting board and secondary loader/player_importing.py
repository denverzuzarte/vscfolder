import pygame
import json

class PlayerImporting:
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
        
        # Player selection state
        self.game_state = "alignment_selection"  # alignment_selection, player_selection, playing
        self.selected_alignment = 0
        self.selected_player_index = 0
        self.available_players = []
        self.player_images = {}
        self.player = None
        
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
    
    def load_player_data(self):
        try:
            with open(r"D:\\vsc folder\\LoyalAndTheLawless\\src\\player.json", 'r') as f:
                players_data = json.load(f)
                
            # Convert to list format for easier handling
            self.all_players = []
            for player_key, player_data in players_data.items():
                player_data['key'] = player_key
                self.all_players.append(player_data)
                
            # Load player images
            for player_data in self.all_players:
                image_path = player_data.get('Photo', '')
                if image_path:
                    try:
                        image = pygame.image.load(image_path)
                        image = pygame.transform.scale(image, (120, 120))
                        self.player_images[player_data['name']] = image
                    except Exception as e:
                        print(f"Could not load image for {player_data['name']}: {e}")
                        self.player_images[player_data['name']] = None
                        
        except Exception as e:
            print(f"Error loading player data: {e}")
            self.all_players = []
    
    def filter_players_by_alignment(self):
        """Filter players by selected alignment + neutral characters"""
        alignment_name = self.alignments[self.selected_alignment][0].lower()
        
        # Include both the selected alignment and neutral characters
        self.available_players = [p for p in self.all_players 
                                if p.get('alignment', '').lower() == alignment_name 
                                or p.get('alignment', '').lower() == 'neutral']
        
        print(f"Available players for {alignment_name}: {[p['name'] for p in self.available_players]}")
        self.selected_player_index = 0
