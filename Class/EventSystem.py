import pygame
import sys
from pygame.locals import *
from pygame.math import Vector2
from Model.DataBase import DataBase
from Class.Ball import Ball
import random
from Class.Config import Config


class EventSystem:
    def __init__(self, game_objects, game_system, database):
        self.__game_objects = game_objects
        self.__game_system = game_system
        self.__database = database
        pygame.time.set_timer(self.__game_objects["paddle"]["left"][1].power_hit, 0)
        pygame.time.set_timer(self.__game_objects["paddle"]["right"][1].power_hit, 0)

    def update(self, c):
        event_1 = self.__game_objects["paddle"]["left"][0].network.listener()
        event_2 = self.__game_objects["paddle"]["right"][0].network.listener()
        for i in [event_1, event_2]:
            for event in pygame.event.get():
                if event.type == self.__game_objects["paddle"][i["side"]][1].power_hit:
                    self.__game_objects["paddle"][i["side"]][1].is_power_hit = False
                    pygame.time.set_timer(self.__game_objects["paddle"][i["side"]][1].power_hit, 0)
                if i["K_z"] == "True":
                    self.__game_objects["paddle"][i["side"]][1].is_power_hit = True
                    self.__game_objects["paddle"][i["side"]][1].punch()
                    pygame.time.set_timer(self.__game_objects["paddle"][i["side"]][1].power_hit, 1000)

                if event.type == self.__database.restart:
                    self.__game_system.restart()

                if event.type == self.__database.game_over:
                    self.__game_system.game_over(event.message)

                for j in self.__game_objects["map"].get_energy_render():
                    if event.type == j.energy_take:
                        j.is_energy = True
                        pygame.time.set_timer(j.energy_take, 0)

            self.__move_player(i)
            self.__paddle_hit_map(i)
            self.__paddle_hit_ball(i)
            self.__hit_energy(i)
            
        if self.__game_objects["timer"] <= c and self.__game_objects["timer"] >= 0:
            config = Config("game.json")
            config.load()            
            for i in range(len(self.__game_objects["ball"])):
                self.__game_objects["ball"].append(Ball((self.__game_objects["ball"][i].rect.centerx,
                                                         self.__game_objects["ball"][i].rect.centery), [10, 10],
                                                        config.get_color("White"),
                                                        5, 2, 8, (random.uniform(-0.5, 0.5), random.uniform(-0.2, 0.2))))
                self.__game_objects["ball"].append(Ball((self.__game_objects["ball"][i].rect.centerx,
                                                         self.__game_objects["ball"][i].rect.centery), [10, 10],
                                                        config.get_color("White"),
                                                        5, 2, 8, (random.uniform(-0.5, 0.5), random.uniform(-0.2, 0.2))))                
        self.__game_objects["timer"] -= c
        if self.__game_objects["timer"] < -5000:
            self.__game_objects["timer"] = 25000
            
        self.__ball_reflect_map()
        for i in self.__game_objects["ball"]:
            i.move()
        self.update_player()

    def __move_player(self, info):
        direction = (0, 0)
        if info["K_up"] == "True":
            direction = (0, -1)
        elif info["K_down"] == "True":
            direction = (0, 1)
        self.__game_objects["paddle"][info["side"]][1].run(info["K_lshift"])
        self.__game_objects["paddle"][info["side"]][1].direction = Vector2(direction)
        self.__game_objects["paddle"][info["side"]][1].move()

    def __ball_reflect_map(self):
        for i in self.__game_objects["ball"]:
            hit = i.rect.collidelist(self.__game_objects["map"].get_borders()) + 1
            if hit in (3, 4):
                pygame.event.post(self.__database.restart_event)
                self.__database.set_score(hit % 3, 1)
            if hit == 2:
                i.reflect((0, 1))
            if hit == 1:
                i.reflect((0, -1))

    def __paddle_hit_map(self, i):
        hit = self.__game_objects["paddle"][i["side"]][1].rect.collidelist(self.__game_objects["map"].get_borders()) + 1
        if hit == 2:
            self.__game_objects["paddle"][i["side"]][1].reflect((0, 1))
            self.__game_objects["paddle"][i["side"]][1].direction = Vector2((0, 0))
        if hit == 1:
            self.__game_objects["paddle"][i["side"]][1].reflect((0, -1))
            self.__game_objects["paddle"][i["side"]][1].direction = Vector2((0, 0))

    def __paddle_hit_ball(self, i):
        for j in self.__game_objects["ball"]:
            hit = j.rect.colliderect(self.__game_objects["paddle"][i["side"]][1].rect)
            if hit:
                j.direction += self.__game_objects["paddle"][i["side"]][1].is_ball_direction
    
                speed_punch = self.__game_objects["paddle"][i["side"]][1].punch()
                j.set_speed(speed_punch)

    def add_game_object(self, name_object, game_object):
        self.__game_objects[name_object] = game_object

    def __hit_energy(self, i):
        hit = self.__game_objects["paddle"][i["side"]][1].rect.collidelist(self.__game_objects["map"].get_energy())
        if hit != -1:
            energy = self.__game_objects["map"].get_energy_render()[hit]
            if energy.is_energy:
                energy.is_energy = False
                pygame.time.set_timer(energy.energy_take, 10000)
                self.__game_objects["paddle"][i["side"]][1].set_energy(energy.energy)

    def update_player(self):
        energy = self.__game_objects["map"].get_energy_render()
        if self.__game_objects["timer"] < 0:
            c = 'Мультиболл!!!'
        else:
            c = str(self.__game_objects["timer"] // 1000)
        balls_x = []
        balls_y = []
        for i in self.__game_objects["ball"]:
            balls_x.append(i.rect.centerx)
            balls_y.append(i.rect.centery)
        message = {
            "Type_message": "Update_position",
            "Position": {
                "paddle": {
                    "x": [self.__game_objects["paddle"]["left"][1].rect.centerx,
                          self.__game_objects["paddle"]["right"][1].rect.centerx],
                    "y": [self.__game_objects["paddle"]["left"][1].rect.centery,
                          self.__game_objects["paddle"]["right"][1].rect.centery],
                    "energy": [self.__game_objects["paddle"]["left"][1].energy,
                               self.__game_objects["paddle"]["right"][1].energy]
                },
                "balls": {"x": balls_x, "y": balls_y},
                "energy": {
                    "id_energy": [],
                    "flag": []
                },
                "score": self.__database.score, "timer": c
            }}
        
        for j in range(len(energy)):
            message["Position"]["energy"]["id_energy"].append(j)
            message["Position"]["energy"]["flag"].append(energy[j].is_energy)

        self.__game_objects["paddle"]["left"][0].network.send_message(message)
        self.__game_objects["paddle"]["right"][0].network.send_message(message)
