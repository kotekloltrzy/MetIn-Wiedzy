files = {
    "setosa": open("setosa.data", "w"),
    "versicolor": open("setosa.data", "w"),
    "virginica": open("setosa.data", "w")
}


def tworzenie_plikow(filename):
    with open(filename) as infile, \
            open("setosa.data", "w") as setosa, \
            open("versicolor.data", "w") as versicolor, \
            open("virginica.data", "w") as virginica:
        for line in infile:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) != 5:
                continue
            label = parts[4].strip()

            if label == "Iris-setosa":
                setosa.write(line + "\n")
            elif label == "Iris-versicolor":
                versicolor.write(line + "\n")
            elif label == "Iris-virginica":
                virginica.write(line + "\n")
            else:
                print("Nieznana etykieta:", repr(label))


def wczytanie_danych(filename):
    data = []
    with open(filename) as f:
        for line in f:
            parts = line.strip().split(",")
            features = list(map(float, parts[:4]))
            data.append(features)
    return data


def mean(values):
    return sum(values)/len(values)


def std(values, m):
    variance = sum((x - m) ** 2 for x in values) / len(values)
    return variance ** 0.5


def summarize(data):
    summaries = []
    for col in zip(*data):
        m = mean(col)
        s = std(col, m)
        summaries.append((m, s))
    return summaries


setosa_data = wczytanie_danych("setosa.data")
versicolor_data = wczytanie_danych("versicolor.data")
virginica_data = wczytanie_danych("virginica.data")

model = {
    "setosa": summarize(setosa_data),
    "versicolor": summarize(versicolor_data),
    "virginica": summarize(virginica_data),
}


def gauss(x, m, s):
    if s == 0:
        return 1.0 if x == m else 0.0

    expo = 2.718 ** (-((x-m) ** 2) / (2 * s ** 2))
    return (1/((2 * 3.14) ** 0.5 * std)) * expo


def prawdopodobienstwo(mod, wektor):
    probs = {}
    for class_name, summaries in mod.items():
        probs[class_name] = 1
        for i in range(len(summaries)):
            m, s = summaries[i]
            x = wektor[i]
            probs[class_name] *= gauss(x, m, s)
    return probs


def predict(mod, wektor):
    probs = prawdopodobienstwo(mod, wektor)
    return max(probs, key=probs.get)


sample = [5.1, 3.5, 1.4, 0.2]
print("Przewidywana klasa:", predict(model, sample))

tworzenie_plikow("iris.data")
