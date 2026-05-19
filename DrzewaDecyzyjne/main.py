import math


def wczytanie_danych(plik):
    tabela = []
    with open(plik, "r", encoding="utf-8") as plik:
        kolumny = plik.readline().split()
        for linia in plik:
            dane = linia.split()
            wiersz = dict(zip(kolumny, dane))
            tabela.append(wiersz)

    return tabela


dane_tabeli = wczytanie_danych("dane.txt")


def entropia(tabela):  # ile jak "Tak" ile jest "Nie" i obliczanie entropii
    pozytywne = 0
    negatywne = 0
    wszystkie = len(tabela)
    for wiersz in tabela:
        if list(wiersz.values())[-1] == "Tak":
            pozytywne += 1
        else:
            negatywne += 1
    pp = pozytywne/wszystkie
    pn = negatywne/wszystkie
    e = 0
    if pp > 0:
        e -= pp * math.log(pp, 2)
    if pn > 0:
        e -= pn * math.log(pn, 2)
    return round(e, 3)


def entropia_konkretna(tabela, kolumna):  # funkcja moze przyjmowac wartosc kolumna jako int lub jako str
    wyniki = {}

    kolumny = list(tabela[0].keys())
    if isinstance(kolumna, str):
        if kolumna in kolumny:
            kolumna = kolumny.index(kolumna)
        else:
            raise ValueError(f"Nie istnieje kolumna: {kolumna}")

    for wiersz in tabela:
        wartosc = list(wiersz.values())[kolumna]
        decyzja = list(wiersz.values())[-1]

        if wartosc not in wyniki:
            wyniki[wartosc] = [0, 0]  # [Tak, Nie]

        if decyzja == "Tak":
            wyniki[wartosc][0] += 1
        else:
            wyniki[wartosc][1] += 1

    for i in wyniki:
        p = wyniki[i][0]
        n = wyniki[i][1]
        w = p + n
        pp = p / w
        pn = n / w
        e = 0

        if pp > 0:
            e -= pp * math.log(pp, 2)
        if pn > 0:
            e -= pn * math.log(pn, 2)

        wyniki[i].append(round(e, 3))
    return wyniki  # zwraca słownik {nazwa: [ilość "Tak", ilość "Nie", gain}


def gain(tabela, wartosc):
    ent_og = entropia(tabela)
    suma = 0

    for i in wartosc:
        p = wartosc[i][0]
        n = wartosc[i][1]
        e = wartosc[i][2]

        w = p + n

        suma += (w / len(tabela)) * e
    wartosc.update({"Gain": round(ent_og - suma, 3)})
    return wartosc


def sortuj_gainy(tabela, uzyte_kolumny=None):  # sprawdzanie gainow i zwracanie posortowanej listy
    if uzyte_kolumny is None:
        uzyte_kolumny = []

    kolumny = list(tabela[0].keys())
    wyniki_gain = []

    for i in range(1, len(kolumny) - 1):  # pomijamy dzień i decyzje
        nazwa = kolumny[i]

        ent_kon = entropia_konkretna(tabela, i)
        wynik = gain(tabela, ent_kon)  # obliczanie gaina

        gain_wartosc = wynik["Gain"]

        if nazwa in uzyte_kolumny:  # jeżeli kolumna była wykorzystana to ustawia gain na 0
            gain_wartosc = 0

        wyniki_gain.append({
            "wartość": nazwa,
            "gain": gain_wartosc
        })

    return sorted(wyniki_gain, key=lambda x: x["gain"], reverse=True)


def tworzenie_drzewa(tabela, uzyte_kolumny=None):
    if uzyte_kolumny is None:
        uzyte_kolumny = []

    sorted_gains = sortuj_gainy(tabela, uzyte_kolumny)
    if sorted_gains[0]["gain"] == 0:  # gdy gain wynosi 0 to jest decyzja większościowa
        tak = 0
        nie = 0
        for wiersz in tabela:
            if list(wiersz.values())[-1] == "Tak":
                tak += 1
            else:
                nie += 1
        return "Tak" if tak >= nie else "Nie"

    najlepsza = sorted_gains[0]["wartość"]
    uzyte_kolumny.append(najlepsza)  # kolumny mogą być użyte tylko raz
    drzewo = {najlepsza: {}}  # zaczynamy tworzyc drzewo
    temp = entropia_konkretna(tabela, najlepsza)

    for wartosc in temp:
        podzbior = []
        for wiersz in tabela:
            if wiersz[najlepsza] == wartosc:
                nowy = wiersz.copy()
                del nowy[najlepsza]
                podzbior.append(nowy)

        tak = temp[wartosc][0]
        nie = temp[wartosc][1]

        if tak == 0:
            drzewo[najlepsza][wartosc] = "Nie"

        elif nie == 0:
            drzewo[najlepsza][wartosc] = "Tak"
        else:
            # rekurencyjnie powtarzamy do utrzymania całego drzewa
            drzewo[najlepsza][wartosc] = tworzenie_drzewa(podzbior, uzyte_kolumny)
    return drzewo


def drukowanie_drzewa(drzewo, sciezka=""):
    for cecha, galezie in drzewo.items():
        for wartosc, wynik in galezie.items():
            if sciezka:
                nowa_sciezka = sciezka + " ∧ " + f"{cecha}({wartosc})"
            else:
                nowa_sciezka = f"{cecha}({wartosc})"
            if isinstance(wynik, str):
                print(nowa_sciezka + " => " + wynik)
            else:
                drukowanie_drzewa(wynik, nowa_sciezka)


drukowanie_drzewa(tworzenie_drzewa(dane_tabeli))
