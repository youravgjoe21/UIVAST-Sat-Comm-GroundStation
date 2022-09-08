from datetime import datetime
import math
import random
from time import sleep
import json
import globals

class d():

    moduleStatus = {}
    sensorData = {}
    updateTime = None
    lat = 0
    long = 0
    alt = 0

    def generateData(self):
        global lat, long, alt, moduleStatus, updateTime, sensorData
        
        while True:

            moduleStatus = {'Radio':       not math.floor(random.randint(0,10) / 10),
                            'Satellite':   not math.floor(random.randint(0,10) / 10),
                            'Power Board': not math.floor(random.randint(0,10) / 10)}
            sensorData = {'external-temp': random.randint(-100,70), 'internal-temp': random.randint(-20,60), 'pressure': random.randint(40,60)}

            updateTime = datetime.now()
            lat,long,alt = random.randint(1,100000),random.randint(1,100000),random.randint(1,100000)

            globals.db.writeRow(updateTime, lat, long, alt, self.generateModuleJSON(),self.generateSensorJSON())

            sleep(10)

    def getModuleStatus(self):
        return moduleStatus

    def getSensorData(self):
        return sensorData

    def getUpdateTime(self):
        return updateTime

    def getGPSData(self):
        return lat, long, alt

    def generateModuleJSON(self):
        modJSON = {'radio':[
                    {'display-name':'Radio',
                     'value':moduleStatus['Radio']
                    }],
                    'satellite':[
                    {
                     'display-name':'Satellite',
                     'value':moduleStatus['Satellite']
                    }],
                    'power-board':[
                    {
                     'display-name':'Power Board',
                     'value':moduleStatus['Power Board']
                    }]
                  }
        
        return json.dumps(modJSON)

    def generateSensorJSON(self):
        sensorJSON = {'external-temp':[
                        {'display-name':'Outside Temperature',
                         'value':sensorData['external-temp']
                        }],
                      'internal-temp':[
                        {'display-name':'Payload Temperature',
                         'value':sensorData['internal-temp']
                        }],
                      'pressure':[
                        {'display-name':'Pressure',
                         'value':sensorData['pressure']
                        }]
                     }

        return json.dumps(sensorJSON)