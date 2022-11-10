import GUI
from threading import Thread
import globals

globals.init()

rbThread = Thread(target=globals.rbInst.receive(),args=())

rdThread.start()
GUI.start()
