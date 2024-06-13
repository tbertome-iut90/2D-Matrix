import numpy as np

Mdegueu = np.array([[3, 1, 2],
                    [-1, 4, 6],
                    [2, 8, 7]])

valeurs_propres, vecteurs_propres = np.linalg.eig(Mdegueu)

print("valeurs propres : ", valeurs_propres)
print("vecteurs propres : ", vecteurs_propres)

Mbb = np.array([[0.0]*3]*3)

for i in range(3):
    Mbb[i,i] = valeurs_propres[i]

print(Mbb)

P = np.array([[0.0]*3]*3)

for i in range(3):
    for j in range(3):
        P[i,j] = vecteurs_propres[j,i]

print(P)

Mcan = np.dot(np.dot(P, Mbb), np.linalg.inv(P))

print(Mcan)