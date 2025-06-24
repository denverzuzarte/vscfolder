import pygame
import math
from PIL import Image, ImageDraw

class Player:
    def __init__(self, name, faction, action_desc="", special_action_desc="", image_path=None, 
                 ability_n=1, s_ability_n=1,moves_left=2):
        """
        Initialize a player with faction, abilities, and optional image
        
        Args:
            name (str): Player's name
            faction (str): 'loyal' (blue), 'lawless' (red), or 'special' (royal purple)
            action_desc (str): Description of the player's regular action ability
            special_action_desc (str): Description of the player's special action ability
            image_path (str): Path to player's image file (optional)
            ability_n (int): Number of times regular ability can be used per turn
            s_ability_n (int): Number of times special ability can be used per turn
        """
        self.name = name
        self.faction = faction.lower()
        self.action_desc = action_desc
        self.special_action_desc = special_action_desc
        self.image_path = image_path
        self.image = None
        
        # Ability usage limits
        self.max_ability_uses = ability_n
        self.max_special_ability_uses = s_ability_n
        
        # Faction colors
        self.faction_colors = {
            'loyal': (70, 130, 180),      # Blue
            'lawless': (220, 20, 60),     # Red  
            'special': (128, 0, 128)      # Royal Purple
        }
        
        # Game state
        self.position = None  # (q, r) coordinates on hex board
        self.moves_used = 0
        self.max_moves = 4
        self.is_active = False
        
        # Ability usage tracking
        self.ability_uses = 0
        self.special_ability_uses = 0
        
    def get_faction_color(self):
        """Get the color associated with this player's faction"""
        return self.faction_colors.get(self.faction, (128, 128, 128))
    
    def get_faction_name(self):
        """Get the formatted faction name"""
        faction_names = {
            'loyal': 'Loyal',
            'lawless': 'Lawless',
            'special': 'Royal'
        }
        return faction_names.get(self.faction, 'Unknown')
    
    def reset_turn(self):
        """Reset all turn-based resources (moves, actions)"""
        self.moves_used = 0
        self.ability_uses = 0
        self.special_ability_uses = 0
    
    def can_move(self):
        """Check if player can still move"""
        return self.moves_used < self.max_moves
    
    def use_move(self):
        """Use one move, returns True if successful"""
        if self.can_move():
            self.moves_used += 1
            return True
        return False
    
    def can_use_ability(self):
        """Check if player can use their regular ability"""
        return self.ability_uses < self.max_ability_uses
    
    def can_use_special_ability(self):
        """Check if player can use their special ability"""
        return self.special_ability_uses < self.max_special_ability_uses
    
    def use_ability(self):
        """Use the player's regular ability"""
        if self.can_use_ability():
            self.ability_uses += 1
            print(f"{self.name} used their ability ({self.ability_uses}/{self.max_ability_uses}): {self.action_desc}")
            return True
        else:
            print(f"{self.name} has used all their ability uses this turn! ({self.ability_uses}/{self.max_ability_uses})")
            return False
    
    def use_special_ability(self):
        """Use the player's special ability"""
        if self.can_use_special_ability():
            self.special_ability_uses += 1
            print(f"{self.name} used their special ability ({self.special_ability_uses}/{self.max_special_ability_uses}): {self.special_action_desc}")
            return True
        else:
            print(f"{self.name} has used all their special ability uses this turn! ({self.special_ability_uses}/{self.max_special_ability_uses})")
            return False
    
    def get_status_text(self):
        """Get a formatted status string for UI display"""
        faction_name = self.get_faction_name()
        moves_text = f"Moves: {self.moves_used}/{self.max_moves}"
        ability_status = f"Ability: {self.ability_uses}/{self.max_ability_uses}"
        special_status = f"Special: {self.special_ability_uses}/{self.max_special_ability_uses}"
        
        return f"{self.name} ({faction_name}) | {moves_text} | {ability_status} | {special_status}"

