koncept1 = []
koncept2 = []


def tab_print(tab):
    wynik = ""
    for element in tab:
        wynik += f"\t{element} \n"
    return wynik


def wczytanie_tabel():
    with open('tabela.txt', 'r') as file:
        tab =[]
        for i in file:
            row = [int(x) for x in i.split()]
            tab.append(row)
        for j in tab:
            if j[-1] == 1:
                koncept1.append(j)
            if j[-1] == 2:
                koncept2.append(j)


def dodawanie_wierszy(tab):
    ilosc = len(tab)
    wynik = []
    i = 0
    while i < ilosc:
       wynik.append(i)
       i = i + 1
    return wynik


def najczestszy_deskryptor(tab):
    wiersze_do_sprawdzenia = dodawanie_wierszy(tab)
    wybrane_wiersze = [tab[i] for i in wiersze_do_sprawdzenia]


wczytanie_tabel()
najczestszy_deskryptor(koncept1)
#print("Koncpet 1: \n", tab_print(koncept1), "Koncept 2:\n", tab_print(koncept2))
