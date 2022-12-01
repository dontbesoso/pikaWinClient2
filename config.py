import json

class Config:
     def __init__(self):
        configFile = open('config.json')
        configData = json.load(configFile)
        configFile.close()

        self.apiPathLogowanie = (configData['apiPathLogin'])
        self.apiPathUser = (configData['apiPathUser'])
        self.appName = (configData['appName'])
        self.machineName = (configData['machineName'])

