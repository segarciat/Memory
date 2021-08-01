import typing
import random
import pygame as pg

import src.services.image_loader as image_loader
from src.card import Card


class Deck(pg.sprite.Sprite):
    """Sprite that represents a 52-card deck."""
    def __init__(self):
        """Creates a Deck of 52 cards and shuffles them."""
        pg.sprite.Sprite.__init__(self)
        self._cards = [Card(suit, value) for suit in Card.suits() for value in Card.values()]
        self.image = image_loader.get_image('cardBack_red1.png')
        self.rect = self.image.get_rect()
        self.shuffle()

    def shuffle(self) -> None:
        """Shuffles the deck of cards."""
        random.shuffle(self._cards)

    def discard(self) -> typing.Union['Card', None]:
        """Returns a card if the deck is not empty; otherwise, returns None"""
        if self._cards:
            card = self._cards.pop()
            card.rect.topleft = self.rect.topright
            if len(self._cards) == 0:
                self.kill()
            return card
        return None  # None is returned by default... but just being explicit.
