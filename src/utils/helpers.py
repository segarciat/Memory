def is_hovering(sprite, mouse_x: int, mouse_y: int) -> bool:
    """Determines whether the mouse is hovering over the sprite."""
    if mouse_x < sprite.rect.left:
        return False
    if mouse_x > sprite.rect.right:
        return False
    if mouse_y < sprite.rect.top:
        return False
    if mouse_y > sprite.rect.bottom:
        return False
    return True