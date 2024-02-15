# Importation des bibliothèques
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Déclaration des constantes
MORT = 0
VIVANT = 1
TAILLE = 100
NB_GENERATION = 60
MODE_STANDARD = 0
MODE_NEURAL = 1
SCORE = 0

mode = MODE_STANDARD

# Initialisation du générateur de nombres aléatoires
# Doit assurer la reproductibilité
rnd = np.random.default_rng()#

while SCORE < 0.5 :
    # Générer 100 données avec 8 caractéristiques binaires et la caractéristique cible (somme des caractéristiques binaires)
    x_array = list()
    y_array = list()
    for _ in range(0,100) :
        new_array = rnd.integers(low=0, high=2, size=8)     #Creer un array de 8, avec des nombres aleatoire entre 0 et 1 pour les features(X)
        x_array.append(new_array)
        y = 0
        for i in new_array :    #Calculer le nombre de 1 dans la nouvelle array pour les labels(Y)
            if i == 1 :
                y = y + 1
        y_array.append(y)

    #for i in range(0,100) :
    #    print(x_array[i])
    #    print(y_array[i])

    # Diviser les données en ensembles d'entraînement et de test (X_train, X_test, Y_train, Y_test)
    # 80% pour l'entraînement et 20% pour les tests.
    # Assurer la reproductibilité
    X_train, X_test, y_train, y_test = train_test_split(x_array, y_array, train_size=0.8, test_size=0.2, shuffle=True)

    #print("Format des données d'entrainement")
    #print(X_train)
    #print(y_train)
    #print("Format des données test")
    #print(X_test)
    #print(y_test)

    # Créer le modèle MLPRegressor nommé mlp, 1 couche cachée avec 8 neurones. Reproductible, Maximum 1000 itérations d'apprentissage.
    mlp = MLPRegressor(hidden_layer_sizes=1, solver='lbfgs', max_iter=1000, learning_rate_init=0.0001)

    # Entraîner le modèle sur les données d'entraînement
    mlp.fit(X_train,y_train)

    # Faire des prédictions sur les données de test.
    print(mlp.predict(X_test))

    # Calculer et afficher l'erreur quadratique moyenne (MSE) et coefficient de détermination R^2 (le score)
    SCORE = mlp.score(X_test,y_test)
    print(SCORE)

# Tester individuellement le model avec .predict.
# Le paramètre est un tableau 2 dimensions qui contient 1 ligne, et 8 caractéristiques valant 0 ou 1.
# Le résultat doit donner une bonne approximation du nombre de voisins.
#print(mlp.predict([[0,0,0,0,0,0,0,0]]))
#print(mlp.predict([[0,0,1,0,0,0,0,0]]))
#print(mlp.predict([[0,0,0,1,0,1,0,0]]))
#print(mlp.predict([[0,1,0,1,1,0,0,0]]))
#print(mlp.predict([[1,0,1,0,1,0,1,0]]))
#print(mlp.predict([[0,1,1,0,1,1,1,0]]))
#print(mlp.predict([[1,1,0,1,1,1,0,1]]))
#print(mlp.predict([[1,1,1,1,0,1,1,1]]))
#print(mlp.predict([[1,1,1,1,1,1,1,1]]))

#############################################################################
grille  = [[0,0,0,0,0,0,1,0,0,0,0,0,0],
           [0,0,0,0,0,0,1,0,0,0,0,0,0],
           [0,0,0,0,1,1,0,1,1,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,1,0,1,0,0,0,1,0,1,0,0],
           [0,0,1,0,0,0,0,0,0,0,1,0,0],
           [1,1,0,0,0,0,0,0,0,0,0,1,1],
           [0,0,1,0,0,0,0,0,0,0,1,0,0],
           [0,0,1,0,1,0,0,0,1,0,1,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,1,1,0,1,1,0,0,0,0],
           [0,0,0,0,0,0,1,0,0,0,0,0,0],
           [0,0,0,0,0,0,1,0,0,0,0,0,0]
           ]

#Afficher la grille de base
fig, ax = plt.subplots()
im = plt.imshow(grille, cmap = 'gray_r')

def voisin_mlp(i, j) :
    global grille
    nb_voisin = 0
    new_array = list()
    positionVoisin = [[-1,-1],[0,-1],[1,-1],
                      [-1,0],        [1,0],
                      [-1,1], [0,1] ,[1,1]]
    for iCtr, jCtr in positionVoisin :
        mi = iCtr
        mj = jCtr
        ni = i + mi
        nj = j + mj
        if 0 <= ni < len(grille) and 0 <= nj < len(grille[0]) : #Creer une nouvelle array pour faire predir
            new_array.append(grille[ni][nj])
        else :
            new_array.append(0)

    #print(new_array)
    nb_voisin = mlp.predict([new_array])
    #print(nb_voisin)
    nb_voisin = np.round(nb_voisin)
    #print(nb_voisin)
    return nb_voisin

#Générer la nouvelle grille selon la fonction voisin(i,j)
def generation_suivante(old_grille) :
    global grille
    new_grille = old_grille
    for iCtr in range(len(grille)) :
        for jCtr in range(len(grille[0])) :
            print("------\nAncienne valeur:" + str(new_grille[iCtr][jCtr]))
            print("[" + str(iCtr) + "][" + str(jCtr) + "] voisin:" + str(voisin_mlp(iCtr,jCtr)))
            nb_voisin = voisin_mlp(iCtr,jCtr)
            position = grille[iCtr][jCtr]
            if position == 1 :
                if nb_voisin < 2 or nb_voisin > 3 :
                    new_grille[iCtr][jCtr] = 0
                else :
                    new_grille[iCtr][jCtr] = 1
            if position == 0 :
                if nb_voisin == 3 :
                    new_grille[iCtr][jCtr] = 1
                else :
                    new_grille[iCtr][jCtr] = 0
            print("Nouvelle valeur:" + str(new_grille[iCtr][jCtr]))
    grille = new_grille
    return grille

# Fonction d'initialisation de l'animation
def init():
    im.set_data(grille)
    return [im]

# Fonction de la mise à jour de l'animation
def update(frames):
    global grille
    # Récupère les données
    old_grille = im.get_array()
    # calcule la génération suivante
    grille = generation_suivante(old_grille)
    # Réassigne les nouvelles données
    im.set_array(grille)
    return [im]

# Fonction d'animation
# np.linspace(debut, fin, num=nombre_de_division_dans_le_vecteur): Produit un vecteur sur le nombre de frame
ani = animation.FuncAnimation(fig, update, init_func=init, frames=np.linspace(0, NB_GENERATION, num=NB_GENERATION), interval=1000)
#ani = animation.FuncAnimation(fig, update, init_func=init,  interval=100)

plt.show()
