"""Game configuration file specifying game constants and resource locations."""
import os


# Screen Settings.
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 1024
TITLE = "Memory"
FPS = 30

# Game directory and game assets directories.
GAME_DIR = os.path.dirname(__file__)
IMG_DIR = os.path.join(GAME_DIR, 'assets', 'images')
SND_DIR = os.path.join(GAME_DIR, 'assets', 'sound')

# Color RGBs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
TRANSPARENT = (255, 255, 255, 0)
COLOR_KEY = BLACK


# Sprite sheets.
SPRITE_SHEETS = (
    {"img": "playingCards.png", "xml": "playingCards.xml"},  # Game Object images.
    {"img": "playingCardBacks.png", "xml": "playingCardBacks.xml"},
    {"img": "blueSheet.png", "xml": "blueSheet.xml"}
)
CARD_HEIGHT = 140
CARD_WIDTH = 190

# Game font names.
FONT_NAMES = ('arial', 'calibri')
EASY = "EASY"
MEDIUM = "MEDIUM"
HARD = "HARD"
# Difficulty -> Number of Pairs (note that, when doubled, you get a perfect square).
PAIRS_BY_DIFFICULTY = {EASY: 8, MEDIUM: 18, HARD: 32}
