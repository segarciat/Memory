import typing
import pygame as pg

import src.services.image_loader as image_loader


class Card(pg.sprite.Sprite):
    """Sprite class that models a playing card from a 52-card deck."""
    TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN = '2', '3', '4', '5', '6', '7', '8', '9', '10'
    ACE, JACK, QUEEN, KING = 'A', 'J', 'Q', 'K'
    SPADES, HEARTS, DIAMONDS, CLUBS = "Spades", "Hearts", "Diamonds", "Clubs"

    BACK_CARD_IMAGE = 'cardBack_red1.png'

    def __init__(self, suit, value):
        """Creates a hard and defaults to having it face up.

        :param suit: The card's suit; only valid suits are Card.SPADES, Card.HEARTS, Card.DIAMONDS, and Card.CLUBS.
        :param value: The card's value; only valid ones are Card.TWO,... Card.TEN,
        Card.ACE, Card.JACK, Card.QUEEN, and Card.King.
        """
        pg.sprite.Sprite.__init__(self)
        self._suit = suit
        self._val = value
        self.image = image_loader.get_image(f"card{suit}{value}.png")
        self.rect = self.image.get_rect()
        self._face_up = True

    @property
    def suit(self) -> str:
        """Returns this card's suit, which is one of Card.SPADES,...,Card.CLUBS"""
        return self._suit

    @property
    def value(self) -> str:
        """Returns this card's value, which is one of Card.TWO,..., Card.TEN, Card.ACE,..., Card.KING"""
        return self._val

    @property
    def is_face_up(self) -> bool:
        return self._face_up

    def flip(self) -> None:
        """Negates the 'is_face_up' property of the card; note the image remains unchanged."""
        self._face_up = not self._face_up

    @classmethod
    def suits(cls) -> typing.Tuple[str, ...]:
        return cls.SPADES, cls.HEARTS, cls.DIAMONDS, cls.CLUBS

    @classmethod
    def values(cls) -> typing.Tuple[str, ...]:
        return cls.ACE, cls.TWO, cls.THREE, cls.FOUR, cls.FIVE, cls.SIX, \
               cls.SEVEN, cls.EIGHT, cls.NINE, cls.TEN, cls.JACK, cls.QUEEN, cls.KING

    @classmethod
    def back_card_image(cls) -> pg.Surface:
        return image_loader.get_image(cls.BACK_CARD_IMAGE)
