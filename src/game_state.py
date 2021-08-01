"""
Art by Kenney: https://kenney.nl/
Card touch sound effect by Brian MacIntosh: https://opengameart.org/content/playing-card-sounds
Won! sound from: https://opengameart.org/content/won-orchestral-winning-jingle
Medieval loop sound from: https://opengameart.org/content/short-medieval-loop
"""
import abc
import sys
import time
import random
import math
import pygame as pg

import src.config as cfg
import src.input.input_manager as input_manager
import src.services.image_loader as image_loader
import src.services.sound as sound_manager
import src.utils.helpers as helpers
from src.input.input_state import InputState
from src.deck import Deck
from src.card import Card


class GameState(metaclass=abc.ABCMeta):
    """Abstract the state of the Game class."""
    def __init__(self, game):
        """Creates a GameState object.

        :param game: Game class whose behavior is driven by this class.
        """
        self._game = game

    @abc.abstractmethod
    def enter(self) -> None:
        """Performs any initial work to transition into this state."""
        pass

    def exit(self) -> None:
        """Performs any necessary clean-up before having the game transition to a new state."""
        pass

    @abc.abstractmethod
    def process_inputs(self) -> None:
        """Fetches any inputs in the queue since last frame and processes them."""
        pass

    @abc.abstractmethod
    def update(self) -> None:
        pass

    @abc.abstractmethod
    def draw(self, screen: pg.Surface) -> None:
        pass


class GameMainMenuState(GameState):
    """Represents the menu that a player sees upon opening the game."""
    def __init__(self, game):
        """Creates the main menu splash."""
        GameState.__init__(self, game)
        self._main_menu_splash = image_loader.get_image('main-menu-splash.png')

    def enter(self):
        """Creates the menu that lets a player begin playing or exit."""
        self._game.ui.clear()
        buttons = [
            {'action': self._select_difficulty, 'text': "Play", 'size': 16, 'color': cfg.WHITE},
            {'action': sys.exit, 'text': "Exit", 'size': 16, 'color': cfg.WHITE},
        ]
        self._game.ui.make_menu("Main Menu", 24, cfg.WHITE, buttons)

    def process_inputs(self):
        """Saves all inputs and allows the UI to process them."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
        input_manager.update_inputs()
        self._game.ui.process_inputs()

    def update(self) -> None:
        """Does nothing."""
        pass

    def draw(self, screen: pg.Surface) -> None:
        """Draws the main menu splash and the UI."""
        screen.blit(self._main_menu_splash, self._main_menu_splash.get_rect())
        self._game.ui.draw(screen)

    def _select_difficulty(self):
        """Creates a menu that allows a player to select the game's difficulty."""
        self._game.ui.clear()
        buttons = [
            {'action': lambda: self._play(difficulty=cfg.EASY), 'text': "Easy", 'size': 16, 'color': cfg.WHITE},
            {'action': lambda: self._play(difficulty=cfg.MEDIUM), 'text': "Medium", 'size': 16, 'color': cfg.WHITE},
            {'action': lambda: self._play(difficulty=cfg.HARD), 'text': "Hard", 'size': 16, 'color': cfg.WHITE},
            {'action': self.enter, 'text': "Main Menu", 'size': 16, 'color': cfg.WHITE},
        ]
        self._game.ui.make_menu("Select a Difficulty", 24, cfg.WHITE, buttons)

    def _play(self, difficulty):
        """Transitions the game to the playing state.

        :param difficulty: Determines the number of pairs the player has to guess.
        Can be cfg.EASY, cfg.MEDIUM, or cfg.HARD.
        :return: None
        """
        self._game.ui.clear()
        self._game.state = GamePlayingState(self._game, difficulty)


