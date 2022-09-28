from randomData import d
from DatabaseManager import DatabaseManager

# The globals file contains global variables used across threads.
# It contains a few shared instances of classes, and a couple variables that need to be accessed everywhere.

def init():
    global db # Global DatabaseManager instance
    db = DatabaseManager()
    db.activeTable = 'Test Launch-2022-09-22'
    
    global rdInst
    rdInst = d()

    global isSetup # Responsible for determining if setup process has been run yet
    isSetup = True