import players
import sampleboard
import pygame

if __name__ == "__main__":
    # Create sample images for testing
    sampleboard.create_sample_images()
    
    
    print("Controls:")
    print("- Click on hexagons to see their coordinates")
    print("- Use WASD + E/Z to move player (4 moves max):")
    print("  D: +1,+0  |  E: +1,-1  |  W: 0,-1")
    print("  A: -1,+0  |  Z: -1,+1  |  X: 0,+1")
    print("- Click RESET button to restore 4 moves")
    print("- Press ESC to quit")
    print("Board is rotated 60 degrees counter-clockwise")
    print("N changes the turn")
    
    board.run()
        # Initialize pygame for testing
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Enhanced Player Class Test")
    clock = pygame.time.Clock()
    
    # Create example players with different ability usage limits
    players = [
        Player("Blackbeard", "lawless",
                "Steal gold from adjacent players and gain extra movement", 
                "Cannon Barrage: Deal massive damage to all players within 2 hexes, ignoring cover",
                ability_n=3, s_ability_n=2),
        Player("Captain Hook", "lawless",
                "Hook an enemy and pull them closer while dealing damage",
                "Pirate's Curse: Mark a target - they lose gold every turn until curse is broken",
                ability_n=2, s_ability_n=1),
        Player("Admiral Sterling", "loyal",
                "Rally nearby allies, granting them bonus actions and movement",
                "Naval Bombardment: Call in fleet support to devastate a large area",
                ability_n=4, s_ability_n=1)
    ]

    # Create ability panel
    ability_panel = AbilityPanel(175, 125)
    
    current_player_index = 0
    font = pygame.font.Font(None, 20)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    # Open ability panel for current player
                    ability_panel.open(players[current_player_index])
                elif event.key == pygame.K_n:
                    # Next player
                    current_player_index = (current_player_index + 1) % len(players)
                elif event.key == pygame.K_r:
                    # Reset current player's turn
                    players[current_player_index].reset_turn()
                    print(f"Reset {players[current_player_index].name}'s turn")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle ability panel clicks
                ability_panel.handle_click(event.pos)
        
        # Draw everything
        screen.fill((30, 30, 30))
        
        # Draw current player info
        current_player = players[current_player_index]
        status_text = current_player.get_status_text()
        status_surface = font.render(status_text, True, current_player.get_faction_color())
        screen.blit(status_surface, (20, 20))
        
        for i, instruction in enumerate(instructions):
            text_surface = font.render(instruction, True, (255, 255, 255))
            screen.blit(text_surface, (20, 50 + i * 22))
        
        # Draw player list
        list_y = 180
        for i, player in enumerate(players):
            prefix = ">>> " if i == current_player_index else "    "
            player_text = f"{prefix}{player.name} (Ability: {player.ability_uses}/{player.max_ability_uses}, Special: {player.special_ability_uses}/{player.max_special_ability_uses})"
            color = player.get_faction_color() if i == current_player_index else (180, 180, 180)
            text_surface = font.render(player_text, True, color)
            screen.blit(text_surface, (20, list_y + i * 25))
        
        # Draw ability panel
        ability_panel.draw(screen)
        
    pygame.quit