class GamePlayingState(GameState):
    """Represents the main gameplay behavior of the game."""
    def __init__(self, game, difficulty):
        """

        :param game: The top-level Game class for running the game.
        :param difficulty: The difficulty of the game for deciding the number of pairs the player must guess.
        """
        GameState.__init__(self, game)
        self._difficulty = difficulty
        self._all_cards = []
        self._guessed_pairs = []
        self._flipped_card = None
        self._paused = False
        self._back_card_image = None
        self._guesses = 0

    def enter(self):
        """Creates the pairs the player must guess in order to win."""
        self._game.ui.clear()
        self._pick_cards()
        self._scale_cards()
        self._paused = False
        self._guesses = 0
        sound_manager.play_sfx('shuffle.wav')
        sound_manager.play_music('medieval_loop.ogg', loops=-1)

    def exit(self):
        """Stops the main gameplay music."""
        sound_manager.stop_music()

    def process_inputs(self) -> None:
        """Allows the player to quit or pause the game, and the UI to process inputs directed at it."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            # todo: event for pausing and returning to main menu.
            if event.type == pg.KEYUP:
                if event.key == pg.K_p:
                    self._pause()
        input_manager.update_inputs()
        self._game.ui.process_inputs()

    def update(self):
        # See if game is over.
        if not self._paused and len(self._guessed_pairs) == len(self._all_cards):
            sound_manager.stop_music()
            sound_manager.play_sfx('Won!.wav')
            buttons = [
                {'action': self.enter, 'text': 'Restart', 'size': 16, 'color': cfg.WHITE},
                {'action': self._main_menu, 'text': 'Main Menu', 'size': 16, 'color': cfg.WHITE}
            ]
            self._game.ui.make_menu(f"Guesses: {self._guesses}", 24, cfg.WHITE, buttons)
            self._paused = True
        # Do not update if game is paused or mouse click has been processed elsewhere (such as by the UI).
        mouse_state = input_manager.mouse_state.get(InputState.MOUSE_LEFT)
        if self._paused or not mouse_state:
            return
        for card in self._all_cards:
            if helpers.is_hovering(card, *pg.mouse.get_pos()) and mouse_state == InputState.JUST_RELEASED:
                # If card has already been guessed, ignore.
                if card in self._guessed_pairs or card == self._flipped_card:
                    break
                card.flip()
                sound_manager.play_sfx('contact1.wav')
                # First card flipped.
                if self._flipped_card is None:
                    self._flipped_card = card
                # A match was found.
                elif self._flipped_card.value == card.value and self._flipped_card.suit == card.suit:
                    self._guessed_pairs.append(self._flipped_card)
                    self._guessed_pairs.append(card)
                    self._flipped_card = None
                    self._guesses += 1
                # Second card was not a match.
                else:
                    # Show the card we just flipped for 2 seconds.
                    self._game.screen.blit(card.image, card.rect)
                    pg.display.flip()
                    time.sleep(1.5)
                    # Flip both cards back down.
                    self._flipped_card.flip()
                    card.flip()
                    self._flipped_card = None
                    self._guesses += 1
                break

    def draw(self, screen: pg.Surface) -> None:
        """Draws all cards and the UI."""
        # Draw everything.
        if not self._paused:
            screen.fill(cfg.WHITE)
            for card in self._all_cards:
                if card.is_face_up:
                    screen.blit(self._back_card_image, card.rect)
                else:
                    screen.blit(card.image, card.rect)
        self._game.ui.draw(screen)

    def _pick_cards(self):
        """Picks a set cards from a deck to determine the pairs the player must guess to win."""
        self._all_cards = []
        self._guessed_pairs = []
        self._flipped_card = None
        deck = Deck()
        pairs_count = cfg.PAIRS_BY_DIFFICULTY[self._difficulty]
        # Select pairs
        for i in range(pairs_count):
            # Choose a card.
            card = deck.discard()
            # Copy each card for the memory game.
            self._all_cards.append(card)
            self._all_cards.append(Card(card.suit, card.value))

        # Shuffle all cards.
        random.shuffle(self._all_cards)

    def _scale_cards(self):
        """Resizes the cards based on the number of cards chosen to allow an equal number of rows and columns."""
        # Scale card images.
        row_cards_count = math.sqrt(len(self._all_cards))
        # Scale vertically so that cards are against screen boundaries.
        card_height = int(cfg.SCREEN_HEIGHT // row_cards_count)
        # Scale horizontally by the same by maintaining aspect ratio.
        card_width = int(self._all_cards[0].rect.width * (card_height / self._all_cards[0].rect.height))

        # Scale the back card image.
        # TODO: scaling the Card class back card image directly? doesn't seem right.
        self._back_card_image = pg.transform.scale(Card.back_card_image(), (card_width, card_height))

        row_padding = (cfg.SCREEN_WIDTH - row_cards_count * card_width) / 2
        # Scale the cards picked from the deck.
        for i, card in enumerate(self._all_cards):
            card.image = pg.transform.scale(card.image, (card_width, card_height))
            card.rect = card.image.get_rect()
            row = int(i / row_cards_count)
            col = int(i % row_cards_count)
            card.rect.topleft = (row_padding + col * card_width, row * card_height)

    def _pause(self):
        """Pauses the game, giving a player options such as restarting, exiting, or continuing to play."""
        if self._paused:
            self._game.ui.pop_menu()
        else:
            buttons = [
                {'action': self._pause, 'text': 'Resume', 'size': 16, 'color': cfg.WHITE},
                {'action': self.enter, 'text': 'Restart', 'size': 16, 'color': cfg.WHITE},
                {'action': self._main_menu, 'text': 'Main Menu', 'size': 16, 'color': cfg.WHITE}
            ]
            self._game.ui.make_menu("Game Paused", 24, cfg.WHITE, buttons)
        self._paused = not self._paused

    def _main_menu(self):
        """Sets the state of the Game class driven by this class to the main menu state."""
        self._game.state = self._game.main_menu_state
