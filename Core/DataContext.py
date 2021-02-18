import pyodbc
from Model import Goods, MapStorage
from Class.Interfase.ISolid import Solide
from Class.Entity.EntityClass import EntityModel


class DataContext(metaclass=Solide):
    __server = 'localhost'
    __database = 'SmartSorageData'
    __connect = pyodbc.connect("DRIVER={ODBC Driver 13 for SQL Server};"
                               "Server=" + __server + ";"
                               "Database=" + __database + ";"
                               "Trusted_Connection=yes;"
                               )
    __link = __connect.cursor()

    Goods = EntityModel(Goods.Goods(), __link, __connect)
    MapStorage = EntityModel(MapStorage.MapStorage(), __link, __connect)



