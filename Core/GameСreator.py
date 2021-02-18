import pygame
import time
from Class.GameSystem import GameSystem
from Model.DataBaseGame import DataBaseGame
from Class.Interfase.IObserver import Observer
from threading import Thread


def game_start(player_1, player_2, id_game):
    pygame.init()
    winner = 1
    clock = pygame.time.Clock()
    database = DataBaseGame()
    database.is_playing = True
    game_system = GameSystem(database, player_1, player_2)
    game_system.game_init()

    while database.is_playing:
        game_system.update_game(clock.tick(120))
        if database.score[0] > database.score[1]:
            winner = 2
        else:
            winner = 1
    game_system.game_over(winner)


class GameCreator(Observer):
    def __init__(self):
        self.network = None
        self.id_game = 0
        self.colors = []

    def update(self, subject):
        if type(subject) == list:
            new_player = subject[1:]
            print(new_player)

            new_player = sorted(new_player, key=lambda x: x.mmr and x.state == "search")
            if len(new_player) > 1:
                new_player[0].state = "in_game"
                new_player[1].state = "in_game"

                if len(self.colors) > 2:
                    self.colors = self.colors[-2:]
                new_player[0].network.send_message({"Type_message": "Server", "Type_command": "Started_game",
                                                    "Side": "left", "Color": self.colors[0], "EnemyColor": self.colors[1]})
                new_player[1].network.send_message({"Type_message": "Server", "Type_command": "Started_game",
                                                    "Side": "right", "Color": self.colors[1], "EnemyColor": self.colors[0]})
                Thread(target=game_start, args=(new_player[0], new_player[1], self.id_game), daemon=True).start()
                self.id_game += 1
