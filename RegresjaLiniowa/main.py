import matplotlib.pyplot as plt
x = [1, 2, 3, 4, 5]
y = [4, 6, 9, 11, 18]


def srednia_aryt(zbior):
    wynik = 0
    for i in zbior:
        wynik = wynik + i
    return wynik / len(zbior)


Mx = srednia_aryt(x)
My = srednia_aryt(y)


def odchyl_stand(zbior, srednia):
    wynik = 0
    for i in zbior:
        wynik = wynik + (i - srednia) ** 2
    wynik = wynik / (len(zbior)-1)
    wynik = wynik ** 0.5
    return round(wynik, 2)


Sx = odchyl_stand(x, Mx)
Sy = odchyl_stand(y, My)


def korelacja_Pearsona(zbiorx, zbiory):
    licznik = 0
    mianownik = 0
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


r = korelacja_Pearsona(x, y)


def naj_pas_lin(Mx, My, Sx, Sy, r):
    b = round(r * (Sy/Sx), 3)
    a = round(My - (b * Mx), 3)
    return a, b


a, b = naj_pas_lin(Mx, My, Sx, Sy, r)


def funkcja(a, b):

    plt.title("Regresja liniowa")
    plt.xlabel("Wartości X")
    plt.ylabel("Wartości Y")