import pygame
from pygame.locals import *
import random
import pyautogui
import time

from collections import deque

from pygame.sprite import Group

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

# Reduce the size of the images
scaled_player_img = pygame.transform.scale(player_img, (player_img.get_width() // 2, player_img.get_height() // 2))
scaled_dice_img = pygame.transform.scale(dice_img, (dice_img.get_width() // 2, dice_img.get_height() // 2))



# set game variables
position = 0
moves = 0
landing = []
get_out_of_jail_cards = 0
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

# hashmap of locations
locations = {}
locations["GO"] = 0
locations["Mediterranean Avenue"] = 0
locations["Community Chest #1"] = 0
locations["Baltic Avenue"] = 0
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
locations["Chance"] = 0
locations["Park Place"] = 0
locations["Luxury Tax"] = 0
locations["Boardwalk"] = 0

space_counts = {space: 0 for space in locations.keys()}


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))



class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = scaled_player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.position = 0
        self.moves = 0
        self.get_out_of_jail_cards = 0

# Create a Player object
player = Player(432, 936 - 48)

# Function to draw the player on the screen
def draw_player():
    screen.blit(player.image, player.rect)


in_jail = False
# Function to draw buttons on the screen
def draw_buttons():
    # Draw Dice button
    dice_button_rect = pygame.draw.rect(screen, white, (50, 800, 100, 40))  # Width: 100, Height: 40
    draw_text("Roll Dice", font, (0, 0, 0), screen, dice_button_rect.centerx-40, dice_button_rect.centery-15)

    # Draw Community Chest button
    cc_button_rect = pygame.draw.rect(screen, white, (200, 800, 130, 40))  # Width: 130, Height: 40
    draw_text("C Chest", font, (0, 0, 0), screen, cc_button_rect.centerx-55, cc_button_rect.centery-15)

    # Draw Chance button
    chance_button_rect = pygame.draw.rect(screen, white, (600, 800, 100, 40))  # Width: 100, Height: 40
    draw_text("Chance", font, (0, 0, 0), screen, chance_button_rect.centerx-35, chance_button_rect.centery-15)



# Function to draw text on the screen
def draw_text(text, font, color, surface, x, y):
    lines = text.split('\n')
    line_height = font.size("")[1]  # Get the height of a single line of text
    for i, line in enumerate(lines):
        text_obj = font.render(line, True, color)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (x, y + i * line_height)  # Adjust vertical spacing using line_height
        surface.blit(text_obj, text_rect)


def simulate_roll():
    global die1, die2, space_counts

    # Roll the dice and move the player
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    total_moves = die1 + die2

    # Update player position and handle board wrap-around
    player.position = (player.position + total_moves) % len(locations)

    # Increment the number of moves
    player.moves += total_moves

    # Update space counts
    current_space = list(locations.keys())[player.position]
    space_counts[current_space] += 1

# Main game loop
running = True
die1 = 0
die2 = 0

for _ in range(1000):
    # Reset player position and moves for each iteration
    player.position = 0
    player.moves = 0
    in_jail = False
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                
                if 50 <= event.pos[0] <= 200 and 800 <= event.pos[1] <= 850:
                    # if not in_jail:  # Only roll the dice if the player is not in jail

                        die1 = random.randint(1, 6)
                        die2 = random.randint(1, 6)
                        total_moves = die1 + die2

                        # Update player position and handle board wrap-around
                        player.position = (player.position + total_moves) % len(locations)

                        # Increment the number of moves
                        player.moves += 1

                        current_space = list(locations.keys())[player.position]
                        space_counts[current_space] += 1

                        # Handle landing on Community Chest and Chance spaces
                        current_space = list(locations.keys())[player.position]
                        if "Community Chest" in current_space:
                            # Draw a Community Chest card and process it
                            card = cc_queue.popleft()
                            cc_queue.append(card)  # Put the card back to the bottom of the deck
                            print(f"Community Chest Card: {card}")
                            # Add your code to process the Community Chest card here
                            if "Go to Jail" in card:
                                in_jail = True

                        elif "Chance" in current_space:
                            # Draw a Chance card and process it
                            card = chance_queue.popleft()
                            chance_queue.append(card)  # Put the card back to the bottom of the deck
                            print(f"Chance Card: {card}")
                            # Add your code to process the Chance card here
                            if "Go to Jail" in card:
                                in_jail = True

                elif 250 <= event.pos[0] <= 450 and 800 <= event.pos[1] <= 850:
                    # if not in_jail:  # Only draw Community Chest card if not in jail
                        # Draw a Community Chest card and process it
                        community_chest_card = cc_queue.popleft()
                        cc_queue.append(community_chest_card)  # Put the card back to the bottom of the deck
                        print(f"Community Chest Card: {community_chest_card}")
                        # Add your code to process the Community Chest card here
                        if "Go to Jail" in community_chest_card:
                            in_jail = True
                            get_out_of_jail_cards = False
                        if "Get Out of Jail Free" in community_chest_card:
                            get_out_of_jail_cards = True

                elif 500 <= event.pos[0] <= 650 and 800 <= event.pos[1] <= 850:
                    # if not in_jail:  # Only draw Chance card if not in jail
                        # Draw a Chance card and process it
                        chance_card = chance_queue.popleft()
                        chance_queue.append(chance_card)  # Put the card back to the bottom of the deck
                        print(f"Chance Card: {chance_card}")
                        # Add your code to process the Chance card here
                        if "Go to Jail" in chance_card:
                            in_jail = True
                            get_out_of_jail_cards = False
                        if "Get Out of Jail Free" in chance_card:
                            get_out_of_jail_cards = True

                elif 700 <= event.pos[0] <= 800 and 800 <= event.pos[1] <= 850:
                    # Toggle In Jail text (Simple Yes/No)
                    in_jail = not in_jail

        # Draw buttons on the screen
        draw_buttons()

        # Draw text on the screen
        draw_text("Position: " + list(locations.keys())[player.position], font, white, screen, 10, 50)
        draw_text("Dice: " + str(die1 + die2), font, white, screen, 10, 150)
        draw_text("Moves: " + str(player.moves), font, white, screen, 10, 250)
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