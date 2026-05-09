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


def entropia(tabela):
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
    return wyniki


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


def sortuj_gainy(tabela):
    kolumny = list(tabela[0].keys())
    wyniki_gain = []

    for i in range(1, len(kolumny) - 1):
        nazwa = kolumny[i]
        ent_kon = entropia_konkretna(tabela, i)
        wynik = gain(tabela, ent_kon)

        wyniki_gain.append({
            "wartość": nazwa,
            "gain": wynik["Gain"]
        })

    return sorted(wyniki_gain, key=lambda x: x["gain"], reverse=True)


def tworzenie_drzewa(tabela):
    sorted_gains = sortuj_gainy(tabela)
    najlepsza = sorted_gains[0]["wartość"]
    drzewo = {najlepsza: {}}
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
            drzewo[najlepsza][wartosc] = tworzenie_drzewa(podzbior)

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
