from pygame.sprite import Sprite
from pygame import Surface


class Border(Sprite):
    def __init__(self, position, size, color):
        Sprite.__init__(self)
        self.image = Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
