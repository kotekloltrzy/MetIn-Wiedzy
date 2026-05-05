import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use('TkAgg')


def wczytaj_dane(plik):
    temp1 = []
    temp2 = []
    with open(plik, "r") as f:
        for line in f:
            a, b = map(int, line.split())
            temp1.append(a)
            temp2.append(b)
    return temp1, temp2


def srednia_aryt(zbior):
    wynik = 0
    for i in zbior:
        wynik = wynik + i
    return wynik / len(zbior)


def odchyl_stand(zbior, srednia):
    wynik = 0
    for i in zbior:
        wynik = wynik + (i - srednia) ** 2
    wynik = wynik / (len(zbior)-1)
    wynik = wynik ** 0.5
    return round(wynik, 2)


def korelacja_pearsona(zbiorx, zbiory):
    licznik = 0
    sumax = sum(zbiorx)
    sumay = sum(zbiory)
    sumaxk = 0
    sumayk = 0
    n = len(zbiorx)
    i = 0
    while i < n:
        licznik = licznik + (zbiorx[i] * zbiory[i])
        i = i + 1
    licznik = ((n * licznik) - (sumax * sumay))
    for i in zbiorx:
        sumaxk = sumaxk + i**2
    for i in zbiory:
        sumayk = sumayk + i**2
    mianownik = ((n * sumaxk - sumax**2)*(n * sumayk - sumay**2)) ** 0.5
    return round(licznik/mianownik, 2)


def naj_pas_lin(Mx, My, Sx, Sy, r):
    b = round(r * (Sy/Sx), 3)
    a = round(My - (b * Mx), 3)
    return a, b


def wykres(dane_a, dane_b, dane_x, dane_y):
    temp_x = np.linspace(0, 5, 100)
    temp_y = dane_b * temp_x + dane_a
    plt.title("Regresja liniowa")
    plt.xlabel("Wartości X")
    plt.ylabel("Wartości Y")
    plt.plot(temp_x, temp_y, label=f'y = {dane_b}x + {dane_a}')
    plt.scatter(dane_x, dane_y, label="Wartości Niezależne", color='red')
    plt.legend()
    plt.show()


def przewidywanie(a, b, nowe_x):
    y_pred = b * nowe_x + a
    return round(y_pred, 2)


x, y = wczytaj_dane("dane.txt")


def uruchomienie_funckji(dane_x, dane_y, nowe_x=None):
    Mx = srednia_aryt(dane_x)
    My = srednia_aryt(dane_y)
    Sx = odchyl_stand(dane_x, Mx)
    Sy = odchyl_stand(dane_y, My)
    r = korelacja_pearsona(dane_x, dane_y)
    a, b = naj_pas_lin(Mx, My, Sx, Sy, r)
    wykres(a, b, dane_x, dane_y)
    if nowe_x is not None:
        y_pred = przewidywanie(a, b, nowe_x)
        print(f"Predykcja dla x = {nowe_x}: y = {y_pred}")


uruchomienie_funckji(x, y, nowe_x=6)
