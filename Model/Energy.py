from pygame.sprite import Sprite
from pygame import Surface
from pygame import event, USEREVENT


class Energy(Sprite):
    def __init__(self, position, size, color, id_en, energy):
        Sprite.__init__(self)
        self.image = Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
        self.is_energy = True
        self.energy_take = USEREVENT + (2 + id_en)
        self.energy = energy
