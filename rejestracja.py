from datetime import datetime
import requests
from plyer import notification
from config import Config

class rejestracja:
    def __init__(self, cardKey, report_method="api"):

        self.config = Config()
        self.report_method = report_method
        self.now = datetime.now()

        self.txt_log = ""
        self.filename = "inlog-" + self.now.strftime("%Y-%m-%d %H:%M:%S")[:10]

        self.biezaceLogowanie = {
            'id': 0,
            'userid': cardKey,
            'userName': cardKey,
            'timeIn': self.now.strftime("%Y-%m-%d %H:%M:%S"),
            'type': "INSTART",
            'prevId': 0,
            'sessionId': 0,
            'machineName': self.config.machineName
        }

        self.requestCode = self.getUserInfoFromApi()

        if len(self.user):
            self.biezaceLogowanie['userName'] = self.user[-1].get('name')

        self.report()

    def report(self):
        if self.report_method == "file":
            self.getUserInfoFromApi();
            self.sendRequestToFile()

        if self.report_method == "api":
            self.getUserInfoFromApi();

            self.sendRequestToApi()
            self.sendRequestToFile()

    def getUserInfoFromApi(self):
        getUserRequest = requests.get(self.config.apiPathUser + '?cardId=' + self.biezaceLogowanie['userid'])

        self.user = getUserRequest.json()
        return getUserRequest.status_code

    def getUserTimes(self):
        getUserFirst = requests.get(self.config.apiPathLogin + '?userid=' + self.biezaceLogowanie['userid'] + '&type=INSTART')
        getUserLast = requests.get(self.config.apiPathLogin + '?userid=' + self.biezaceLogowanie['userid'])

        self.pierwszeLogowanie = self.calculateFirstLogin(getUserFirst.json())
        self.ostatnieLogowanie = self.calculateLastLogin(getUserLast.json())

    def calculateFirstLogin(self, pierwszeLogowanie):
        if len(pierwszeLogowanie):
            self.biezaceLogowanie['sessionId'] = pierwszeLogowanie[-1].get('id')
        else:
            self.biezaceLogowanie['sessionId'] = 0

    def calculateLastLogin(self, ostatnieLogowanie):
        if len(ostatnieLogowanie):
            czasOstatniegoLogowania = ostatnieLogowanie[-1].get('timeIn')
            czas = self.timeInterval(self.now, czasOstatniegoLogowania)

            self.biezaceLogowanie['prevId'] = ostatnieLogowanie[-1].get('id')
            typOstatniegoLogowania = ostatnieLogowanie[-1].get('type')

            if typOstatniegoLogowania == "INSTART":
                self.biezaceLogowanie['typLogowania'] = "INBREAK"
            elif typOstatniegoLogowania == "INBREAK":
                self.biezaceLogowanie['typLogowania'] = "OUTBREAK"
            elif typOstatniegoLogowania == "OUTBREAK":
                self.biezaceLogowanie['typLogowania'] = "INBREAK"
            elif typOstatniegoLogowania == "OUTEND":
                self.biezaceLogowanie['typLogowania'] = "INSTART"

            if (czas > 43200): #12h * 60' * 60''
                self.biezaceLogowanie['typLogowania'] = "OUTEND"
        else:
            self.biezaceLogowanie['prevId'] = 0
            self.biezaceLogowanie['sessionId'] = 0

    def sendRequestToApi(self):
        try:
            postRequest = requests.post(self.config.apiPathLogin, json=self.biezaceLogowanie)
        except requests.exceptions.RequestException as e:
            return -1
        else:
            self.showNotification()
            return postRequest.status_code

        self.log = ""

    def sendRequestToFile(self):
        self.txt_log = self.buildTextLog()

        with open(f"{self.filename}.csv", "a+") as f:
            print(self.txt_log, file=f)

        self.txt_log = ""

    def buildTextLog(self):
        return self.biezaceLogowanie['userid'] \
                        + ";" + self.biezaceLogowanie['timeIn'] \
                        + ";" + self.biezaceLogowanie['timeIn'][:10] \
                        + ";" + self.biezaceLogowanie['timeIn'][-8:] \
                        + ";" + self.biezaceLogowanie['machineName']

    def showNotification(self):
        notification.notify(
            title="Wykonano logowanie\n",
            message=f"Wykonano logowanie \nCzas: {self.now}",
            app_icon="plum.ico",
            timeout=0,
            app_name="Plum!"
        )
        return 0

    def timeInterval(self, d1, d2):
        d1 = datetime.strptime(d1, "%Y-%m-%d %H:%M:%S")
        d2 = datetime.strptime(d2, "%Y-%m-%d %H:%M:%S")
        return (d2 - d1).total_seconds()







