
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import colors

class VariableContainer:
    pass


p = VariableContainer()
#définir constante N
p.N = 201
#définir les limites, qui vont de -N/2 à N/2
p.correctionX = int((p.N -1)/2)
p.correctionY = int((p.N -1)/2)
#définir rayon
p.R = 0


class Cristal:

    def __init__(self):
        #initialise le cristal avec un angle aléatoire et un rayon r+1
        angle = 2*np.pi*np.random.rand()
        valx = (p.R+1) * np.cos(angle)
        valy = (p.R+1) * np.sin(angle)
        self.posx = int(np.sign(valx)*np.ceil(abs(valx)))
        self.posy = int(np.sign(valy)*np.ceil(abs(valy)))
        #variable de l'état du cristal
        self.stuck = False
        self.outOfBound = False


    def mvt(self,pos_cristals_Geles):
        #test si il doit se geler
        self.colle(pos_cristals_Geles)
            
        
        
        if not self.stuck:
            direction = np.random.randint(4)
            

            if direction == 0 :
                self.posx +=1
                            
            elif direction == 1:
                self.posy +=1
                
            elif direction == 2:
                self.posx -=1
                
            else :
                self.posy -=1
            #test si il est hors limite
            self.OffBound()
            
 


    def colle(self,pos_cristals_Geles):
        #gele si il est coller sur un cristal déjà geler
        if (    pos_cristals_Geles[self.posy + p.correctionY + 1 , self.posx + p.correctionX] == 1
            or  pos_cristals_Geles[self.posy + p.correctionY - 1 , self.posx + p.correctionX] == 1
            or  pos_cristals_Geles[self.posy + p.correctionY , self.posx + p.correctionX + 1] == 1
            or  pos_cristals_Geles[self.posy + p.correctionY , self.posx + p.correctionX - 1] == 1):
            
            self.stuck = True
        
        

    def OffBound(self):
        #hors limite si il est hors du carré NxN
        if abs(self.posx)+1 > p.correctionX or abs(self.posy)+1 > p.correctionX:
            
            self.outOfBound = True

        #hors limite si il plus loin que le cercle de rayon 2R
        #(le +2 est pour eviter que le cristal soit hors limit pour la premiere instance
        #où le cercle plus grand que r+1 est en dehors de 2R)    
        if np.sqrt(self.posx**2+self.posy**2)> 2*p.R +2:
            
            self.outOfBound = True
        
        
        




def main():
    #creer un array contenant tout mes cristals gelés
    pos_cristals_Geles = np.zeros([p.N,p.N])
    #on gel le premier cristal
    pos_cristals_Geles[p.correctionY,p.correctionX] = 1

    
    
    
    while True:

        cristal = Cristal()
        
        #deplace le nouveau cristal jusqu'à ce que le cristal se gele ou qu'il soit hors limite
        while not cristal.stuck :
            cristal.mvt(pos_cristals_Geles)
            if cristal.outOfBound:
                break


        #calcule nouveau R
        nouvR = np.sqrt(cristal.posx**2+cristal.posy**2)
        
        if not cristal.outOfBound:
            #si le nouveau r est plus grand que l'ancien on remplace
            if nouvR > p.R:
                
                p.R = nouvR
               
            #note la position de du nouveau crsital geler
            pos_cristals_Geles[cristal.posy+p.correctionY,cristal.posx+p.correctionX] = 1
            
                
            if p.R > p.N/3:
                break

        


    #creation du graphique
    fig, ax = plt.subplots()
    ax.imshow(pos_cristals_Geles,origin = "lower",aspect="equal")

    label = np.arange(-p.correctionX, p.correctionX+1,10)
    
    
    ax.set_xticks(np.arange(0, p.N, 10),label);
    ax.set_yticks(np.arange(0, p.N, 10),label);
    plt.show()



main()
