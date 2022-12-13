import pygame
import sys
from pygame import mixer
from fighter import Fighter
from button import Button

mixer.init()
pygame.init()

#create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mortal Kombat")

BG = pygame.image.load("assets/images/background/menubg.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/images/FONTS/Halloween Morning.ttf", size)
def get_font2(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/images/FONTS/Halloween Morning.ttf", size)

def play():

    #set framerate
    clock = pygame.time.Clock()
    FPS = 60

    #define colours
    RED = (255, 0, 0)
    GREEN = (0 , 255 , 0)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)

    #define game variables
    intro_count = 3
    last_count_update = pygame.time.get_ticks()
    score = [0, 0]#player scores. [P1, P2]
    round_over = False
    ROUND_OVER_COOLDOWN = 2000

    #define fighter variables
    WARRIOR_SIZE = 162
    WARRIOR_SCALE = 4
    WARRIOR_OFFSET = [72, 56]
    WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
    WIZARD_SIZE = 250
    WIZARD_SCALE = 3
    WIZARD_OFFSET = [112, 107]
    WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

    #load music and sounds
    pygame.mixer.music.load("assets/audio/music.mp3")
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play(-1, 0.0, 5000)
    sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
    sword_fx.set_volume(0.5)
    magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
    magic_fx.set_volume(0.75)

    #load background image
    bg_image1 = pygame.image.load("assets/images/background/finalbg6.png").convert_alpha()
    bg_image2 = pygame.image.load("assets/images/background/finalbg2.png").convert_alpha()
    bg_image3 = pygame.image.load("assets/images/background/finalbg3.png").convert_alpha()
    bg_image4 = pygame.image.load("assets/images/background/finalbg4.png").convert_alpha()
    bg_image5 = pygame.image.load("assets/images/background/finalbg1.png").convert_alpha()

    ll = [bg_image1 , bg_image2 , bg_image3 , bg_image4 , bg_image5 ]
    x=0

    x+=1
    if x>4:
        x=0

    #load spritesheets
    warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
    wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

    #load vicory image
    victory_img = pygame.image.load("assets/images/icons/victoryfinalllllll-removebg-preview.png").convert_alpha()

    #define number of steps in each animation
    WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
    WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

    #define font
    count_font = pygame.font.Font("assets/images/FONTS/Halloween Morning.ttf", 80)
    score_font = pygame.font.Font("assets/images/FONTS/Halloween Morning.ttf", 30)

    #function for drawing text
    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    #function for drawing background
    def draw_bg():
        scaled_bg = pygame.transform.scale( ll[x], (SCREEN_WIDTH, SCREEN_HEIGHT) )
        screen.blit( scaled_bg, (0, 0) )
        

    #function for drawing fighter health bars
    def draw_health_bar(health, x, y):
        ratio = health / 100
        pygame.draw.rect(screen, WHITE, (x - 3, y - 3, 406, 36) , 3 , 24)
        #pygame.draw.rect(screen, RED, (x, y, 400, 30))
        pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 30 ,) , 0 , 23)

    #create two instances of fighters
    fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
    fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

   


    #game loop
    run = True
    while run:
        clock.tick(FPS)
        #draw background
        draw_bg()
        #show player stats
        draw_health_bar(fighter_1.health, 20, 20)
        draw_health_bar(fighter_2.health, 580, 20)
        draw_text("Player 1: " + str(score[0]), score_font, WHITE, 20, 60)
        draw_text("Player 2: " + str(score[1]), score_font, WHITE, 580, 60)

        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        PLAY_BACK = Button(image=None, pos=(900, 750), 
                            text_input="BACK", font=get_font(55), base_color="white", hovering_color="green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(screen)
        #update countdown
        if intro_count <= 0:
            #move fighters
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
        else:
            #display count timer
            draw_text(str(intro_count) , count_font, WHITE , SCREEN_WIDTH / 2 , SCREEN_HEIGHT / 3)
            #update count timer
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

        #update fighters
        fighter_1.update()
        fighter_2.update()

        #draw fighters
        fighter_1.draw(screen)
        fighter_2.draw(screen)

        #check for player defeat
        if round_over == False:
            if fighter_1.alive == False:
             score[1] += 1
             if sum(score)>2:
                main_menu()
             round_over = True
             round_over_time = pygame.time.get_ticks()
            elif fighter_2.alive == False:
             score[0] += 1
             if sum(score)>2:
                main_menu()
             round_over = True
             round_over_time = pygame.time.get_ticks()
        else:
            #display victory image
            screen.blit(victory_img, (200,0))
            # x+=1
            # if x>4 :
            #  x=0
            
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                round_over = False
                intro_count = 3
                fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
                fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

        
        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
             run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        #update display
        pygame.display.update()

def instructions():
    while True:
        INSTRUCTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("black")

        INSTRUCTIONS_TEXT = get_font(65).render("INSTRUCTIONS", True, "#b68f40")
        INSTRUCTIONS_RECT = INSTRUCTIONS_TEXT.get_rect(center=(500, 150))
        screen.blit(INSTRUCTIONS_TEXT, INSTRUCTIONS_RECT)

        CONTENT_TEXT = get_font(30).render("1.) This is a two player fighter game ,one fighter being WARRIOR and the other WIZARD.",True,"white")
        CONTENT_RECT=CONTENT_TEXT.get_rect(center=(500,250))
        screen.blit(CONTENT_TEXT,CONTENT_RECT)
        # player 1
        WARRIOR_TEXT = get_font(30).render("2.) The key controls for warrior are: a*left  d*right  w*jump  z*attack1  x*attack2   ",True,"white")
        WARRIOR_RECT=WARRIOR_TEXT.get_rect(center=(500,300))
        screen.blit(WARRIOR_TEXT,WARRIOR_RECT)
        #player 2
        WIZARD_TEXT = get_font2(30).render("3.)  The key controls for wizard are: 4*left  6*right  8*jump  1*attack1  2*attack2     ",True,"white")
        WIZARD_RECT=WIZARD_TEXT.get_rect(center=(500,350))
        screen.blit(WIZARD_TEXT,WIZARD_RECT)

        CONTENT_TEXT2 = get_font(30).render("4.) Each bout is of three rounds and the player with maximum points wins the bout.   ",True,"white")
        CONTENT_RECT2=CONTENT_TEXT2.get_rect(center=(500,400))
        screen.blit(CONTENT_TEXT2,CONTENT_RECT2)

        INSTRUCTIONS_BACK = Button(image=None, pos=(500, 550), 
                            text_input="BACK", font=get_font(65), base_color="#b68f40", hovering_color="white")

        INSTRUCTIONS_BACK.changeColor(INSTRUCTIONS_MOUSE_POS)
        INSTRUCTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if INSTRUCTIONS_BACK.checkForInput(INSTRUCTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        scaled_menu_bg = pygame.transform.scale( BG, (SCREEN_WIDTH, SCREEN_HEIGHT) )
        screen.blit(scaled_menu_bg, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(500, 200))

        PLAY_BUTTON = Button(image=None, pos=(500 , 375), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        INSTRUCTIONS_BUTTON = Button(image=None, pos=(500, 525), 
                            text_input="INSTRUCTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(500, 675), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON,INSTRUCTIONS_BUTTON,QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if INSTRUCTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    instructions()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                

        pygame.display.update()

main_menu()

