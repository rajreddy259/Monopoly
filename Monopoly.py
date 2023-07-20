import pygame
from pygame.locals import *
import random

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


#intialize Player class
class Player (pygame.sprite.Sprite):
    def __init__(self, x,  y):
        pygame.sprite.Sprite.__init__(self)
        self.position = 0
        self.moves = 0;
        self.get_out_of_jail_cards = 0
