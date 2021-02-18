from Core.GameСreator import GameCreator
from Model.Player import Player
from Model.DataBase import DataBase
from socket import *
from threading import Thread
from Core.Network import NetWork

sock = socket()
sock.bind(('', 2510))
sock.listen(6)

gc = GameCreator()
DataBase().attach(gc)


def client_core(socket_client):
    global gc
    network_core = NetWork(socket_client)
    reg_message = network_core.listener()
    if reg_message["Type_Command"] is not None:
        user = Player(reg_message["Name_user"], reg_message["Ip_user"],  reg_message["Mmr_user"], network_core)
        if len(DataBase().get_observer()) > 2:
            for i in DataBase().get_observer():
                DataBase().detach(i)
            DataBase().attach(gc)        
        gc.colors.append(reg_message["Color"])
        DataBase().attach(user)
    else:
        return
    while True:
        command = user.network.listener()
        if command is not None:
            DataBase().add_list_command(command)
        else:
            break


while True:
    print('connection...')
    client, mass = sock.accept()
    print(mass, 'connect')
    Thread(target=client_core, args=(client,), daemon=True).start()
