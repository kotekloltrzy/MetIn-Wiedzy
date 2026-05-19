def wczytanie_danych(nazwa_pliku):
    tabela = []
    with open(nazwa_pliku, "r") as plik:
        for linia in plik:
            dane = linia.strip().split()
            obiekt = {"id": dane[0]}
            for i, wartosc in enumerate(dane[1:-1], start=1):
                obiekt[f"a{i}"] = int(wartosc)
            obiekt["d"] = int(dane[-1])
            tabela.append(obiekt)
    return tabela


dane_tabeli = wczytanie_danych("dane.txt")
atrybuty = [element for element in dane_tabeli[0].keys() if element not in ["id", "d"]]


def spelnia(obiekt, regula):  # sprawdzamy czy obiekt spełnia podaną regułę
    for (atr, value) in regula:
        if obiekt[atr] != value:
            return False
    return True


def sprzeczna(regula, decyzja, tabela):  # sprzeczne gdy warunki takie same ale decyzja inna
    for obiekt in tabela:
        if spelnia(obiekt, regula):
            if obiekt["d"] != decyzja:
                return True

    return False


def wybierz_najlepszy(aktualne, regula):  # wybieramy warunek o najwiekszym pokryciu
    najlepszy = None
    max_pokrycie = -1  # ile obiektów spełnia najlepszy warunek
    for atr in atrybuty:
        wartosci = set(o[atr] for o in aktualne)
        for value in wartosci:
            warunek = (atr, value)
            if warunek in regula:
                continue
            pokrycie = 0  # ile obiektów spełnia warunek
            for obiekt in aktualne:
                if obiekt[atr] == value:
                    pokrycie += 1
            if pokrycie > max_pokrycie:
                max_pokrycie = pokrycie
                najlepszy = warunek

    return najlepszy


def usun_pokryte(niepokryte, regula):  # usuwanie spełniających reguły obiektów
    wynik = []
    for obiekt in niepokryte:
        if not spelnia(obiekt, regula):
            wynik.append(obiekt)
    return wynik


def lem2(tabela):
    zasady = []  # lista słowników {reguła: [lista warunków], decyzja: atrybut decyzyjny}
    decyzje = set(o["d"] for o in tabela)
    for decyzja in decyzje:
        niepokryte = [o for o in tabela if o["d"] == decyzja]
        while len(niepokryte) > 0:
            regula = []  # lista warunków: [("a1", 2), ("a3", 1)] oznacza to że atrybut a1 musi wynosić 2 oraz a3 == 1
            aktualne = niepokryte.copy()
            while sprzeczna(regula, decyzja, tabela):  # dopóki reguła jest sprzeczna szukamy kolejnych warunków
                najlepszy = wybierz_najlepszy(aktualne, regula)
                regula.append(najlepszy)
                # zostawiamy tylko obiekty które speniają nowe warunki
                aktualne = [o for o in aktualne if o[najlepszy[0]] == najlepszy[1]]
            zasady.append({"regula": regula, "decyzja": decyzja})  # dodajemy do zasad zbiór regułę jako zbiór warunków
            niepokryte = usun_pokryte(niepokryte, regula)
    return zasady


def policz_support(regula, decyzja, tabela):  # dla każdej reguły sprawdza ile razy jest spełniona
    licznik = 0
    for obiekt in tabela:
        if spelnia(obiekt, regula):
            if obiekt["d"] == decyzja:
                licznik += 1
    return licznik


def wypisz_reguly(zasady, tabela):
    for i, r in enumerate(zasady):
        warunki = []
        for (atr, value) in r["regula"]:
            warunki.append(f"({atr} = {value})")
        lewa = " ∧ ".join(warunki)
        decyzja = r["decyzja"]
        support = policz_support(r["regula"], decyzja, tabela)
        prawa = f"(d = {decyzja})"
        if support > 1:
            prawa += f"[{support}]"
        print(f"rule{i+1} {lewa} => {prawa}")


reguly = lem2(dane_tabeli)
wypisz_reguly(reguly, dane_tabeli)
