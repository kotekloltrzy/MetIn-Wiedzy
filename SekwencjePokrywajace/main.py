from itertools import combinations

tabela = [[7, 2, 3], [3, 3, 5], [10, 45, 4]]
d = [1, 2, 1]

for i in combinations(tabela, 2):
    for j in combinations(i, 2):
        print(j)