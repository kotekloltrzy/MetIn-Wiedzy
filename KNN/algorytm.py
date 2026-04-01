tabela = []


def wczytanie_danych():
    with open('australian.csv', 'r') as file:
        temp = []
        for i in file:
            row = [float(x) for x in i.split()]
            temp.append(row)
    return temp


print(wczytanie_danych())

