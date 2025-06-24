import pygame
pygame.init();
# screen size
screenheight = 600;
screenwidth = 800;
screen = pygame.display.set_mode((screenwidth,screenheight));
# making a rectangle
rect = pygame.Rect((300,250,50,50));rect = pygame.Rect((400,300,50,50));
# caption of the game
pygame.display.set_caption('learning pygame');
#icon of the game
icon=pygame.transform.scale(pygame.image.load(r"C:\Users\Denver Zuzarte\game images\pachycephalosaurus.png"),(50,50));
pygame.display.set_icon(icon);
#load background
background = pygame.image.load(r"C:\Users\Denver Zuzarte\Documents\WhatsApp Image 2024-08-16 at 11.51.47_a2cef3e6.jpg");
# player creation
class obstacle:
    def __init__(self,height,width,posx,posy):
        obs=pygame.rect(height,width,posx,posy);
        
def player (x,y):
    screen.blit(icon,(x,y));
# game loop
run = True;
while run:
    #filling the screen
    screen.fill((0,0,0))
        # setting up a key to control rect
    w = pygame.key.get_pressed();
    a = pygame.key.get_pressed();
    s = pygame.key.get_pressed();
    d = pygame.key.get_pressed();
    if a[pygame.K_a] == True :
        rect.move_ip(-1,0);
    if d[pygame.K_d] == True :
        rect.move_ip(1,0);
    if s[pygame.K_w] == True :
        rect.move_ip(0,-1);
    if w[pygame.K_s] == True :
        rect.move_ip(0,1);
        #drawing the rectangle
    pygame.draw.rect(screen,(255,255,255),rect);
    #calling the player
    player(20,30);
    # moving the player
    t = pygame.key.get_pressed();
    f = pygame.key.get_pressed();
    g = pygame.key.get_pressed();
    h = pygame.key.get_pressed();
    if f[pygame.K_f] == True :
        player.move_ip(-1,0);
    if h[pygame.K_h] == True :
        player.move_ip(1,0);
    if g[pygame.K_g] == True :
        player.move_ip(0,-1);
    if t[pygame.K_t] == True :
        player.move_ip(0,1);
    # event for exiting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False;
    pygame.display.update();
pygame.quit();