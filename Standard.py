import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np 

# Déclaration des constantes
MORT = 0
VIVANT = 1
TAILLE = 100
NB_GENERATION = 60
MODE_STANDARD = 0
MODE_NEURAL = 1

mode = MODE_STANDARD

# Est ce que la grille doit être 100 x 100? Est ce qu'on doit utiliser un array, doit-on considérer que les cases en bordures compte l'autres côté?
#Doit-on générer aléatoirement les cases?
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

#Calculer le nombre de case adjacente vivante 
def voisin(i,j):
    global grille
    nb_voisin = 0
    positionVoisin = [[-1,-1],[0,-1],[1,-1],
                      [-1,0],        [1,0],
                      [-1,1], [0,1] ,[1,1]]
    for iCtr, jCtr in positionVoisin :
        mi = iCtr
        mj = jCtr
        ni = i + mi
        nj = j + mj
        if 0 <= ni < len(grille) and 0 <= nj < len(grille[0]) :
            #print(ni , nj, grille[ni][nj])
            if grille[ni][nj] == 1 :
                nb_voisin += 1
    return nb_voisin

#Générer la nouvelle grille selon la fonction voisin(i,j)
def generation_suivante(old_grille) :
    global grille
    new_grille = old_grille
    for iCtr in range(len(grille)) :
        for jCtr in range(len(grille[0])) :
            print("------\nAncienne valeur:" + str(new_grille[iCtr][jCtr]))
            print("[" + str(iCtr) + "][" + str(jCtr) + "] voisin:" + str(voisin(iCtr,jCtr)))
            nb_voisin = voisin(iCtr,jCtr)
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

#while True:
#    grille = generation_suivante()
#    plt.imshow(grille, cmap = 'gray_r')
#    plt.show()

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