from randomData import d
from DatabaseManager import DatabaseManager

# The globals file contains global variables used across threads.
# It contains a few shared instances of classes, and a couple variables that need to be accessed everywhere.

def init():
    global db # Global DatabaseManager instance
    db = DatabaseManager()
    db.activeTable = 'test'
    
    global rdInst
    rdInst = d()

    global isSetup # Responsible for determining if setup process has been run yet
    isSetup = False