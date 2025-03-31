import datetime
import json
import os

# Klasa reprezentująca książkę w bibliotece
class Ksiazka:
    """
    Reprezentuje książkę w bibliotece.

    Atrybuty:
    - tytul (str): Tytuł książki.
    - autor (str): Autor książki.
    - rok_wydania (int): Rok wydania książki.
    - id_ksiazki (int): Unikalny identyfikator książki.
    - wypozyczona (bool): Status wypożyczenia książki (True, jeśli wypożyczona).
    - data_zwrotu (str lub None): Data zwrotu książki, jeśli jest wypożyczona.
    """
    def __init__(self, tytul, autor, rok_wydania, id_ksiazki, wypozyczona=False, data_zwrotu=None):
        # Inicjalizacja atrybutów książki
        self.tytul = tytul
        self.autor = autor
        self.rok_wydania = rok_wydania
        self.id_ksiazki = id_ksiazki
        self.wypozyczona = wypozyczona
        self.data_zwrotu = data_zwrotu

    def __str__(self):
        # Reprezentacja książki jako ciąg znaków
        status = "Wypożyczona" if self.wypozyczona else "Dostępna"
        zwrot = f", Data zwrotu: {self.data_zwrotu}" if self.data_zwrotu else ""
        return f"{self.id_ksiazki}: {self.tytul} - {self.autor} ({self.rok_wydania}) - Status: {status}{zwrot}"


# Klasa reprezentująca użytkownika biblioteki
class Uzytkownik:
    """
    Reprezentuje użytkownika biblioteki.

    Atrybuty:
    - imie (str): Imię użytkownika.
    - nazwisko (str): Nazwisko użytkownika.
    - id_uzytkownika (int): Unikalny identyfikator użytkownika.
    - wypozyczone_ksiazki (list): Lista książek wypożyczonych przez użytkownika.
    """
    def __init__(self, imie, nazwisko, id_uzytkownika, wypozyczone_ksiazki=None):
        # Inicjalizacja atrybutów użytkownika
        self.imie = imie
        self.nazwisko = nazwisko
        self.id_uzytkownika = id_uzytkownika
        self.wypozyczone_ksiazki = wypozyczone_ksiazki if wypozyczone_ksiazki is not None else []

    def __str__(self):
        # Reprezentacja użytkownika jako ciąg znaków
        return f"{self.id_uzytkownika}: {self.imie} {self.nazwisko} - Wypożyczone książki: {len(self.wypozyczone_ksiazki)}"


