from itertools import combinations


def wczytaj_dane(nazwa_pliku):
    tabela = []

    with open(nazwa_pliku, "r") as plik:
        for linia in plik:
            if linia.strip():
                wiersz = list(map(int, linia.split()))
                tabela.append(wiersz)

    return tabela


def czy_wiersze_sprzeczne(w1, w2):
    atrybuty = w1[:-1] == w2[:-1]
    decyzje = w1[-1] != w2[-1]

    return atrybuty and decyzje


def znajdz_sprzecznosci(tabela):
    sprzeczne = set()

    for i in range(len(tabela)):
        for j in range(i + 1, len(tabela)):
            if czy_wiersze_sprzeczne(tabela[i], tabela[j]):
                sprzeczne.add(i)
                sprzeczne.add(j)

    return sprzeczne


def sprawdz_regule(tabela, warunek, decyzja):
    pasujace = []

    for indeks, wiersz in enumerate(tabela):

        if all(wiersz[i] == wartosc for i, wartosc in warunek):  # sprawdzanie czy pasuje do warunku

            if wiersz[-1] != decyzja:
                return None

            pasujace.append(indeks)

    return pasujace


def znajdz_regule_wiersza(tabela, indeks_wiersza, rzad):
    wiersz = tabela[indeks_wiersza]

    liczba_atrybutow = len(wiersz) - 1
    decyzja = wiersz[-1]

    for kombinacja in combinations(range(liczba_atrybutow), rzad):

        warunek = [(i, wiersz[i]) for i in kombinacja]

        pasujace = sprawdz_regule(tabela, warunek, decyzja)

        if pasujace:
            return {
                "wiersz": indeks_wiersza,
                "warunek": warunek,
                "decyzja": decyzja,
                "pasujace": pasujace
            }

    return None


def covering(tabela):
    liczba_atrybutow = len(tabela[0]) - 1

    sprzecznosci = znajdz_sprzecznosci(tabela)

    niepokryte = set(range(len(tabela))) - sprzecznosci

    wyniki = {}

    for rzad in range(1, liczba_atrybutow + 1):

        if not niepokryte:
            break

        reguly_rzedu = []

        for indeks in sorted(niepokryte):

            if indeks not in niepokryte:
                continue

            regula = znajdz_regule_wiersza(
                tabela,
                indeks,
                rzad
            )

            if regula:
                reguly_rzedu.append(regula)

                for i in regula["pasujace"]:
                    niepokryte.discard(i)

        if reguly_rzedu:
            wyniki[rzad] = reguly_rzedu

    return wyniki, sprzecznosci


def formatuj_warunek(warunek):
    return " ∧ ".join(
        f"(a{i + 1} = {wartosc})"
        for i, wartosc in warunek
    )


def drukuj_sprzecznosci(sprzecznosci):
    if sprzecznosci:
        lista = [i + 1 for i in sorted(sprzecznosci)]
        print(f"Wykluczono sprzeczności: {lista}\n")


def drukuj_reguly(wyniki):
    if not wyniki:
        print("Nie znaleziono żadnych reguł.")
        return

    for rzad in sorted(wyniki.keys()):

        print(f"Rząd {rzad}:")

        for regula in wyniki[rzad]:

            numer = regula["wiersz"] + 1
            warunek = formatuj_warunek(regula["warunek"])
            decyzja = regula["decyzja"]
            liczba = len(regula["pasujace"])

            dodatek = f" [{liczba}]" if liczba > 1 else ""

            print(
                f"z o{numer} {warunek} "
                f"⇒ (d = {decyzja}){dodatek}"
            )

        print()


def drukuj_wyniki(wyniki, sprzecznosci):
    drukuj_sprzecznosci(sprzecznosci)
    drukuj_reguly(wyniki)


def uruchomienie():
    tabela = wczytaj_dane("dane.txt")

    wyniki, sprzecznosci = covering(tabela)

    drukuj_wyniki(wyniki, sprzecznosci)


uruchomienie()
