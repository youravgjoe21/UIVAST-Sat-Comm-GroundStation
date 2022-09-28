# Global variables must be initialized before anything else can execute
import globals
globals.init()

import GUI
from threading import Thread

rdThread = Thread(target=globals.rdInst.generateData,args=())

rdThread.start()
GUI.start()