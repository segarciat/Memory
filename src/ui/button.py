import typing
import pygame as pg

import src.services.text as text_renderer
import src.input.input_manager as input_manager
import src.utils.helpers as helpers
from src.input.input_state import InputState
from src.animated_sprite import AnimatedSprite


class Button(AnimatedSprite):
    """Represents a button sprite that, upon click, runs some action."""
    _HOVER_OFF, _HOVER_ON, _CLICKED = 0, 1, 2

    def __init__(self, action: typing.Callable, text: str, size: int, color, img_files: typing.List[str], all_groups):
        """Renders text onto the button and assigns the action.

        :param action: Function to run when button is clicked.
        :param text: Text to be rendered on the button.
        :param size: Size of the font for the text to be rendered.
        :param color: Color for the text to be rendered.
        :param img_files: List of filenames of the button's images.
        :param all_groups: Dictionary of sprite groups.
        """
        frame_info = [
            {'start_frame': Button._HOVER_OFF, 'num_frames': 1},
            {'start_frame': Button._HOVER_ON, 'num_frames': 1},
            {'start_frame': Button._CLICKED, 'num_frames': 1}
        ]
        AnimatedSprite.__init__(self, img_files, frame_info, all_groups)
        # Add Text to buttons.
        for i in range(len(self._images)):
            # Make a copy to safely alter image with text.
            self._images[i] = self._images[i].copy()
            text_renderer.render(self._images[i], text, size, color)
        # on-click button function
        self._action = action

    def handle_mouse(self):
        """Either animates the button or executes the function that it encapsulates."""
        # Keep track of bottom of button.
        old_bot = self.rect.bottomleft
        mouse_x, mouse_y = pg.mouse.get_pos()

        # See if a mouse click was registered and has not been processed.
        mouse_state = input_manager.mouse_state.get(InputState.MOUSE_LEFT, None)
        if mouse_state and helpers.is_hovering(self, mouse_x, mouse_y):
            self.change_anim(Button._HOVER_ON)
            if mouse_state == InputState.STILL_PRESSED:
                self.change_anim(Button._CLICKED)
            elif mouse_state == InputState.JUST_RELEASED:
                # toggle-off clicked animation
                self._action()
            # Process mouse click.
            del input_manager.mouse_state[InputState.MOUSE_LEFT]
        else:
            self.change_anim(Button._HOVER_OFF)
        # Update button position
        self.rect = self.image.get_rect()
        self.rect.bottomleft = old_bot
