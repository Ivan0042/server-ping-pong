from Class.Interfase.IObserver import Subject
from Class.Interfase.ISolid import Solide


class DataBase(Subject):
    __observes = []
    __task_list_robot = []
    __command_list = []
    __metaclass__ = Solide

    def attach(self, observer):
        self.__observes.append(observer)
        self.notify(self.__observes)

    def notify(self, lists):
        for observer in self.__observes:
            observer.update(lists)

    def detach(self, observer):
        self.__observes.remove(observer)

    def add_list_command(self, command):
        self.__command_list.append(command)
        self.notify(self.__command_list.pop())

    def get_observer(self):
        return self.__observes
