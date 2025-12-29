# TODO (konkretne zadania)

1. Generowanie przypadków testowych

* \[x] napisać algorytm Johnsona do generacji połączeń kolejowych
* \[ ] dodać możliwość generacji listy transportów
* \[ ] połączyć generowanie grafu miast i listy ładunków aby tworzyć obiekt klasy TransportProblemObject

2. Zapis/odczyt z pliku

* \[ ] przenieść zapis i odczyt z pliku do klasy TransportProblemObject jako metody klasy

3. Ocena rozwiązania

* \[ ] napisać funkcję ewaluującą rozwiązanie, jako metodę klasy TransportProblemObject

4. TransportProblemObject

* \[ ] dodać pola reprezentujące populację rozwiązań oraz parametry eksperymentu

5. Genetyka i populacja

* \[x] dokończyć metody krzyżujące i mutujące rozwiązanie
* \[x] dodać metody selekcji organizmów

# STRUKTURA CAŁOŚCIOWA PRACY (składowe projektu)

1. Generowanie danych

* \[x] generowanie mapy (generate\_graphs.py)
* \[ ] generowanie listy (TBD)
* \[x] zapis/odczyt mapy i listy z pliku CSV (file\_handling.py)

2\. Klasy obiektów

* \[x] obiekty reprezentujące klasy populacje, organizmy i ich składowe (organisms\_and\_population.py)
* \[x] klasa reprezentująca przypadek testowy (problem\_description.py)

3\. Interfejs

* \[ ] warstwa graficzna interfejsu (TBD)
* \[ ] zapis i odczyt do pliku konfiguracyjnego (TBD)
* \[ ] konfiguracja algorytmu (TBD)

4\. Główny algorytm

* \[x] mechanizm selekcji (organisms\_and\_population.py)
* \[x] mechanizm krzyżowania (organisms\_and\_population.py)
* \[x] mechanizm mutacji (organisms\_and\_population.py)
* \[x] funkcja celu (problem\_description.py)
* \[x] algorytm konstrukcyjny (problem\_description.py)
* \[ ] (\*) możliwość zapisu algorytmu do pliku w trakcie działania (TBD)
* \[ ] mechanizm algorytmu genetycznego (genetic\_algorithm.py)

5\. Testy

6\. Sprawozdanie

