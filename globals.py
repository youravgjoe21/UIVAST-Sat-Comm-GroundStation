from randomData import d
from DatabaseManager import DatabaseManager

def init():
    global db
    db = DatabaseManager()
    db.activeTable = 'test'
    global rdInst
    rdInst = d()
