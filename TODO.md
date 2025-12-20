# TODO (konkretne zadania)

1. Generowanie przypadków testowych

* \[ ] napisać algorytm Johnsona do generacji połączeń kolejowych
* \[ ] dodać możliwość generacji listy transportów
* \[ ] połączyć generowanie grafu miast i listy ładunków aby tworzyć obiekt klasy TransportProblemObject

2. Zapis/odczyt z pliku

* \[ ] przenieść zapis i odczyt z pliku do klasy TransportProblemObject jako metody klasy

3. Ocena rozwiązania

* \[ ] napisać funkcję ewaluującą rozwiązanie, jako metodę klasy TransportProblemObject

4. TransportProblemObject

* \[ ] dodać pola reprezentujące populację rozwiązań oraz parametry eksperymentu

5. Genetyka i populacja

* \[ ] dokończyć metody krzyżujące i mutujące rozwiązanie
* \[ ] dodać metody selekcji organizmów

# STRUKTURA CAŁOŚCIOWA PRACY (składowe projektu)

1. Generowanie danych

* \[ ] generowanie mapy (generate\_graphs.py)
* \[ ] generowanie listy (TBD)
* \[ ] zapis/odczyt mapy i listy z pliku CSV (file\_handling.py)

2\. Klasy obiektów

* \[ ] obiekty reprezentujące klasy populacje, organizmy i ich składowe (organisms\_and\_population.py)
* \[ ] klasa reprezentująca przypadek testowy (problem\_description.py)

3\. Interfejs

* \[ ] warstwa graficzna interfejsu (TBD)
* \[ ] zapis i odczyt do pliku konfiguracyjnego (TBD)

4\. Główny algorytm

* \[ ] mechanizm selekcji (TBD)
* \[ ] mechanizm krzyżowania (TBD)
* \[ ] mechanizm mutacji (TBD)
* \[ ] funkcja celu (TBD)
* \[ ] (\*) możliwość zapisu algorytmu do pliku w trakcie działania (TBD)
* \[ ] mechanizm algorytmu genetycznego

5\. Testy

6\. Sprawozdanie

