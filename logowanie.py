from datetime import datetime
import requests
import re
from plyer import notification


class logowanie:
    def __init__(self, config, cardKey, report_method="file"):

        """ Logowanie - układa na podstawie klucza wpis do logowania
            Odseparować i api i metody tekstowe od "logowania"
            Klasa config może się powoływać w każdej klasie, w której jest potrzebna
        """

        self.key = cardKey
        self.now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")[:10]
        self.txt_log = ""
        self.report_method = report_method
        self.filename = f"inlog-{self.now}"

        self.apiUrlLogowanie = config.apiPathLogowanie
        self.apiUrlPracownicy = config.apiPathUser
        self.machineName = config.machineName

        print(self.apiUrlLogowanie)
        print(self.apiUrlPracownicy)
        print(self.machineName)

        self.report()
        # self.report_to_api(self.log)
    """
    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                print("Space")
                name = " "
            elif name == "enter":
                name = ""
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name
    """
    def report(self):

        if self.report_method == "file":
            self.sendRequestToFile()

        if self.report_method == "api":
            self.sendRequestToApi(self.key)
            self.sendRequestToFile()

    def sendRequestToApi(self):
        now = datetime.now()
        timeIn = f"{now}"[:19]

        try:

            getUserRequest = requests.get(self.apiUrlPracownicy + '?cardId=' + self.key)
            print("Api o użytkonwiku: ", self.apiUrlPracownicy + '?cardId=' + self.key)

            getUserFirst = requests.get(self.apiUrlLogowanie + '?userid=' + self.key + '&type=INSTART')
            getUserLast = requests.get(self.apiUrlLogowanie + '?userid=' + self.key)

            print("Ostatnie logowanie:", self.apiUrlLogowanie + '?userid=' + self.key)
            print("Pierwsze logowanie: ", self.apiUrlLogowanie + '?userid=' + self.key + '&type=INSTART')

        except requests.exceptions.RequestException as e:
            logowanie = {
                'id': 0,
                'userid': self.key,
                'userName': self.key,
                'timeIn': timeIn,
                'type': "INSTART",
                'prevId': 0,
                'sessionId': 0,
                'machineName': self.machineName
            }
        else:
            user = getUserRequest.json()
            if len(user):
                nazwaUzytkownika = user[-1].get('name')
            else:
                nazwaUzytkownika = self.key


            ostatnieLogowanie = getUserLast.json()

            if len(ostatnieLogowanie):
                czasOstatniegoLogowania = ostatnieLogowanie[-1].get('timeIn')
                czas = self.timeInterval(timeIn, czasOstatniegoLogowania)
                print(f"Czas logowania: ", timeIn)
                print(f"Czas ostatniego: ", czasOstatniegoLogowania)
                print(f"Interwał między logowaniami: ", czas)

                if (czas > 600):
                    typOstatniegoLogowania = "OUTEND"

                typOstatniegoLogowania = ostatnieLogowanie[-1].get('type')
                prevId = ostatnieLogowanie[-1].get('id')

                pierwszeLogowanie = getUserFirst.json()
                if len(pierwszeLogowanie):
                    sessionId = pierwszeLogowanie[-1].get('id')
                else:
                    sessionId = 0

            else:
                typOstatniegoLogowania = "OUTEND"
                prevId = 0
                sessionId = 0



            #Obliczenia na czasie

            print("Ostatnie logowanie: ", ostatnieLogowanie)

            if typOstatniegoLogowania == "INSTART":
                typLogowania = "INBREAK"

            elif typOstatniegoLogowania == "INBREAK":
                typLogowania = "OUTBREAK"

            elif typOstatniegoLogowania == "OUTBREAK":
                typLogowania = "INBREAK"

            elif typOstatniegoLogowania == "OUTEND":
                typLogowania = "INSTART"


            #print("Wszystekie logowania użytkownika: ", logowania)

            logowanie = {
                'id': 0,
                'userid': self.key,
                'userName': nazwaUzytkownika,
                'timeIn': timeIn,
                'type': typLogowania,
                'prevId': prevId,
                'sessionId': sessionId,
                'machineName': self.machineName,
            }

        self.txt_log += logowanie.get('userid') \
                        + ";" + logowanie.get('timeIn') \
                        + ";" + logowanie.get('timeIn')[:10] \
                        + ";" + logowanie.get('timeIn')[-8:] \
                        + ";" + self.machineName

        print("Self.txt_log: ", self.txt_log)

        print("Dane wykonanego logowania: ", logowanie)

        try:
            postRequest = requests.post(self.apiUrlLogowanie, json=logowanie)
            print(postRequest.status_code)

        except requests.exceptions.RequestException as e:
            print("Błąd logowania: ", e.errno)
        else:
            notification.notify(
                title="Wykonano logowanie\n",
                message=f"Wykonano logowanie \nCzas: {timeIn}",
                app_icon="plum.ico",
                timeout=0,
                app_name="Plum!"
            )
        self.log = ""

    def sendRequestToFile(self):
        with open(f"{self.filename}.csv", "a+") as f:
            print("Zapisywany log: ", self.txt_log)
            print(self.txt_log, file=f)
        print(f"[+] Zapisano w pliku: {self.filename}.csv")
        self.txt_log = ""

    def timeInterval(self, d1, d2):
        d1 = datetime.strptime(d1, "%Y-%m-%d %H:%M:%S")
        d2 = datetime.strptime(d2, "%Y-%m-%d %H:%M:%S")
        return abs((d2 - d1).total_seconds() / 60)







