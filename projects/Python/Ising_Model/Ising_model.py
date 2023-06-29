import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation 


class Ising:



    def __init__(self,N,J,KbT,nIteration,titre):
        """
        Initialise la simulation avec les conditions de départ
        """
        self.titre = titre
        self.N =N
        self.grille = np.empty([N,N])
        self.J = J
        self.nIteration = nIteration
        self.KbT = KbT
        
        #creation des listes de données stockant les valeurs d'énergie
        #et de magnétisation
        self.listE = []
        self.listM = []

        # definit la color map pour les graphiques
        self.color_map = {1: np.array([200, 0, 200]), 
                         -1.0: np.array([0,0, 100])}
        # creer un array avec les memes dimension de la grille avec 3 composant (RGB) pour chaque point
        self.grille_3d = np.ndarray(shape=(self.grille.shape[0], self.grille.shape[1], 3), dtype=int)
                
        self.RemplirGrille()
        
        
        

    def Run(self):     
        
        
        self.CalculEnergieInit()
        
        self.creerGraphDynamique(self.grille)
        
        for i in range(self.nIteration):                
            self.ChangementSpin()            
            
                
    def RemplirGrille(self):
        """
        Rempli la grille aléatoirement de 1 ou de -1
        """
        nb1 = 0
        nb2 = 0
        for i in range(self.N):
            for j in range(self.N):                
                self.grille[i,j] = [-1,1][np.random.randint(2)]
                if self.grille[i,j]==-1:
                    nb1 += 1
                else:
                    nb2 += 1

        
               
        

    def CalculEnergieInit(self):
        """
        Calculer l'énergie initiale pour le système entier
        Pour ne pas calculer chaque pair plus d'une fois,
        on va boucler seulement sur les combinaison de x et y pair :
        
                    (0,0)   X   (0,2)   X   ...
                      X   (1,1)   X   (1,3) ...
                    (2,0)   X   (2,2)   X   ...
                      X   (3,1)   X   (3,3) ...  
                     ...   ...   ...   ...  ...
                     
        """
        somme = 0
        for i in range(self.N):
            for j in range(self.N):
                if i+j % 2 == 0:
                    somme += self.CalculEnergie1Point(i,j,self.grille)

                    

        self.energy = -self.J*somme

        
        self.listE.append(self.energy)
        self.listM.append(self.CalculMagnetization())

        
        
    def CalculEnergie1Point(self,i,j,grille):
        """
        Calcul l'énergie des pairs autour d'un points avec les execptions pour les cotés de la grille
        """

        energie = 0
        
        if i-1 >= 0:
            energie += grille[i,j] * grille[i-1,j]
        if i+1 < self.N:
            energie += grille[i,j] * grille[i+1,j]
        if j-1 >= 0:
            energie += grille[i,j] * grille[i,j-1]
        if j+1 < self.N:
            energie += grille[i,j] * grille[i,j+1]

        return energie
    

    def CalculMagnetization(self):
        """
        Calcul la magnétization totale
        """
        magnetization = 0
        for i in range(self.N):
            for j in range(self.N):
                magnetization += self.grille[i,j]
                
        return magnetization
            
            
        
    def ChangementSpin(self):
        """
        Choisit un point aléatoire, change son spin et regarde la différence d'énergie associer au changement
        si la différence est négative accept le changement sinon accept avec une proababilité e^(-deltaE / KbT)
        """


        x,y = np.random.randint(self.N,size = 2)

        
        energieInitiale = -self.J* self.CalculEnergie1Point(x,y,self.grille)
        
    
        nouvGrille = np.array(self.grille)
        nouvGrille[x,y] = -nouvGrille[x,y]
        nouvEnergie = -self.J * self.CalculEnergie1Point(x,y,nouvGrille)


        deltaE = nouvEnergie-energieInitiale
        
        accept = False
        
        if deltaE < 0:
            accept = True
        else:
            accept = bool(np.random.rand() < np.exp(-deltaE / self.KbT))

        
        if accept:
            #change la grille, update la valeur de l'énergie et sauvegarde la grille pour le graphique dynamique
            self.grille = nouvGrille
            self.energy += deltaE
            self.ajoutGraphDynamique(self.grille)

        #sauvegarde de la valeur de Energie et de Magnétization    
        self.listE.append(self.energy)
        self.listM.append(self.CalculMagnetization())
      
    

    def ShowGraph(self):
        """
        Prend la grille résultante et la porte sur un graphique 2D 

        """
        fig, ax = plt.subplots()

        #####transforme chaque point de la grille en composant RGB pour pouvoir choisir la couleur#####            
        for i in range(0, self.grille.shape[0]):
            for j in range(0, self.grille.shape[1]):                
                self.grille_3d[i][j] = self.color_map[self.grille[i][j]]
        ###############################################################################################
                

        
        ax.imshow(self.grille_3d,origin = "lower",aspect="equal")
        label = np.arange(1,self.N+1)        
        
        ax.set_xticks(np.arange(0,self.N),label)        
        ax.set_yticks(np.arange(0,self.N),label)

        plt.title(self.titre)

        plt.show()

    def Result(self):
        """
        retourne les listes de valeurs d'énergies et de magnétisation
        """
        return self.listE , self.listM



    def creerGraphDynamique(self,grille):
        """
        Créer une liste d'image qui contiendra toutes les images du graphiques dynamiques et créer les éléments du graphique et règle les paramètre du graphique
        et ajoute l'image de la grille initiale

        """
        self.figDyn, self.axDyn = plt.subplots()
        self.ims = []
        self.compteurGraphDyn = 0
        
                         

        #####transforme chaque point de la grille en composant RGB pour pouvoir choisir la couleur#####     
        for i in range(0, grille.shape[0]):
            for j in range(0, grille.shape[1]):                
                self.grille_3d[i][j] = self.color_map[grille[i][j]]
        ###############################################################################################
        
         

        im = self.axDyn.imshow(self.grille_3d,origin = "lower",aspect="equal",animated = True)

        label = np.arange(1,self.N+1)
        self.axDyn.set_xticks(np.arange(0,self.N),label)
        self.axDyn.set_yticks(np.arange(0,self.N),label)
        
        self.ims.append([im])
        

    def ajoutGraphDynamique(self,grille):
        """
        est appelé à chaque fois que la grille change
        ajoute l'image de la grille à la liste d'image
        Puisque pour des KbT élevé la condition d'acceptation est moins restrictives
        utilise un compteur pour réduire le nombre d'image si KbT augmente
        (pour augmenter la rapidité du programme)
        """
        self.compteurGraphDyn += 1
        if self.compteurGraphDyn % 5*self.KbT == 0:            
            for i in range(0, grille.shape[0]):
                for j in range(0, grille.shape[1]):
                    self.grille_3d[i][j] = self.color_map[grille[i][j]]
                    
            im = self.axDyn.imshow(self.grille_3d,origin = "lower",aspect="equal",animated = True)        
            
            self.ims.append([im])

    def ShowGraphDyn(self):
        """
        imprime le graphqique dynamique créer avec la liste d'image de la grilles
        """
        ani = animation.ArtistAnimation(self.figDyn, self.ims, interval=0, blit=True, repeat_delay=3000)
        plt.title(self.titre)
        plt.show()
        




