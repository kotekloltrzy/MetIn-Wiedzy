tabela = []


def wczytanie_tabel():
    with open('tabela.txt', 'r') as file:
        tab =[]
        for i in file:
            row = [int(x) for x in i.split()]
            tab.append(row)
        for j in tab:
            tabela.append(j)


def drukowanie_tabel(tab):
    for i in tab:
        print(i)


def sprawdzanie_sprzecznosci(wiersz_sprawdzany, tabela_sprawdzana):
    ilosc_atrybutow = len(wiersz_sprawdzany)-1
    atrybut_decyzyjny = len(wiersz_sprawdzany) - 1
    reguly = []
    for i in tabela_sprawdzana:
        o = 1
        j = 0
        while j < ilosc_atrybutow:
            if wiersz_sprawdzany[j] == i[j] and wiersz_sprawdzany[atrybut_decyzyjny] == i[atrybut_decyzyjny]:
                reguly.append(f"z o{i} (a{j} = {i[j]}) => (d = {i[atrybut_decyzyjny]})")
                j = j + 1
                o = o + 1
                break
            j = j + 1
            o = o + 1
    drukowanie_tabel(reguly)


wczytanie_tabel()
drukowanie_tabel(tabela)
sprawdzanie_sprzecznosci(tabela[1], tabela)

