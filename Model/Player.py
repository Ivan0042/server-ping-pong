from Class.Interfase.IObserver import Observer
import json as js


class Player(Observer):
    def __init__(self, name, id_player, mmr, network):
        self.__name = name
        self.__id_player = id_player
        self.network = network
        self.state = "search"
        self.mmr = mmr

    def __repr__(self):
        return f"Player {self.__name}, {self.__id_player}"

    def __str__(self):
        return f"Player {self.__name}, {self.__id_player}"

    def update(self, subject):
        pass

    def get_name(self):
        return self.__name
