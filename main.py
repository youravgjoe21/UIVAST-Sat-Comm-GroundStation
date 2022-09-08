import GUI
from threading import Thread
import globals

globals.init()

rdThread = Thread(target=globals.rdInst.generateData,args=())

rdThread.start()
GUI.start()
