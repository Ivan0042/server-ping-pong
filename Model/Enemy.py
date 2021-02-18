from pygame.sprite import Sprite
from pygame import Surface
from pygame.math import Vector2


class GameObject(Sprite):
    def __init__(self, start_point, size, color, speed, min_speed, max_speed, direction):
        Sprite.__init__(self)

        self.image = Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.position = Vector2(start_point)
        self.direction = Vector2(direction)

        self.rect.centerx, self.rect.centery = self.position.x, self.position.y

    def move(self):
        pass

    def set_speed(self, speed):
        pass
