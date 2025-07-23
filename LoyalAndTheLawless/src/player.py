import pygame
import math

class Player:
    """Player class with health, attack damage, and abilities"""
    
    def __init__(self, player_id, start_q, start_r, hex_radius=40):
        self.player_id = player_id
        self.q = start_q  # Hex coordinate q
        self.r = start_r  # Hex coordinate r
        self.hex_radius = hex_radius
        
        # Player stats
        self.health = 100
        self.max_health = 100
        self.attack_damage = 25
        
        # Movement
        self.move_count = 0
        
        # UI state
        self.ability_screen_open = False
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.BLUE = (25, 100, 200)
        self.GRAY = (128, 128, 128)
        self.LIGHT_GRAY = (200, 200, 200)
        
        # Font for player number (will be initialized when needed)
        self.font = None
        self.ui_font = None
        
        # Hexagonal movement directions
        self.movement_keys = {
            pygame.K_d: (1, 0),    # d: +1,0
            pygame.K_e: (1, -1),   # e: +1,-1  
            pygame.K_w: (0, -1),   # w: 0,-1
            pygame.K_a: (-1, 0),   # a: -1,0
            pygame.K_z: (-1, 1),   # z: -1,+1
            pygame.K_x: (0, 1)     # x: 0,+1
        }
    
    def move(self, direction_key):
        """Move player in hexagonal direction"""
        if direction_key in self.movement_keys:
            dq, dr = self.movement_keys[direction_key]
            self.q += dq
            self.r += dr
            self.move_count += 1
            return True
        return False
    
    def toggle_ability_screen(self):
        """Toggle the ability screen on/off"""
        self.ability_screen_open = not self.ability_screen_open
    
    def close_ability_screen(self):
        """Close the ability screen"""
        self.ability_screen_open = False
    
    def use_attack(self):
        """Use basic attack ability"""
        print(f"Player {self.player_id} uses attack for {self.attack_damage} damage!")
        self.close_ability_screen()
    
    def use_special_move(self):
        """Use special move ability"""
        print(f"Player {self.player_id} uses special move!")
        self.close_ability_screen()
    
    def take_damage(self, damage):
        """Take damage and reduce health"""
        self.health = max(0, self.health - damage)
        return self.health <= 0  # Return True if player died
    
    def heal(self, amount):
        """Heal player"""
        self.health = min(self.max_health, self.health + amount)
    
    def get_pixel_position(self, center_x, center_y):
        """Convert hex coordinates to pixel coordinates"""
        x = center_x + self.hex_radius * 1.5 * self.q
        y = center_y + self.hex_radius * math.sqrt(3) * (self.r + self.q / 2)
        return x, y
    
    def _ensure_fonts(self):
        """Initialize fonts if not already done"""
        if self.font is None:
            self.font = pygame.font.Font(None, 24)
        if self.ui_font is None:
            self.ui_font = pygame.font.Font(None, 36)
    
    def draw_player(self, screen, center_x, center_y):
        """Draw the player as a small black coin with player number"""
        self._ensure_fonts()
        x, y = self.get_pixel_position(center_x, center_y)
        
        # Draw player coin (smaller than hex radius)
        coin_radius = self.hex_radius // 3
        pygame.draw.circle(screen, self.BLACK, (int(x), int(y)), coin_radius)
        pygame.draw.circle(screen, self.WHITE, (int(x), int(y)), coin_radius, 2)
        
        # Draw player number
        player_text = self.font.render(str(self.player_id), True, self.WHITE)
        text_rect = player_text.get_rect()
        text_rect.center = (int(x), int(y))
        screen.blit(player_text, text_rect)
    
    def draw_ability_screen(self, screen, screen_width, screen_height):
        """Draw the ability screen overlay"""
        if not self.ability_screen_open:
            return
        
        self._ensure_fonts()
        
        # Semi-transparent overlay
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(128)
        overlay.fill(self.BLACK)
        screen.blit(overlay, (0, 0))
        
        # Ability screen background
        screen_rect = pygame.Rect(screen_width//4, screen_height//4, 
                                screen_width//2, screen_height//2)
        pygame.draw.rect(screen, self.BLUE, screen_rect)
        pygame.draw.rect(screen, self.WHITE, screen_rect, 3)
        
        # Title
        title_text = self.ui_font.render(f"Player {self.player_id} Abilities", True, self.WHITE)
        title_rect = title_text.get_rect()
        title_rect.centerx = screen_width // 2
        title_rect.y = screen_height//4 + 30
        screen.blit(title_text, title_rect)
        
        # Player stats
        stats_y = screen_height//4 + 80
        health_text = self.ui_font.render(f"Health: {self.health}/{self.max_health}", True, self.WHITE)
        screen.blit(health_text, (screen_width//4 + 20, stats_y))
        
        damage_text = self.ui_font.render(f"Attack Damage: {self.attack_damage}", True, self.WHITE)
        screen.blit(damage_text, (screen_width//4 + 20, stats_y + 40))
        
        moves_text = self.ui_font.render(f"Moves: {self.move_count}", True, self.WHITE)
        screen.blit(moves_text, (screen_width//4 + 20, stats_y + 80))
        
        # Ability options
        options_y = screen_height//4 + 200
        attack_text = self.ui_font.render("1) Attack", True, self.WHITE)
        screen.blit(attack_text, (screen_width//4 + 20, options_y))
        
        special_text = self.ui_font.render("2) Special Move", True, self.WHITE)
        screen.blit(special_text, (screen_width//4 + 20, options_y + 50))
        
        # Instructions
        instructions_y = screen_height//4 + screen_height//2 - 80
        instruction_texts = [
            "Press 1 for Attack, 2 for Special Move",
            "Press S or ESC to close"
        ]
        
        for i, instruction in enumerate(instruction_texts):
            text = self.ui_font.render(instruction, True, self.WHITE)
            text_rect = text.get_rect()
            text_rect.centerx = screen_width // 2
            text_rect.y = instructions_y + i * 30
            screen.blit(text, text_rect)
    
    def handle_ability_input(self, event):
        """Handle input when ability screen is open"""
        if not self.ability_screen_open:
            return False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.use_attack()
                return True
            elif event.key == pygame.K_2:
                self.use_special_move()
                return True
            elif event.key == pygame.K_s or event.key == pygame.K_ESCAPE:
                self.close_ability_screen()
                return True
        
        return False


# Starting positions
x1s, y1s = 0, 0  # Player 1 starting position

# Create player1 object
player1 = Player(player_id=1, start_q=x1s, start_r=y1s)