import random
import math


def wczytaj_plik(nazwa):
    temp = []
    with open(nazwa, "r") as file:
        for wiersz in file:
            element = [float(x) for x in wiersz.strip().split()]
            temp.append(element)
    random.shuffle(temp)
    return temp


def podzial(dane):
    n = len(dane)
    ilosc = n // 6
    extra = n % 6
    wynik = []
    start = 0
    for i in range(6):
        size = ilosc
        if i < extra:
            size += 1
        wynik.append(dane[start:start+size])
        start += size

    return wynik


def six_fold(dane, ktory=0):  # wybieramy jeden z sześciu zbiorów jako testowy a resztę jako treningowy
    testowy = dane[ktory]
    treningowy = []
    for i in range(6):
        if i != ktory:
            treningowy.extend(dane[i])
    return testowy, treningowy


def srednia_odchylenie(tren):
    liczba_kolumn = len(tren[0]) - 1  # nie liczymy decyzji
    srednie = []
    odchylenia = []
    for i in range(liczba_kolumn):
        kolumna = [wiersz[i] for wiersz in tren]
        srednia = sum(kolumna) / len(kolumna)  # średnia = suma elementów / ilość elementów
        suma = 0
        for j in kolumna:
            suma += (j - srednia) ** 2  # suma wszystkich wartości kolumny - średnia do potęgi 2
        odchylenie = math.sqrt(suma / len(kolumna))  # podzielić na ilość elementów pod pierwiatskiem
        srednie.append(srednia)    # dodanie poszczególnej średniej kolumny do listy
        odchylenia.append(odchylenie)  # dodanie poszczególnego odchylenia kolumny do listy
    return srednie, odchylenia


def skalowanie(dane, srednie, odchylenia):
    wynik = []
    for wiersz in dane:
        temp = []
        for i in range(len(srednie)):
            if odchylenia[i] == 0:  # nie dzielimy przez 0
                temp.append(0.0)
            else:
                temp.append((wiersz[i] - srednie[i]) / odchylenia[i])  # element - średnia / odchylenie
        temp.append(wiersz[-1])  # pomijamy kolumnę z klasą decyzyjną
        wynik.append(temp)
    return wynik


def sigma(x):
    return 1.0 / (1.0 + math.exp(-x))  # funkcja sigmoidalna - zmiana wyniku na prawdopodobieństwo


def trenowanie(tren, uczenie=0.01, ile=100):
    liczba_cech = len(tren[0]) - 1
    wagi = [0.0] * liczba_cech
    bias = 0.0
    n = len(tren)
    for i in range(ile):  # 100 razy trening
        grad_wag = [0.0] * liczba_cech
        grad_bias = 0.0
        for probka in tren:
            x = probka[:-1]
            y = probka[-1]
            # Krok a)  bias + wszystkie elementy * ich waga
            z = bias
            for j in range(liczba_cech):
                z += wagi[j] * x[j]
            # Krok b) prawdopodobieństwo
            y_dwa = sigma(z)
            # Krok c) błąd
            error = y_dwa - y
            # Krok d) gradient wag
            for j in range(liczba_cech):
                grad_wag[j] += error * x[j]
            # Krok e) gradient biasu
            grad_bias += error
        # Krok f) uśrednienie gradientu wag
        for j in range(liczba_cech):
            grad_wag[j] /= n
        grad_bias /= n
        # Krok g) aktualizacja wag
        for j in range(liczba_cech):
            wagi[j] -= uczenie * grad_wag[j]
        # Krok h) aktualizacja biasu
        bias -= uczenie * grad_bias
    # po 100 treningach mamy wynik
    return wagi, bias


def testowanie(test, wagi, bias):
    poprawnie = 0
    tp = 0  # true positive
    tn = 0  # true negative
    fp = 0  # false positive
    fn = 0  # false negative
    for probka in test:
        x = probka[:-1]
        y = probka[-1]
        # bias + elementy * waga
        z = bias
        for j in range(len(wagi)):
            z += wagi[j] * x[j]
        # prawdopodobieństwo
        y_dwa = sigma(z)
        # zamiana na klasę
        if y_dwa >= 0.5:
            pred = 1
        else:
            pred = 0
        # sprawdzanie poprawności
        if pred == y:
            poprawnie += 1
        # macierz pomyłek
        if pred == 1 and y == 1:
            tp += 1
        elif pred == 0 and y == 0:
            tn += 1
        elif pred == 1 and y == 0:
            fp += 1
        elif pred == 0 and y == 1:
            fn += 1
    accuracy = round(poprawnie / len(test), 3)
    return accuracy, tp, tn, fp, fn


def uruchom():
    dane_pliku = wczytaj_plik("australian 1.csv")
    foldy = podzial(dane_pliku)
    accuracy_wszystkie = []
    for fold in range(6):
        testowy, treningowy = six_fold(foldy, fold)  # podzial na zbiór testowy i treningowy
        srednie, odchylenia = srednia_odchylenie(treningowy)  # obliczanie średniej i odchylenia standardowego
        treningowy = skalowanie(treningowy, srednie, odchylenia)  # skalujemy trening
        testowy = skalowanie(testowy, srednie, odchylenia)  # skalujemy test tymi samymi wartościami co trening
        wagi, bias = trenowanie(treningowy, uczenie=0.01, ile=100)  # trenowanie modelu
        accuracy, tp, tn, fp, fn = testowanie(testowy, wagi, bias)  # testowanie i wyciąganie accuracy
        accuracy_wszystkie.append(accuracy)
        print(f"\n{'=========================================================='}")
        print(f"FOLD {fold + 1}")
        print(f"Accuracy = {accuracy:}")
        print("\nMacierz pomyłek:")
        print(f"TP: {tp}      TN: {tn}")
        print(f"FP: {fp}      FN: {fn}")
    srednie_accuracy = round((sum(accuracy_wszystkie) / len(accuracy_wszystkie)), 3)
    print(f"Średnie accuracy = {srednie_accuracy}")



uruchom()
