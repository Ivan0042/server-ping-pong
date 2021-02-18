from pygame.math import Vector2
from Model.Enemy import GameObject


class Ball(GameObject):
    def __init__(self, start_position, size, color, speed, min_speed, max_speed, direction):
        super().__init__(start_position, size, color, speed, min_speed, max_speed, direction)
        self.direction = self.direction.normalize()

    def reflect(self, new_dir):
        self.direction = self.direction.reflect(Vector2(new_dir))

    def move(self):
        self.position += self.direction.normalize() * self.speed
        self.rect.center = round(self.position.x), round(self.position.y)

    def set_speed(self, speed):
        if self.speed + speed >= self.max_speed:
            self.speed = self.max_speed
        elif self.speed + speed <= self.min_speed:
            self.speed = self.min_speed
        else:
            self.speed += speed
