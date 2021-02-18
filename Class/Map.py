from pygame.sprite import RenderPlain
from pygame import Surface, sprite, Rect
from Model.Border import Border
from Model.Energy import Energy
from Class.Config import Config


class Map:
    def __init__(self, color_border, color_energy):
        self.__color_border = color_border
        self.__borders = []
        self.__borders_render = []

        self.__color_energy = color_energy
        self.__energys = []
        self.__energys_render = []

        self.create_border()
        self.create_energy()

    def create_border(self):
        config = Config("game.json")
        config.load()

        border_position = ((0, 0), (0, config.get_window("Height") - 305),
                           (0, 0), (config.get_window("Width") - 5, 0))
        border_size = ((config.get_window("Width"), 5), (config.get_window("Width"), 5),
                       (5, config.get_window("Height") - 300), (5, config.get_window("Height") - 300))

        for i, z in zip(border_position, border_size):
            border = Border(i, z, self.__color_border)
            self.__borders.append(border.rect)
            self.__borders_render.append(border)

    def create_energy(self):
        config = Config("game.json")
        config.load()

        energy_position = ((45, 100), (45, 500),
                           (config.get_window("Width") - 60, 100), (config.get_window("Width") - 60, 500))

        energy_size = ((10, 10), (10, 10), (10, 10), (10, 10))
        info = 1
        for i, z in zip(energy_position, energy_size):
            energy = Energy(i, z, self.__color_energy, info, 33)
            info += 1
            self.__energys.append(energy.rect)
            self.__energys_render.append(energy)

    def get_borders_render(self):
        return self.__borders_render

    def get_borders(self):
        return self.__borders

    def get_energy_render(self):
        return self.__energys_render

    def get_energy(self):
        return self.__energys
