from pygame.sprite import Sprite
from pygame import USEREVENT
from pygame import K_UP, K_DOWN, transform
from pygame.math import Vector2
from Model.Enemy import GameObject


class Paddle(GameObject):
    def __init__(self, start_point, size, color, speed,  min_speed, max_speed, id_paddle, vector):
        super().__init__(start_point, size, color, speed, min_speed, max_speed, (0, 0))
        self.is_ball_direction = Vector2(vector)
        self.energy = 33
        self.is_power_hit = False
        self.power_hit = USEREVENT + id_paddle

    def move(self):
        self.position += (self.direction * self.speed)
        self.rect.center = round(self.position.x), round(self.position.y)

    def reflect(self, new_dir):
        self.direction = self.direction.reflect(Vector2(new_dir))
        self.move()

    def set_speed(self, speed):
        self.speed = speed

    def set_energy(self, en):
        if self.energy + en > 100:
            self.energy = 100
        elif self.energy + en <= 0:
            self.energy = 0
        else:
            self.energy += en

    def run(self, key):
        if key == "True" and self.energy > 0:
            self.speed = self.max_speed
            self.energy -= 0.5
        else:
            self.speed = 4

    def punch(self):
        if self.energy // 20 > 0:
            self.set_energy(-20)
            if self.is_power_hit:
                return 20
        return 0

