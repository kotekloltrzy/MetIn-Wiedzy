from itertools import combinations


def read_table(filename):
    table = []
    with open(filename, "r") as f:
        for line in f:
            if line.strip():
                row = list(map(int, line.split()))
                table.append(row)
    return table


def sprzwdzanie_sprzecznosci(table):
    sprzeczne = set()
    wiersze = len(table)
    for i in range(wiersze):
        for j in range(i + 1, wiersze):
            if table[i][:-1] == table[j][:-1]:
                if table[i][-1] != table[j][-1]:
                    sprzeczne.add(i)
                    sprzeczne.add(j)
    return sprzeczne


def sequential_covering(table):
    atrybut_decyzyjny = len(table[0]) - 1
    wiersze = len(table)
    sprzeczneosci = sprzwdzanie_sprzecznosci(table)
    do_sprawdzenia = set(range(wiersze)) - sprzeczneosci
    wyniki = {}
    for r in range(1, atrybut_decyzyjny + 1):
        if not do_sprawdzenia:
            break
        temp_wyniki = []
        temp_do_sprawdzenia = sorted(list(do_sprawdzenia))
        for index in temp_do_sprawdzenia:
            if index not in do_sprawdzenia:
                continue
            wiersz = table[index]
            decyzja = wiersz[-1]
            dobra_regula = None
            for comb in combinations(range(atrybut_decyzyjny), r):
                cond = tuple(sorted([(i, wiersz[i]) for i in comb]))
                sprawdzone = []
                conflict = False
                for j, other in enumerate(table):
                    if all(other[i] == v for i, v in cond):
                        if other[-1] != decyzja:
                            conflict = True
                            break
                        sprawdzone.append(j)
                if not conflict and len(sprawdzone) > 0:
                    dobra_regula = (index, list(cond), decyzja, sprawdzone)
                    break
            if dobra_regula:
                temp_wyniki.append(dobra_regula)
                for idx in dobra_regula[3]:
                    do_sprawdzenia.discard(idx)
        if temp_wyniki:
            wyniki[r] = temp_wyniki
    return wyniki, sprzeczneosci


def drukuj_wynik(wyniki, sprzecznosci):
    if sprzecznosci:
        print(f"Wykluczono sprzeczności: {[i + 1 for i in sorted(list(sprzecznosci))]}\n")
    if not wyniki:
        print("Nie znaleziono żadnych reguł.")
        return
    for r in sorted(wyniki.keys()):
        print(f"Rząd {r}:")
        for index, cond, decyzja, sprawdzone in wyniki[r]:
            name = f"o{index + 1}"
            cond_str = " ∧ ".join([f"(a{i + 1} = {v})" for i, v in cond])
            ilosc = f" [{len(sprawdzone)}]" if len(sprawdzone) > 1 else ""
            print(f"z {name} {cond_str} ⇒ (d = {decyzja}){ilosc}")
        print()


data = read_table("dane.txt")
wynik, sprzecznosc = sequential_covering(data)
drukuj_wynik(wynik, sprzecznosc)
