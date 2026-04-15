from itertools import combinations


def wczytanie_tabel():
    tab = []
    with open('tabela.txt', 'r') as file:
        for line in file:
            row = [int(x) for x in line.split()]
            tab.append(row)
        return tab


def drukuj(tab):
    for i in tab:
        print(i)


def generuj_warunki(wiersz):
    atrybuty = [(i, wiersz[i]) for i in range(len(wiersz)-1)]
    warunki = []
    for r in range(1, len(atrybuty)+1):
        for comb in combinations(atrybuty,r):
            warunki.append(comb)
    return warunki


def pokrywanie(regula, rekord):
    for (i, j) in regula:
        if rekord[i] != j:
            return False
    return True


def ocen_regule(regula, tab, decyzja):
    TP = 0
    FP = 0
    for i in tabela:
        if pokrywanie(regula, i):
            if i[-1] == decyzja:
                TP += 1
            else:
                FP += 1
    if TP + FP == 0:
        return 0
    return TP/(TP+FP)


def najlepsza_regula(tab):
    najlepsza = None
    najlepsza_ocena = 0
    for wiersz in tab:
        decyzja = wiersz[-1]
        warunki = generuj_warunki(wiersz)
        for reg in warunki:
            ocena = ocen_regule(reg, tab, decyzja)
            if ocena > najlepsza_ocena:
                najlepsza_ocena = ocena
                najlepsza = (reg, decyzja)
    return najlepsza


def sequential_covering(tab):
    dane = tabela.copy()
    reguly = []
    while len(dane)>0:
        wynik = najlepsza_regula(dane)
        if wynik is None:
            break
        regula, decyzja = wynik
        reguly.append((regula, decyzja))
        nowe = []
        for r in dane:
            if not pokrywanie(regula, r):
                nowe.append(r)
        dane = nowe
    return reguly


tabela = wczytanie_tabel()
drukuj(tabela)