# Klasa reprezentująca bibliotekę
class Biblioteka:
    """
    Reprezentuje bibliotekę i zarządza książkami, użytkownikami oraz historią wypożyczeń.

    Atrybuty:
    - ksiazki (list): Lista książek w bibliotece.
    - uzytkownicy (list): Lista użytkowników biblioteki.
    - historia (list): Historia wypożyczeń książek.
    - plik_dane (str): Ścieżka do pliku JSON przechowującego dane biblioteki.
    """
    def __init__(self):
        # Inicjalizacja atrybutów biblioteki
        self.ksiazki = []  # Lista książek w bibliotece
        self.uzytkownicy = []  # Lista użytkowników biblioteki
        self.historia = []  # Historia wypożyczeń
        self.plik_dane = "test_data.json"  # Plik JSON do przechowywania danych
        self.wczytaj_dane()

    def zapisz_dane(self):
        """
        Zapisuje dane biblioteki (książki, użytkownicy, historia) do pliku JSON.
        """
        dane = {
            "ksiazki": [vars(ksiazka) for ksiazka in self.ksiazki],
            "uzytkownicy": [vars(uzytkownik) for uzytkownik in self.uzytkownicy],
            "historia": self.historia
        }
        with open(self.plik_dane, "w") as f:
            json.dump(dane, f, indent=4)
        print("Dane zostały zapisane.")

    def wczytaj_dane(self):
        """
        Wczytuje dane biblioteki (książki, użytkownicy, historia) z pliku JSON.
        """
        if os.path.exists(self.plik_dane):
            with open(self.plik_dane, "r") as f:
                dane = json.load(f)
                self.ksiazki = [Ksiazka(**ksiazka) for ksiazka in dane.get("ksiazki", [])]
                self.uzytkownicy = [Uzytkownik(**uzytkownik) for uzytkownik in dane.get("uzytkownicy", [])]
                self.historia = dane.get("historia", [])
        else:
            print("Plik test_data.json nie istnieje. Zostanie utworzony przy zapisie danych.")

    def dodaj_ksiazke(self, tytul, autor, rok_wydania):
        # Dodanie nowej książki do biblioteki
        try:
            id_ksiazki = len(self.ksiazki) + 1
            ksiazka = Ksiazka(tytul, autor, int(rok_wydania), id_ksiazki)
            self.ksiazki.append(ksiazka)
            print(f"Dodano książkę: {tytul}")
        except ValueError:
            print("Rok wydania musi być liczbą.")

    def usun_ksiazke(self, id_ksiazki):
        # Usunięcie książki z biblioteki
        for ksiazka in self.ksiazki:
            if ksiazka.id_ksiazki == id_ksiazki:
                self.ksiazki.remove(ksiazka)
                print(f"Usunięto książkę: {ksiazka.tytul}")
                return
        print(f"Książka o ID {id_ksiazki} nie istnieje.")

    def wyswietl_ksiazki(self):
        # Wyświetlenie listy książek w bibliotece
        if not self.ksiazki:
            print("Brak książek w bibliotece.")
            return
        for ksiazka in self.ksiazki:
            print(ksiazka)

    def szukaj_ksiazki(self, kryterium, wartosc):
        # Wyszukiwanie książek według kryterium
        if kryterium not in ["tytul", "autor", "rok_wydania"]:
            print("Nieprawidłowe kryterium wyszukiwania.")
            return
        znalezione = [
            ksiazka for ksiazka in self.ksiazki if str(getattr(ksiazka, kryterium, "")).lower() == wartosc.lower()
        ]
        if not znalezione:
            print("Brak wyników.")
        else:
            for ksiazka in znalezione:
                print(ksiazka)

    def dodaj_uzytkownika(self, imie, nazwisko):
        # Dodanie nowego użytkownika do biblioteki
        id_uzytkownika = len(self.uzytkownicy) + 1
        uzytkownik = Uzytkownik(imie, nazwisko, id_uzytkownika)
        self.uzytkownicy.append(uzytkownik)
        print(f"Dodano użytkownika: {imie} {nazwisko}")

    def wyswietl_uzytkownikow(self):
        # Wyświetlenie listy użytkowników
        if not self.uzytkownicy:
            print("Brak użytkowników.")
            return
        for uzytkownik in self.uzytkownicy:
            print(uzytkownik)

    def wypozycz_ksiazke(self, id_ksiazki, id_uzytkownika):
        # Wypożyczenie książki przez użytkownika
        try:
            id_ksiazki = int(id_ksiazki)
            id_uzytkownika = int(id_uzytkownika)
        except ValueError:
            print("ID książki i użytkownika muszą być liczbami.")
            return

        ksiazka = next((k for k in self.ksiazki if k.id_ksiazki == id_ksiazki), None)
        uzytkownik = next((u for u in self.uzytkownicy if u.id_uzytkownika == id_uzytkownika), None)

        if not ksiazka:
            print(f"Książka o ID {id_ksiazki} nie istnieje.")
            return
        if not uzytkownik:
            print(f"Użytkownik o ID {id_uzytkownika} nie istnieje.")
            return
        if ksiazka.wypozyczona:
            print(f"Książka '{ksiazka.tytul}' jest już wypożyczona.")
            return

        ksiazka.wypozyczona = True
        ksiazka.data_zwrotu = datetime.date.today() + datetime.timedelta(days=14)
        uzytkownik.wypozyczone_ksiazki.append(ksiazka)
        self.historia.append({"uzytkownik": f"{uzytkownik.imie} {uzytkownik.nazwisko}", "ksiazka": ksiazka.tytul, "data": str(datetime.date.today())})
        print(f"Użytkownik {uzytkownik.imie} {uzytkownik.nazwisko} wypożyczył książkę '{ksiazka.tytul}'.")

    def zwroc_ksiazke(self, id_ksiazki, id_uzytkownika):
        # Zwrot książki przez użytkownika
        try:
            id_ksiazki = int(id_ksiazki)
            id_uzytkownika = int(id_uzytkownika)
        except ValueError:
            print("ID książki i użytkownika muszą być liczbami.")
            return

        uzytkownik = next((u for u in self.uzytkownicy if u.id_uzytkownika == id_uzytkownika), None)
        if not uzytkownik:
            print(f"Użytkownik o ID {id_uzytkownika} nie istnieje.")
            return

        ksiazka = next((k for k in uzytkownik.wypozyczone_ksiazki if k.id_ksiazki == id_ksiazki), None)
        if not ksiazka:
            print(f"Książka o ID {id_ksiazki} nie została wypożyczona przez użytkownika {uzytkownik.imie}.")
            return

        ksiazka.wypozyczona = False
        ksiazka.data_zwrotu = None
        uzytkownik.wypozyczone_ksiazki.remove(ksiazka)
        print(f"Książka '{ksiazka.tytul}' została zwrócona.")

    def wyswietl_historie(self):
        # Wyświetlenie historii wypożyczeń
        if not self.historia:
            print("Brak historii wypożyczeń.")
            return
        for wpis in self.historia:
            print(f"{wpis['uzytkownik']} wypożyczył '{wpis['ksiazka']}' - Data: {wpis['data']}")

