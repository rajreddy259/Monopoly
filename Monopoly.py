import pygame
from pygame.locals import *
import random
from collections import deque
from pygame.sprite import Group
import pyperclip

# initilze PyGame library
pygame.init()

# set up game window
clock = pygame.time.Clock()
fps = 60
screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Monopoly')

#define font
font = pygame.font.SysFont('Bauhaus 93', 30)
smaller_font = pygame.font.SysFont('Bauhaus 93', 20)
semi_font = pygame.font.SysFont('Bauhaus 93', 25)

#define colors
white = (255, 255, 255)

# load images
bg = pygame.image.load('assets/black.jpg')
player_img = pygame.image.load('assets/car.png')
dice_img = pygame.image.load('assets/dice.png')

# reduce the size of the images
scaled_player_img = pygame.transform.scale(player_img, (player_img.get_width() // 2, player_img.get_height() // 2))
scaled_dice_img = pygame.transform.scale(dice_img, (dice_img.get_width() // 2, dice_img.get_height() // 2))

# set game variables
position = 0
moves = 0
landing = []
get_out_of_jail_cards = 0
in_jail = False

# using a queue to for the Community Chest and chance cards
# will help with removing and reseting the cards
community_chest_card = ""
chance_card = ""
community_chest_card_text = "Community Chest Card:\n" + community_chest_card
community_chest_cards = [
    "Advance to Go (Collect $200)",
    "Bank error in your favor. Collect $200",
    "Doctor’s fee. Pay $50",
    "From sale of stock you get $50",
    "Get Out of Jail Free",
    "Go to Jail. Go directly to jail, do not pass Go, do not collect $200",
    "Holiday fund matures. Receive $100",
    "Income tax refund. Collect $20",
    "It is your birthday. Collect $10 from every player",
    "Life insurance matures. Collect $100",
    "Pay hospital fees of $100",
    "Pay school fees of $50",
    "Receive $25 consultancy fee",
    "You are assessed for street repair. $40 per house. $115 per hotel",
    "You have won second prize in a beauty contest. Collect $10",
    "You inherit $100"
]

cc_queue = deque(community_chest_cards)

chance_cards = [
    "Advance to Boardwalk",
    "Advance to Go (Collect $200)",
    "Advance to Illinois Avenue. If you pass Go, collect $200",
    "Advance to St. Charles Place. If you pass Go, collect $200",
    "Advance to the nearest Railroad. If unowned, you may buy it from the Bank. If owned, pay wonder twice the rental to which they are otherwise entitled",
    "Advance to the nearest Railroad. If unowned, you may buy it from the Bank. If owned, pay wonder twice the rental to which they are otherwise entitled",
    "Advance token to nearest Utility. If unowned, you may buy it from the Bank. If owned, throw dice and pay owner a total ten times amount thrown.",
    "Bank pays you dividend of $50",
    "Get Out of Jail Free",
    "Go Back 3 Spaces",
    "Go to Jail. Go directly to Jail, do not pass Go, do not collect $200",
    "Make general repairs on all your property. For each house pay $25. For each hotel pay $100",
    "Speeding fine $15",
    "Take a trip to Reading Railroad. If you pass Go, collect $200",
    "You have been elected Chairman of the Board. Pay each player $50",
    "Your building loan matures. Collect $150"
]

chance_queue = deque(chance_cards)

# hashmap of locations with the location being the key and the value beign the number of times visited
locations = {}
locations["GO"] = 0
locations["Baltic Avenue"] = 0
locations["Community Chest #1"] = 0
locations["Mediterranean Avenue"] = 0
locations["Income Tax"] = 0
locations["Reading Railroad"] = 0
locations["Oriental Avenue"] = 0
locations["Chance #1"] = 0
locations["Vermont Ave"] = 0
locations["Connecticut Avenue"] = 0
locations["In Jail/Just Visiting"] = 0
locations["St.Charles Place"] = 0
locations["Electric Company"] = 0
locations["States Avenue"] = 0
locations["Virginia Avenue"] = 0
locations["Pennsylvania Railroad"] = 0
locations["St.James Place"] = 0
locations["Community Chest #2"] = 0
locations["Tennessee Avenue"] = 0
locations["New York Avenue"] = 0
locations["Free Parking"] = 0
locations["Kentucky Avenue"] = 0
locations["Chance #2"] = 0
locations["Indiana Avenue"] = 0
locations["Illinois Avenue"] = 0
locations["B&O Railroad"] = 0
locations["Atlantic Avenue"] = 0
locations["Ventnor Avenue"] = 0
locations["Water Works"] = 0
locations["Marvin Gardens"] = 0
locations["Go To Jail!"] = 0
locations["Pacific Avenue"] = 0
locations["North Carolina Avenue"] = 0
locations["Community Chest #3"] = 0
locations["Pennsylvania Avenue"] = 0
locations["Short Line"] = 0
locations["Chance #3"] = 0
locations["Park Place"] = 0
locations["Luxury Tax"] = 0
locations["Boardwalk"] = 0

space_counts = {space: 0 for space in locations.keys()}


# a player class to set the single player
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = scaled_player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.position = 0
        self.moves = 0
        self.get_out_of_jail_cards = 0
        self.turns = 0

# create a Player object
player = Player(432, 936 - 48)

# function to draw the player on the screen
def draw_player():
    screen.blit(player.image, player.rect)


# Function to draw buttons on the screen
def draw_buttons():
    # dice button
    roll_dice = pygame.draw.rect(screen, white, (50, 800, 100, 40))  # Width: 100, Height: 40
    draw_text("Roll Dice", font, (0, 0, 0), screen, roll_dice.centerx-40, roll_dice.centery-15)

    # Community Chest button
    cc_button = pygame.draw.rect(screen, white, (200, 800, 130, 40))  # Width: 130, Height: 40
    draw_text("C Chest", font, (0, 0, 0), screen, cc_button.centerx-55, cc_button.centery-15)

    # Chance button
    chance_button = pygame.draw.rect(screen, white, (600, 800, 100, 40))  # Width: 100, Height: 40
    draw_text("Chance", font, (0, 0, 0), screen, chance_button.centerx-35, chance_button.centery-15)

# draw text method to render text on a blank screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# this function will place a gray box around the spaces and landings, which will copy the data onto the clipboard
def draw_copy_area():
    copy_area = pygame.draw.rect(screen, (100, 100, 100), (350, 50, 300, 600))  # Adjust the dimensions as needed
    return copy_area

# function to draw text on the screen for the locations as they are a smaller size
def draw_text(text, font, color, surface, x, y):
    lines = text.split('\n')
    line_height = font.size("")[1]  # get the height of a single line of text
    for i, line in enumerate(lines):
        text_obj = font.render(line, True, color)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (x, y + i * line_height)  # adjust vertical spacing using line_height
        surface.blit(text_obj, text_rect)


# Main game loop
running = True
die1 = 0
die2 = 0
turns_in_jail = 0

copy_area_rect = pygame.Rect(350, 50, 300, 800)

for _ in range(1000):
    # Reset player position and moves for each iteration
    player.position = 0
    player.moves = 0
    player.turns = 0
    in_jail = False
    turns_in_jail = 0
    while running:
        screen.fill((0, 0, 0))
        copy_area_rect = draw_copy_area()
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                if copy_area_rect.collidepoint(event.pos):
                            # will copy the spaces and landings text to the clipboard
                            space_counts_text = "\n".join([f" {count}" for space, count in space_counts.items()])
                            pyperclip.copy(space_counts_text)
                if 50 <= event.pos[0] <= 200 and 800 <= event.pos[1] <= 850:
                    # while player.turns < 10000: # loop to test n turns, uncomment this to test different n values

                        die1 = random.randint(1, 6)
                        die2 = random.randint(1, 6)
                        total_moves = die1 + die2

                        # update player position and handle board wrap-around
                        player.position = (player.position + total_moves) % len(locations)

                        # increment the number of moves
                        player.moves += total_moves
                        
                        # increment the number of turns
                        player.turns += 1
                        
                        #location on the board and will increment the value
                        current_space = list(locations.keys())[player.position]
                        space_counts[current_space] += 1

                        # handle landing on Community Chest and Chance spaces
                        current_space = list(locations.keys())[player.position]
                        if "Community Chest" in current_space:
                            # draw a Community Chest card and process it
                            card = cc_queue.popleft()
                            cc_queue.append(card)  # Put the card back to the bottom of the deck
                            print(f"Community Chest Card: {card}")
                            if "Go to Jail" in card:
                                if get_out_of_jail_cards > 1:
                                 get_out_of_jail_cards -= 1
                                 in_jail = False
                            else:
                                in_jail = False
                                ''' The code below is for strategy B'''
                                # in_jail = True
                                # current_space = "In Jail/Just Visiting"
                                # space_counts[current_space] += 1
                                # die1 = random.randint(1, 6)
                                # die2 = random.randint(1, 6)
                                # if die1 == die2:
                                #     # If doubles are rolled, get out of jail
                                #     in_jail = False
                                #     turns_in_jail = 0
                                # else:
                                #     turns_in_jail += 1

                                # if turns_in_jail >= 3:
                                #     # After three turns, assume the player pays the $50 fine and gets out of jail
                                #     in_jail = False
                                #     turns_in_jail = 0
                                # if get_out_of_jail_cards > 0:
                                #     # use the "Get Out of Jail Free" card to avoid staying in jail
                                #     get_out_of_jail_cards -= 1
                                #     in_jail = False
                                
                                
                                
                        elif "Chance" in current_space:
                            # draw a Chance card and process it
                            card = chance_queue.popleft()
                            chance_queue.append(card)  # put the card back to the bottom of the deck
                            print(f"Chance Card: {card}")
                            if "Go to Jail" in card:
                                if get_out_of_jail_cards > 1:
                                 get_out_of_jail_cards -= 1
                                 in_jail = False
                            else:
                                in_jail = False
                                '''The code below is for strategy B'''
                                # in_jail = True
                                # current_space = "In Jail/Just Visiting"
                                # space_counts[current_space] += 1
                                # die1 = random.randint(1, 6)
                                # die2 = random.randint(1, 6)
                                # if die1 == die2:
                                #     # If doubles are rolled, get out of jail
                                #     in_jail = False
                                #     turns_in_jail = 0
                                # else:
                                #     turns_in_jail += 1

                                # if turns_in_jail >= 3:
                                #     # After three turns, assume the player pays the $50 fine and gets out of jail
                                #     in_jail = False
                                #     turns_in_jail = 0
                                # if get_out_of_jail_cards > 0:
                                #     # use the "Get Out of Jail Free" card to avoid staying in jail
                                #     get_out_of_jail_cards -= 1
                                #     in_jail = False
                                

                        elif "Go To Jail!" in current_space:
                            if get_out_of_jail_cards > 1:
                                 get_out_of_jail_cards -= 1
                                 in_jail = False
                            else:
                                 in_jail = False
                            
                            '''The code below is for strategy B'''
                            # in_jail = True
                            # current_space = "In Jail/Just Visiting"
                            # space_counts[current_space] += 1
                            # die1 = random.randint(1, 6)
                            # die2 = random.randint(1, 6)
                            # if die1 == die2:
                            #     # If doubles are rolled, get out of jail
                            #     in_jail = False
                            #     turns_in_jail = 0
                            # else:
                            #     turns_in_jail += 1

                            # if turns_in_jail >= 3:
                            #     # After three turns, assume the player pays the $50 fine and gets out of jail
                            #     in_jail = False
                            #     turns_in_jail = 0
                            # if get_out_of_jail_cards > 0:
                            #     # use the "Get Out of Jail Free" card to avoid staying in jail
                            #     get_out_of_jail_cards -= 1
                            #     in_jail = False
                            
                        elif die1 == die2: #if doubles are rolled, go to position and reroll
                            total_moves = die1 + die2
                            player.position = (player.position + total_moves) % len(locations)
                            player.moves += total_moves
                            current_space = list(locations.keys())[player.position]
                            space_counts[current_space] += 1
                           
                                 
                            
                elif 250 <= event.pos[0] <= 450 and 800 <= event.pos[1] <= 850:
                    # if not in_jail: 
                        # Draw a Community Chest card and process it
                        community_chest_card = cc_queue.popleft()
                        cc_queue.append(community_chest_card)  # Put the card back to the bottom of the deck
                        print(f"Community Chest Card: {community_chest_card}")
                        if "Go to Jail" in community_chest_card:
                            if get_out_of_jail_cards > 1:
                                 get_out_of_jail_cards -= 1
                                 in_jail = False
                            else:
                                in_jail = False
                            
                            ''' The code below is for strategy B'''
                            # in_jail = True
                            # current_space = "In Jail/Just Visiting"
                            # space_counts[current_space] += 1
                            # die1 = random.randint(1, 6)
                            # die2 = random.randint(1, 6)
                            # if die1 == die2:
                            #     # If doubles are rolled, get out of jail
                            #     in_jail = False
                            #     turns_in_jail = 0
                            # else:
                            #     turns_in_jail += 1

                            # if turns_in_jail >= 3:
                            #     # After three turns, assume the player pays the $50 fine and gets out of jail
                            #     in_jail = False
                            #     turns_in_jail = 0
                            # if get_out_of_jail_cards > 0:
                            #     # use the "Get Out of Jail Free" card to avoid staying in jail
                            #     get_out_of_jail_cards -= 1
                            #     in_jail = False
                            
                        if "Get Out of Jail Free" in community_chest_card:
                            get_out_of_jail_cards = True

                elif 500 <= event.pos[0] <= 650 and 800 <= event.pos[1] <= 850:
                    # if not in_jail:  
                        # draw a Chance card and process it
                        chance_card = chance_queue.popleft()
                        chance_queue.append(chance_card)  # Put the card back to the bottom of the deck
                        print(f"Chance Card: {chance_card}")
                        if "Go to Jail" in chance_card:
                            if get_out_of_jail_cards > 1:
                                 get_out_of_jail_cards -= 1
                                 in_jail = False
                            else:
                                in_jail = False
                            
                            ''' The code below is for strategy B'''
                            # in_jail = True
                            # current_space = "In Jail/Just Visiting"
                            # space_counts[current_space] += 1
                            # die1 = random.randint(1, 6)
                            # die2 = random.randint(1, 6)
                            # if die1 == die2:
                            #     # If doubles are rolled, get out of jail
                            #     in_jail = False
                            #     turns_in_jail = 0
                            # else:
                            #     turns_in_jail += 1

                            # if turns_in_jail >= 3:
                            #     # After three turns, assume the player pays the $50 fine and gets out of jail
                            #     in_jail = False
                            #     turns_in_jail = 0
                            # if get_out_of_jail_cards > 0:
                            #     # use the "Get Out of Jail Free" card to avoid staying in jail
                            #     get_out_of_jail_cards -= 1
                            #     in_jail = False
                            
                        if "Get Out of Jail Free" in chance_card:
                            get_out_of_jail_cards = True

                elif 700 <= event.pos[0] <= 800 and 800 <= event.pos[1] <= 850:
                    in_jail = not in_jail
                
                

        # draw buttons on the screen
        draw_buttons()

        # draw text on the screen for locations, variables, and buttons
        draw_text("Position: " + list(locations.keys())[player.position], font, white, screen, 10, 50)
        draw_text("Dice: " + str(die1 + die2), font, white, screen, 10, 150)
        draw_text("Moves: " + str(player.moves), font, white, screen, 10, 250)
        draw_text("Turns: " + str(player.turns), font, white, screen, 10, 300)
        draw_text("In Jail: " + ("Yes" if in_jail else "No"), font, white, screen, 10, 350)
        draw_text("Community Chest Card: ", font, white, screen, 10, 450)
        draw_text(community_chest_card, smaller_font, white, screen, 10, 475)
        draw_text("Chance Card: ", font, white, screen, 10, 550)
        draw_text(chance_card, smaller_font, white, screen, 10, 575)
        draw_text("Get Out of Jail Free Cards: " + ("Yes" if get_out_of_jail_cards else "No"), font, white, screen, 10, 650)
        draw_text("Spaces and Landings:", smaller_font, white, screen, 350, 50)
        space_counts_text = "\n".join([f"{space}: {count}" for space, count in space_counts.items()])
        draw_text(space_counts_text, smaller_font, white, screen, 350, 100)

        pygame.display.update()
        clock.tick(fps)

pygame.quit()