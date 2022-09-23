from datetime import datetime
import math
import random
from time import sleep
import json
import globals

class d():

    moduleStatus = {'Radio':'Waiting on Status','Satellite':'Waiting on Status','Power Board':'Waiting on Status'}
    sensorData = {'external-temp':0,'internal-temp':0,'pressure':0}
    updateTime = datetime(1999,1,1)
    lat = 0
    long = 0
    alt = 0

    def generateData(self):
        while True:
            if globals.isSetup:

                self.moduleStatus = {'Radio':       not math.floor(random.randint(0,10) / 10),
                                     'Satellite':   not math.floor(random.randint(0,10) / 10),
                                     'Power Board': not math.floor(random.randint(0,10) / 10)}
                self.sensorData = {'external-temp': random.randint(-100,70), 'internal-temp': random.randint(-20,60), 'pressure': random.randint(40,60)}

                self.updateTime = datetime.now()
                self.lat,self.long,self.alt = random.randint(1,100000),random.randint(1,100000),random.randint(1,100000)

                globals.db.writeRow(self.updateTime, self.lat, self.long, self.alt, self.generateModuleJSON(),self.generateSensorJSON())

            sleep(10)

    def getModuleStatus(self):
        return self.moduleStatus

    def getSensorData(self):
        return self.sensorData

    def getUpdateTime(self):
        return self.updateTime

    def getGPSData(self):
        return self.lat, self.long, self.alt

    def generateModuleJSON(self):
        modJSON = {'radio':[
                    {'display-name':'Radio',
                     'value':self.moduleStatus['Radio']
                    }],
                    'satellite':[
                    {
                     'display-name':'Satellite',
                     'value':self.moduleStatus['Satellite']
                    }],
                    'power-board':[
                    {
                     'display-name':'Power Board',
                     'value':self.moduleStatus['Power Board']
                    }]
                  }
        
        return json.dumps(modJSON)

    def generateSensorJSON(self):
        sensorJSON = {'external-temp':[
                        {'display-name':'Outside Temperature',
                         'value':self.sensorData['external-temp']
                        }],
                      'internal-temp':[
                        {'display-name':'Payload Temperature',
                         'value':self.sensorData['internal-temp']
                        }],
                      'pressure':[
                        {'display-name':'Pressure',
                         'value':self.sensorData['pressure']
                        }]
                     }

        return json.dumps(sensorJSON)