# Funkcja menu głównego programu
def menu():
    biblioteka = Biblioteka()

    while True:
        print("\nMenu Biblioteki:")
        print("1. Zarządzanie książkami")
        print("2. Zarządzanie użytkownikami")
        print("3. Wypożyczanie książek")
        print("4. Inne")
        print("5. Wyjdź")

        wybor = input("Wybierz opcję (1-5): ")

        if wybor == "1":
            # Podmenu zarządzania książkami
            while True:
                print("\nZarządzanie książkami:")
                print("1. Wyświetl książki")
                print("2. Dodaj książkę")
                print("3. Usuń książkę")
                print("4. Szukaj książki")
                print("5. Powrót do głównego menu")
                sub_wybor = input("Wybierz opcję (1-5): ")

                if sub_wybor == "1":
                    biblioteka.wyswietl_ksiazki()
                elif sub_wybor == "2":
                    tytul = input("Podaj tytuł książki: ")
                    autor = input("Podaj autora książki: ")
                    rok_wydania = input("Podaj rok wydania książki: ")
                    biblioteka.dodaj_ksiazke(tytul, autor, rok_wydania)
                elif sub_wybor == "3":
                    try:
                        id_ksiazki = int(input("Podaj ID książki do usunięcia: "))
                        biblioteka.usun_ksiazke(id_ksiazki)
                    except ValueError:
                        print("Podaj poprawne ID.")
                elif sub_wybor == "4":
                    kryterium = input("Wyszukiwanie po (tytul, autor, rok_wydania): ").lower()
                    wartosc = input(f"Podaj wartość dla {kryterium}: ")
                    biblioteka.szukaj_ksiazki(kryterium, wartosc)
                elif sub_wybor == "5":
                    break
                else:
                    print("Nieprawidłowy wybór. Spróbuj ponownie.")

        elif wybor == "2":
            # Podmenu zarządzania użytkownikami
            while True:
                print("\nZarządzanie użytkownikami:")
                print("1. Wyświetl użytkowników")
                print("2. Dodaj użytkownika")
                print("3. Powrót do głównego menu")
                sub_wybor = input("Wybierz opcję (1-3): ")

                if sub_wybor == "1":
                    biblioteka.wyswietl_uzytkownikow()
                elif sub_wybor == "2":
                    imie = input("Podaj imię użytkownika: ")
                    nazwisko = input("Podaj nazwisko użytkownika: ")
                    biblioteka.dodaj_uzytkownika(imie, nazwisko)
                elif sub_wybor == "3":
                    break
                else:
                    print("Nieprawidłowy wybór. Spróbuj ponownie.")

        elif wybor == "3":
            # Podmenu wypożyczania książek
            while True:
                print("\nWypożyczanie książek:")
                print("1. Wypożycz książkę")
                print("2. Zwróć książkę")
                print("3. Wyświetl historię wypożyczeń")
                print("4. Powrót do głównego menu")
                sub_wybor = input("Wybierz opcję (1-4): ")

                if sub_wybor == "1":
                    id_ksiazki = input("Podaj ID książki do wypożyczenia: ")
                    id_uzytkownika = input("Podaj ID użytkownika: ")
                    biblioteka.wypozycz_ksiazke(id_ksiazki, id_uzytkownika)
                elif sub_wybor == "2":
                    id_ksiazki = input("Podaj ID książki do zwrotu: ")
                    id_uzytkownika = input("Podaj ID użytkownika: ")
                    biblioteka.zwroc_ksiazke(id_ksiazki, id_uzytkownika)
                elif sub_wybor == "3":
                    biblioteka.wyswietl_historie()
                elif sub_wybor == "4":
                    break
                else:
                    print("Nieprawidłowy wybór. Spróbuj ponownie.")

        elif wybor == "4":
            # Podmenu inne opcje
            while True:
                print("\nInne:")
                print("1. Pomoc")
                print("2. O programie")
                print("3. Powrót do głównego menu")
                sub_wybor = input("Wybierz opcję (1-3): ")

                if sub_wybor == "1":
                    print("\nPomoc:")
                    print("1. Zarządzanie książkami - Otwiera podmenu do zarządzania książkami:")
                    print("   - Wyświetl książki: Pokazuje listę wszystkich książek w bibliotece.")
                    print("   - Dodaj książkę: Pozwala dodać nową książkę do biblioteki.")
                    print("   - Usuń książkę: Usuwa książkę z biblioteki na podstawie jej ID.")
                    print("   - Szukaj książki: Wyszukuje książki według tytułu, autora lub roku wydania.")
                    print("2. Zarządzanie użytkownikami - Otwiera podmenu do zarządzania użytkownikami:")
                    print("   - Wyświetl użytkowników: Pokazuje listę wszystkich użytkowników biblioteki.")
                    print("   - Dodaj użytkownika: Dodaje nowego użytkownika do biblioteki.")
                    print("3. Wypożyczanie książek - Otwiera podmenu do zarządzania wypożyczeniami:")
                    print("   - Wypożycz książkę: Pozwala użytkownikowi wypożyczyć książkę.")
                    print("   - Zwróć książkę: Pozwala użytkownikowi zwrócić książkę.")
                    print("   - Wyświetl historię wypożyczeń: Pokazuje historię wszystkich wypożyczeń książek.")
                    print("4. Inne - Otwiera podmenu z dodatkowymi opcjami:")
                    print("   - Pomoc: Wyświetla informacje o działaniu programu.")
                    print("   - O programie: Wyświetla informacje o celu i funkcjonalności programu.")
                    print("5. Wyjdź - Zapisuje dane i kończy działanie programu.")
                elif sub_wybor == "2":
                    print("\nO programie:")
                    print("Ten program to system zarządzania biblioteką. Umożliwia użytkownikom:")
                    print("- Dodawanie, usuwanie i wyszukiwanie książek w bibliotece.")
                    print("- Zarządzanie użytkownikami biblioteki i ich wypożyczonymi książkami.")
                    print("- Śledzenie wypożyczeń i zwrotów książek.")
                    print("- Wyświetlanie historii wszystkich transakcji związanych z książkami.")
                    print("Celem programu jest uproszczenie operacji bibliotecznych i zwiększenie efektywności.")
                elif sub_wybor == "3":
                    break
                else:
                    print("Nieprawidłowy wybór. Spróbuj ponownie.")

        elif wybor == "5":
            # Wyjście z programu
            biblioteka.zapisz_dane()
            print("Dane zostały zapisane. Do widzenia!")
            break
        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")

if __name__ == "__main__":
    menu()
