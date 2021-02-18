from socket import *
from json import *
from Model.DataBase import DataBase


class NetWork:
    def __init__(self, sock):
        self.__socket_main = sock

    def listener(self):
        try:
            message = self.__socket_main.recv(1024).decode()
            try:
                js_convert_message = loads(message)
                return js_convert_message
            except:
                return loads('{"K_z": "False", "K_up": "False", "K_down": "False", "K_lshift": "False", "side": "right"}')
        except ConnectionResetError:
            model = list(filter(lambda x: x.network is not None
                                and x.network.get_socket().getsockname() == self.__socket_main.getsockname(),
                                DataBase().get_observer()))
            print(model)
            DataBase().detach(model[0])
            return None

    def send_message(self, message):
        message = dumps(message)
        self.__socket_main.send(message.encode())

    def close(self):
        self.__socket_main.close()

    def get_socket(self):
        return self.__socket_main
