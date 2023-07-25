import pygame
from pygame.locals import *
import random
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
font = pygame.font.SysFont('Bauhaus 93', 60)

#define colors
white = (255, 255, 255)

#load images
bg = pygame.image.load('assets/monopoly.png')
player_img = pygame.image.load('assets/car.png')
dice_img = pygame.image.load('assets/dice.png')

# set game variables
position = 0
moves = 0
landing = []
get_out_of_jail_cards = 0
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

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
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

# Main game loop
running = True
while running:
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Roll the dice and move the player
    if pygame.key.get_pressed()[K_SPACE]:
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        total_moves = die1 + die2

        # Update player position and handle board wrap-around
        player.position = (player.position + total_moves) % len(spaces)

        # Increment the number of moves
        player.moves += 1

        # Handle landing on Community Chest and Chance spaces
        current_space = spaces[player.position]
        if current_space == "Community Chest":
            # Draw a Community Chest card and process it
            card = cc_queue.popleft()
            cc_queue.append(card)  # Put the card back to the bottom of the deck
            print(f"Community Chest Card: {card}")
            # Add your code to process the Community Chest card here

        elif current_space == "Chance":
            # Draw a Chance card and process it
            card = chance_queue.popleft()
            chance_queue.append(card)  # Put the card back to the bottom of the deck
            print(f"Chance Card: {card}")
            # Add your code to process the Chance card here

    # Draw the player on the screen
    draw_player()

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