def main():
    
    #condition initiale############
    N = 20
    J = 1
    KbT = 1
    nIteration = 250000
    titre = """modèle d'ising 2D sur une grille 20X20
    avec 250 000 pas, J = 1 et KbT = 1"""
    ###############################

    SimIsing = Ising(N,J,KbT,nIteration,titre)
    
    
    SimIsing.Run()

    E,M  = SimIsing.Result()

   
        

    SimIsing.ShowGraphDyn()    
    SimIsing.ShowGraph()

    
    plt.plot(E,label="Énergie")
    plt.plot(M,label="Magnétisation")
    plt.tight_layout()
    plt.legend()
    plt.show()

    text0 = """ Lorsque le systeme à effectué environ 60 000 pas il est souvent thermalisé. Par contre la thermalisation du systeme peut prendre de 20 000 pas à + de 200 000 et depend beaucoup du hasard.
                \nLe systeme tend aussi à rester "coincé" (comme quand il se sépare en deux cotés inversement magnétisé et ralentir beaucoup le processus
            """
    text1 = """ Le signe de la magétisation semble être aléatoire et plus le KbT sera grand plus elle sera instable, faible et changeante.\nPour un Kbt de 1 il n'est pas rare
que le systeme soit entièrement magnétisé positivement/négativement et en générale le systeme forme des blobs de magnétisation semblable
            """  
    print(text0)
    print(text1)
    
    #pour KbT = 2 et 3
    KbT = 2
    titre = """modèle d'ising 2D sur une grille 20X20
avec 250 000 pas, J = 1 et KbT = 2"""
    
    SimIsing = Ising(N,J,KbT,nIteration,titre) 
    SimIsing.Run()
    E,M  = SimIsing.Result()
    SimIsing.ShowGraphDyn()    
    SimIsing.ShowGraph()

    
    plt.plot(E,label="Énergie")
    plt.plot(M,label="Magnétisation")
    plt.tight_layout()
    plt.legend()
    plt.show()

    KbT = 3
    titre = """modèle d'ising 2D sur une grille 20X20
    avec 250 000 pas, J = 1 et KbT = 3"""
    SimIsing = Ising(N,J,KbT,nIteration,titre) 
    SimIsing.Run()
    E,M  = SimIsing.Result()
    SimIsing.ShowGraphDyn()    
    SimIsing.ShowGraph()

    
    plt.plot(E,label="Énergie")
    plt.plot(M,label="Magnétisation")
    plt.tight_layout()
    plt.legend()
    plt.show()











main()
