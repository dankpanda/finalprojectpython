import pygame
import random

# This program assumes that you have all required assets on a file named 'cards' on your directory

pygame.init()

# Setting values
display_width = 800
display_height = 600
card1pos = (300,200)
card2pos = (400,200)
scorefont = pygame.font.SysFont(None, 30)
loseFont = pygame.font.SysFont(None,115)
losepos = (400,300)
scorepos = (665,550)
highscorepos = (665,575)
white = (255,255,255)
blue = (0,0,255)
bg_color = (34,177,76)
score_fill = (730,550,30,20)
highscore_fill = (770,575,30,20)

# Setting video game assets
win_sound = pygame.mixer.Sound("cards\\music\\winsound.flac")
lose_sound = pygame.mixer.Sound("cards\\music\\losesound.wav")
pygame.mixer.music.load("cards\\music\\bensound-dance.mp3")
blank_card_img = pygame.image.load('cards\\blank.png')
bg_img = pygame.image.load('cards\\bg.png')
continue_img = pygame.image.load('cards\\continue.png')
continue2_img = pygame.image.load('cards\\continue2.png')
win_img = pygame.image.load('cards\\win.png')
win2_img = pygame.image.load('cards\\win2.png')
retry_img = pygame.image.load('cards\\retry.png')
retry2_img = pygame.image.load('cards\\retry2.png')
music_credit_img = pygame.image.load('cards\\music_credit.png')

# Game window
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Higher Lower')
clock = pygame.time.Clock()
gameDisplay.blit(bg_img,(0,0))

# Game mechanics
class Higher_Lower():
    
    val_list = [2,3,4,5,6,7,8,9,10,11,12,13,14]
    icon_list = ['spades','clubs','hearts','diamonds']
    with open("cards\\highscore.txt",'r') as f:
        f_read = f.read()
    if f_read == '': # Avoid errors in the case where the highscore.txt file is empty
        f_read = 0
    highscore = int(f_read)
    
    def __init__(self):
        self.current_card = str(random.choice(self.val_list)) + "-" + random.choice(self.icon_list)
        self.next_card = str(random.choice(self.val_list)) + "-" + random.choice(self.icon_list)
        self.raw_value_current = int(self.current_card.split('-')[0])
        self.raw_value_next = int(self.next_card.split('-')[0])
        self.score = 0
        self.lost = False
        self.nextaction = False
    
    # This function checks the outcome when the user goes higher
    def higher(self):
        next_card_img = pygame.image.load('cards\\'+player.next_card+'.png')
        gameDisplay.blit(next_card_img,card2pos)
        if player.raw_value_current < player.raw_value_next or player.raw_value_current == player.raw_value_next:
            self.win()
        else:
            self.lose()
    
    # This function checks the outcome when the user goes lower
    def lower(self):
        next_card_img = pygame.image.load('cards\\'+player.next_card+'.png')
        gameDisplay.blit(next_card_img,card2pos)
        if player.raw_value_current > player.raw_value_next or player.raw_value_current == player.raw_value_next:
            self.win()
        else:
            self.lose()

    # This function will be called when the outcome of user's action is a win
    def win(self):
        pygame.mixer.Sound.play(win_sound)
        gameDisplay.blit(win_img,(255,305))
        self.score += 1
        self.current_card = self.next_card 
        self.next_card = str(random.choice(self.val_list)) + "-" + random.choice(self.icon_list)
        self.raw_value_current = int(self.current_card.split('-')[0])
        self.raw_value_next = int(self.next_card.split('-')[0])
        self.nextaction = True
        
    
    # This function will be called when the outcome of user's action is not a win
    def lose(self):
        pygame.mixer.Sound.play(lose_sound)
        gameDisplay.blit(retry_img,(255,305))
        with open("cards\\highscore.txt","w") as f: # Saves the new highscore 
            f.write(str(self.highscore))
        self.score = 0
        self.lost = True
    
    # This function will be called when the user loses and decides to play again
    def lost_shuffle(self):
        self.current_card = str(random.choice(self.val_list)) + "-" + random.choice(self.icon_list)
        self.next_card = str(random.choice(self.val_list)) + "-" + random.choice(self.icon_list)
        self.raw_value_current = int(self.current_card.split('-')[0])
        self.raw_value_next = int(self.next_card.split('-')[0])
        self.lost = False

    # Updates the current score
    def set_score(self,score):
        self.score = score

# Function to display text on the screen
def display_message(msg, font, color, pos):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, pos)

player = Higher_Lower()
current_card_img = pygame.image.load('cards\\'+player.current_card+'.png')
next_card_img = pygame.image.load('cards\\'+player.next_card+'.png')
    
# Main game loop
def gameloop():
    pygame.mixer.music.play(-1)
    player.set_score(player.score) # Refreshes the player's score live
    run = True

    while run:
        if player.score > player.highscore: # Updates the highscore live
            player.highscore = player.score
        gameDisplay.fill(bg_color,score_fill)
        gameDisplay.fill(bg_color,highscore_fill)
        display_message("Score: "+str(player.score),scorefont,white,scorepos)
        display_message("Highscore: "+str(player.highscore),scorefont,white,highscorepos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open("cards\\highscore.txt","w") as f: # Saves the new highscore 
                    f.write(str(player.highscore))
                run = False

        # Game flow if player have not lost
        if player.lost == False:
            if player.nextaction == False:
                current_card_img = pygame.image.load('cards\\'+player.current_card+'.png')
                gameDisplay.blit(music_credit_img,(5,0))
                gameDisplay.blit(continue2_img,(275,375))
                gameDisplay.blit(blank_card_img,card2pos)
                gameDisplay.blit(current_card_img,card1pos)
                gameDisplay.blit(win2_img,(255,305))
                gameDisplay.blit(retry2_img,(255,305))
                
                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_UP:
                        player.higher()
                    
                    elif event.key == pygame.K_DOWN:
                        player.lower()

            # This ensures the user does not accidentally choose an action twice and instead prompts for the input 'right' before proceeding
            elif player.nextaction  == True:
                gameDisplay.blit(continue_img,(275,375))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        player.nextaction = False
        
        # This block of code will run if the user loses
        else: 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    
                    player.lost_shuffle()           
        pygame.display.update()
        clock.tick(15)
gameloop()
pygame.quit()