from datetime import datetime
import requests
from plyer import notification
from config import Config

class rejestracja:
    def __init__(self, cardKey, report_method="api"):

        self.config = Config()
        self.report_method = report_method
        self.now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.txt_log = ""
        self.filename = f"inlog-{self.now[:10]}"

        self.biezaceLogowanie = {
            'id': 0,
            'userid': cardKey,
            'userName': cardKey,
            'timeIn': self.now,
            'type': "INSTART",
            'prevId': 0,
            'sessionId': 0,
            'machineName': self.config.machineName
        }

        self.report()

    def report(self):
        if self.report_method == "file":
            #self.getUserInfoFromApi();
            self.sendRequestToFile()

        if self.report_method == "api":
            self.getUserInfoFromApi();

            self.sendRequestToApi()
            self.sendRequestToFile()

    def getUserInfoFromApi(self):
        getUserRequest = requests.get(self.config.apiPathUser + '?cardId=' + self.biezaceLogowanie['userid'])
        print("Api o użytkonwiku: ", self.config.apiPathUser + '?cardId=' + self.biezaceLogowanie['userid'])

        getUserFirst = requests.get(self.config.apiPathLogin + '?userid=' + self.biezaceLogowanie['userid'] + '&type=INSTART')
        getUserLast = requests.get(self.config.apiPathLogin + '?userid=' + self.biezaceLogowanie['userid'])

        print("Ostatnie logowanie:", self.config.apiPathLogin + '?userid=' + self.biezaceLogowanie['userid'])
        print("Pierwsze logowanie: ", self.config.apiPathLogin + '?userid=' + self.biezaceLogowanie['userid'] + '&type=INSTART')

        user = getUserRequest.json()
        if len(user):
            self.biezaceLogowanie['userName'] = user[-1].get('name')

        self.ostatnieLogowanie = self.calculateLastLogin(getUserLast.json())
        self.pierwszeLogowanie = self.calculateFirstLogin(getUserFirst.json())

    def calculateFirstLogin(self, pierwszeLogowanie):
        if len(pierwszeLogowanie):
            self.biezaceLogowanie['sessionId'] = pierwszeLogowanie[-1].get('id')
        else:
            self.biezaceLogowanie['sessionId'] = 0

    def calculateLastLogin(self, ostatnieLogowanie):
        if len(ostatnieLogowanie):
            czasOstatniegoLogowania = ostatnieLogowanie[-1].get('timeIn')
            czas = self.timeInterval(self.now, czasOstatniegoLogowania)

            print(f"Czas logowania: ", self.now)
            print(f"Czas ostatniego: ", czasOstatniegoLogowania)
            print(f"Interwał między logowaniami: ", czas)

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

            if (czas > 600):
                self.biezaceLogowanie['typLogowania'] = "OUTEND"
        else:
            self.biezaceLogowanie['prevId'] = 0
            self.biezaceLogowanie['sessionId'] = 0

    def sendRequestToApi(self):
        try:
            postRequest = requests.post(self.config.apiPathLogin, json=self.biezaceLogowanie)
        except requests.exceptions.RequestException as e:
            print("Błąd logowania: ", e.errno)
            return -1
        else:
            self.showNotification()
            return postRequest.status_code

        self.log = ""

    def sendRequestToFile(self):
        self.txt_log = self.buildTextLog()

        with open(f"{self.filename}.csv", "a+") as f:
            print("Zapisywany log: ", self.txt_log)
            print(self.txt_log, file=f)

        print(f"[+] Zapisano w pliku: {self.filename}.csv")
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
        return abs((d2 - d1).total_seconds() / 60)







