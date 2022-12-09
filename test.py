import unittest
from rejestracja import rejestracja
from datetime import datetime, timedelta

class mojeTesty(unittest.TestCase):

    def test_interwalCzasu_1(self):
        testowaRejestracja = rejestracja("1", "file")

        czas_1 = "2022-12-06 13:45:39"
        czas_2 = "2022-12-06 13:45:39"
        wynik = testowaRejestracja.timeInterval(czas_1, czas_2)
        self.assertEqual(wynik, 0)

    def test_interwalCzasu_2(self):
        testowaRejestracja = rejestracja("1", "file")

        czas_1 = "2022-12-06 13:45:39"
        czas_2 = "2022-12-06 13:45:40"
        wynik = testowaRejestracja.timeInterval(czas_1, czas_2)
        self.assertEqual(wynik, 1)

    def test_interwalCzasu_3(self):
        testowaRejestracja = rejestracja("1", "file")
        czas_1 = "2022-12-06 13:45:38"
        czas_2 = "2022-12-06 13:45:39"
        wynik = testowaRejestracja.timeInterval(czas_1, czas_2)
        self.assertEqual(wynik, 1)

    def test_initCzasu(self):
        testowaRejestracja = rejestracja("1", "file")
        czas_1 = datetime.now()
        delta = timedelta(seconds = 2)
        komunikat = "Czasy nie są zbliżone!"
        self.assertAlmostEqual(testowaRejestracja.now, czas_1, None, komunikat, delta)

    def test_reqFromApi(self):
        testowaRejestracja = rejestracja("1")
        apiCode = 200
        self.assertEqual(testowaRejestracja.getUserInfoFromApi(), apiCode)

    def test_reqFromApiNonUser(self):
        test = "nonExistentUser"
        testowaRejestracja = rejestracja(test, "api")
        self.assertEqual(len(testowaRejestracja.user), 0)

    def test_reqFromApiExistentUser(self):
        test = "0015516040"
        testowaRejestracja = rejestracja(test, "api")
        self.assertNotEqual(len(testowaRejestracja.user), 0)

        """
        konstruktor zawiera parametr z kluczem:
            - co jeśli ten klucz jest pusty?
            - co jeśli ten klucz nie spełnia kryteriów regex?
            - 
        Czy w testach mogę powołać obiekt globalny i się do niego odnosić?
            Sceanriusz: testy powołują nowy obiekt globalny rejestracji.
            Każdy kolejny test powołuje obiekt lokalny, który powinien pasować do globalnego(?)  
            
        Klasa rejestracja konstruuje obiekt zawierający informacje o logowaniu.
        Requesty zajmują znikome miejsce w tej zabawie.
        Czy wyodrębniać requesty do osobnej klasy?
        
        Co to jest coverage?
        
        """


if __name__ == '__main__':
    unittest.main()
