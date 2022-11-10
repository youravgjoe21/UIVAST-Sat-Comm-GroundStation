from randomData import d
from DatabaseManager import DatabaseManager

import sys

sys.path.append('Ground_Station-main')
from Iridium import Iridium

# The globals file contains global variables used across threads.
# It contains a few shared instances of classes, and a couple variables that need to be accessed everywhere.

def init():
    global db # Global DatabaseManager instance
    db = DatabaseManager()
    db.activeTable = 'test'
    
    # global rdInst
    # rdInst = d()

    global rbInst
    rbInst = Iridium()
    global rdInst
    rdInst = rbInst

    global isSetup # Responsible for determining if setup process has been run yet
    isSetup = False