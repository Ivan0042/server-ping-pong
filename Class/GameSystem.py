import pygame
from pygame.math import Vector2
from Class.Interfase.ISolid import Solide
from Class.Paddle import Paddle
from Class.Ball import Ball
from Class.Map import Map
from Class.EventSystem import EventSystem
from Model.DataBase import DataBase
import random
from Class.Config import Config


class GameSystem:
    def __init__(self, database, player_1, player_2):
        self.__player = {}
        self.__ball = []
        self.__event_system = None
        self.__main_display = None
        self.__paddle_left = None
        self.__paddle_right = None
        self.__ball = None
        self.__map = None
        self.__database = database
        self.__main_sprites = pygame.sprite.RenderPlain()
        self.__timer = 25000

        self.__player_1 = player_1
        self.__player_2 = player_2

    def game_init(self):
        config = Config("game.json")
        config.load()
        self.__main_display = pygame.display.set_mode((config.get_window("Width"), config.get_window("Height")), 0, 32)

        self.__database.set_position_paddles(config.get_position("Left_paddle"), config.get_position("Right_paddle"))

        self.__database.set_position_ball(config.get_position("Ball"))

        self.__paddle_left = Paddle(config.get_position("Left_paddle"), [10, 100],
                                    config.get_color("White"), 4, 4, 13, 1, (1, 0))

        self.__paddle_right = Paddle(config.get_position("Right_paddle"), [10, 100],
                                     config.get_color("White"), 4, 4, 13, 2, (-1, 0))

        self.__ball = [Ball(self.__database.get_position_ball(), [10, 10], config.get_color("White"),
                           5, 2, 8, (random.uniform(-0.5, 0.5), random.uniform(-0.2, 0.2)))]

        self.__map = Map(config.get_color("Red"), config.get_color("Turquoise"))

        self.__event_system = EventSystem({"paddle": {"left": [self.__player_1, self.__paddle_left],
                                                      "right": [self.__player_2, self.__paddle_right]},
                                           "ball": self.__ball, "map": self.__map, "timer": self.__timer}, self,
                                          self.__database)

    def update_game(self, c):
        self.__event_system.update(c)

    def restart(self):
        config = Config("game.json")
        config.load()        
        self.__timer = 25000    
        self.__paddle_left.energy = 33
        self.__paddle_left.position = self.__database.get_position_paddles()[0]
        self.__paddle_left.direction = (0, 0)
        self.__paddle_left.is_power_hit = False
        self.__paddle_right.energy = 33
        self.__paddle_right.position = self.__database.get_position_paddles()[1]
        self.__paddle_right.direction = (0, 0)
        self.__paddle_right.is_power_hit = False
        self.__ball = [Ball(self.__database.get_position_ball(), [10, 10], config.get_color("White"),
                           5, 2, 8, (random.uniform(-0.5, 0.5), random.uniform(-0.2, 0.2)))]
        self.__event_system = EventSystem({"paddle": {"left": [self.__player_1, self.__paddle_left],
                                                      "right": [self.__player_2, self.__paddle_right]},
                                           "ball": self.__ball, "map": self.__map, "timer": self.__timer}, self,
                                          self.__database)        

    def game_over(self, player_winner):
        self.__database.is_playing = False
        if player_winner == 1:
            player_winner = self.__player_1.get_name()
        else:
            player_winner = self.__player_2.get_name()

        message = {
            "Type_message": "Server",
            "Type_command": "Game_over",
            "Win": player_winner
        }

        self.__player_1.network.send_message(message)
        self.__player_2.network.send_message(message)
        self.__player_1.state = "main_menu"
        self.__player_2.state = "main_menu"