class AbilityPanel:
    def __init__(self, x, y, width=450, height=350):
        """
        Create an ability panel UI for displaying and using player abilities
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.is_open = False
        self.current_player = None
        
        # Button dimensions
        button_width = 180
        button_height = 45
        button_spacing = 30
        
        # Calculate button positions - more separated
        buttons_start_y = y + 140
        button1_x = x + 30
        button2_x = x + width - button_width - 30
        
        # Create separate sections for each ability
        self.action_button = pygame.Rect(button1_x, buttons_start_y, button_width, button_height)
        self.special_button = pygame.Rect(button2_x, buttons_start_y, button_width, button_height)
        
        # Add usage counter displays above buttons
        self.action_counter_rect = pygame.Rect(button1_x, buttons_start_y - 25, button_width, 20)
        self.special_counter_rect = pygame.Rect(button2_x, buttons_start_y - 25, button_width, 20)
        
        self.close_button = pygame.Rect(x + width - 30, y + 10, 20, 20)
        
        # Fonts
        self.title_font = pygame.font.Font(None, 28)
        self.text_font = pygame.font.Font(None, 18)
        self.button_font = pygame.font.Font(None, 20)
        self.counter_font = pygame.font.Font(None, 16)
        
        # Colors
        self.bg_color = (45, 45, 45, 220)  # Semi-transparent dark gray
        self.border_color = (255, 255, 255)
        self.button_color = (70, 120, 180)
        self.button_hover_color = (90, 140, 200)
        self.button_disabled_color = (60, 60, 60)
        self.special_button_color = (150, 70, 150)
        self.special_button_hover_color = (170, 90, 170)
        self.text_color = (255, 255, 255)
        self.counter_color = (200, 200, 200)
        self.close_button_color = (200, 50, 50)
        self.section_divider_color = (100, 100, 100)
    
    def open(self, player):
        """Open the ability panel for a specific player"""
        self.current_player = player
        self.is_open = True
    
    def close(self):
        """Close the ability panel"""
        self.is_open = False
        self.current_player = None
    
    def handle_click(self, mouse_pos):
        """Handle mouse clicks on the ability panel"""
        if not self.is_open or not self.current_player:
            return False
        
        if self.close_button.collidepoint(mouse_pos):
            self.close()
            return True
        
        if self.action_button.collidepoint(mouse_pos):
            self.current_player.use_ability()
            return True
        
        if self.special_button.collidepoint(mouse_pos):
            self.current_player.use_special_ability()
            return True
        
        # Click anywhere else on panel to close
        if self.rect.collidepoint(mouse_pos):
            self.close()
            return True
        
        return False
    
    def draw(self, screen):
        """Draw the ability panel"""
        if not self.is_open or not self.current_player:
            return
        
        # Create a surface with per-pixel alpha for transparency
        panel_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        panel_surface.fill(self.bg_color)
        
        # Draw border
        pygame.draw.rect(panel_surface, self.border_color, 
                        (0, 0, self.rect.width, self.rect.height), 2)
        
        # Draw title
        title_text = f"{self.current_player.name}'s Abilities"
        title_surface = self.title_font.render(title_text, True, self.current_player.get_faction_color())
        title_rect = title_surface.get_rect()
        title_rect.centerx = self.rect.width // 2
        title_rect.y = 15
        panel_surface.blit(title_surface, title_rect)
        
        # Draw faction
        faction_text = f"Faction: {self.current_player.get_faction_name()}"
        faction_surface = self.text_font.render(faction_text, True, self.text_color)
        faction_rect = faction_surface.get_rect()
        faction_rect.centerx = self.rect.width // 2
        faction_rect.y = 45
        panel_surface.blit(faction_surface, faction_rect)
        
        # Draw vertical divider line
        divider_x = self.rect.width // 2
        pygame.draw.line(panel_surface, self.section_divider_color, 
                        (divider_x, 80), (divider_x, self.rect.height - 80), 2)
        
        # Draw regular ability section (left side)
        if self.current_player.action_desc:
            ability_title = self.text_font.render("Regular Ability:", True, self.text_color)
            panel_surface.blit(ability_title, (20, 80))
            
            # Word wrap the ability description
            self.draw_wrapped_text(panel_surface, self.current_player.action_desc, 
                                 20, 100, divider_x - 30, self.text_color)
        
        # Draw special ability section (right side)
        if self.current_player.special_action_desc:
            special_title = self.text_font.render("Special Ability:", True, self.text_color)
            panel_surface.blit(special_title, (divider_x + 20, 80))
            
            # Word wrap the special ability description
            self.draw_wrapped_text(panel_surface, self.current_player.special_action_desc,
                                 divider_x + 20, 100, divider_x - 30, self.text_color)
        
        # Draw usage counters
        action_counter_text = f"Uses: {self.current_player.ability_uses}/{self.current_player.max_ability_uses}"
        counter_surface = self.counter_font.render(action_counter_text, True, self.counter_color)
        counter_rect = counter_surface.get_rect()
        counter_rect.centerx = self.action_counter_rect.centerx - self.rect.x
        counter_rect.y = self.action_counter_rect.y - self.rect.y
        panel_surface.blit(counter_surface, counter_rect)
        
        special_counter_text = f"Uses: {self.current_player.special_ability_uses}/{self.current_player.max_special_ability_uses}"
        special_counter_surface = self.counter_font.render(special_counter_text, True, self.counter_color)
        special_counter_rect = special_counter_surface.get_rect()
        special_counter_rect.centerx = self.special_counter_rect.centerx - self.rect.x
        special_counter_rect.y = self.special_counter_rect.y - self.rect.y
        panel_surface.blit(special_counter_surface, special_counter_rect)
        
        # Draw regular ability button
        action_color = (self.button_disabled_color if not self.current_player.can_use_ability()
                       else self.button_color)
        pygame.draw.rect(panel_surface, action_color, 
                        (self.action_button.x - self.rect.x, self.action_button.y - self.rect.y,
                         self.action_button.width, self.action_button.height))
        
        # Add button border
        pygame.draw.rect(panel_surface, self.border_color,
                        (self.action_button.x - self.rect.x, self.action_button.y - self.rect.y,
                         self.action_button.width, self.action_button.height), 2)
        
        action_text = "Use Ability"
        if not self.current_player.can_use_ability():
            action_text = "No Uses Left"
        
        action_text_surface = self.button_font.render(action_text, True, self.text_color)
        action_text_rect = action_text_surface.get_rect()
        action_text_rect.center = (self.action_button.x - self.rect.x + self.action_button.width // 2, 
                                  self.action_button.y - self.rect.y + self.action_button.height // 2)
        panel_surface.blit(action_text_surface, action_text_rect)
        
        # Draw special ability button
        special_color = (self.button_disabled_color if not self.current_player.can_use_special_ability()
                        else self.special_button_color)
        pygame.draw.rect(panel_surface, special_color,
                        (self.special_button.x - self.rect.x, self.special_button.y - self.rect.y,
                         self.special_button.width, self.special_button.height))
        
        # Add button border
        pygame.draw.rect(panel_surface, self.border_color,
                        (self.special_button.x - self.rect.x, self.special_button.y - self.rect.y,
                         self.special_button.width, self.special_button.height), 2)
        
        special_text = "Use Special"
        if not self.current_player.can_use_special_ability():
            special_text = "No Uses Left"
        
        special_text_surface = self.button_font.render(special_text, True, self.text_color)
        special_text_rect = special_text_surface.get_rect()
        special_text_rect.center = (self.special_button.x - self.rect.x + self.special_button.width // 2,
                                   self.special_button.y - self.rect.y + self.special_button.height // 2)
        panel_surface.blit(special_text_surface, special_text_rect)
        
        # Draw close button
        pygame.draw.rect(panel_surface, self.close_button_color,
                        (self.close_button.x - self.rect.x, self.close_button.y - self.rect.y,
                         self.close_button.width, self.close_button.height))
        close_text = self.text_font.render("×", True, self.text_color)
        close_text_rect = close_text.get_rect()
        close_text_rect.center = (self.close_button.x - self.rect.x + self.close_button.width // 2,
                                 self.close_button.y - self.rect.y + self.close_button.height // 2)
        panel_surface.blit(close_text, close_text_rect)
        
        # Blit the panel to the main screen
        screen.blit(panel_surface, self.rect)
    
    def draw_wrapped_text(self, surface, text, x, y, max_width, color):
        """Draw text with word wrapping"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surface = self.text_font.render(test_line, True, color)
            
            if test_surface.get_width() <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)  # Single word too long, add it anyway
        
        if current_line:
            lines.append(' '.join(current_line))
        
        for i, line in enumerate(lines):
            line_surface = self.text_font.render(line, True, color)
            surface.blit(line_surface, (x, y + i * 18))

print ("Players cache has been updated")