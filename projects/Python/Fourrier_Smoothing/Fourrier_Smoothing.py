

#devoir 9

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

import matplotlib.ticker as ticker

#Problème 1



def ExtracteurDonnee(nom_fichier):

    data= np.loadtxt(nom_fichier)

    
    return data




def DataGraph(x1,y1,x2,y2):


    #troncage des valeurs pour mieux voir les fréquences utiles
    
    x1 = x1[:-30000]
    x2 = x2[:-30000]
    y1 = y1[:-30000]
    y2 = y2[:-30000]
    

   

    fig, axs = plt.subplots(2,figsize=(15, 8))

    axs[0].plot(x1,abs(y1), color=(1,0,0))
    axs[0].set_title("Fréquence du piano")
    axs[0].xaxis.set_major_locator(ticker.MultipleLocator(1000))
    axs[0].xaxis.set_minor_locator(ticker.MultipleLocator(100))
    
    axs[1].plot(x2,abs(y2), color=(0,0,1))
    axs[1].set_title("Fréquence de la trompette")
    axs[1].xaxis.set_major_locator(ticker.MultipleLocator(1000))
    axs[1].xaxis.set_minor_locator(ticker.MultipleLocator(100))

   

    plt.tight_layout(pad=2.5)
    
    
    
    return plt







def TransfoFourrier(signal,samplerate):                
    # Real FFT
    c = np.fft.rfft(signal)

    

    # Get the FFT frequencies
    nu = np.fft.rfftfreq(signal.size,d=1/samplerate)



    return c , nu




def CalculFréquencePrinc(C_instru,freq_instru):


    
    #calcul de la fréquence du plus grand pic de fréquence
    #donc de la note principale

    maxIntensity = 0
    indice_freq_Max = 0
    for i in range(C_instru.size):
        
        if  C_instru[i] > maxIntensity :
            maxIntensity = C_instru[i]
            indice_freq_Max = i

    return freq_instru[indice_freq_Max]



def freq_to_note(freq):
    notes = ['La', 'La#', 'Si', 'Do', 'Do#', 'Ré', 'Ré#', 'Mi', 'Fa', 'Fa#', 'Sol', 'Sol#']

    note_number = 12 * np.log2(freq / 440) + 49  
    note_number = round(note_number)
        
    note = (note_number - 1 ) % len(notes)
    note = notes[note]
    
    return note





def main1():


    nom_fichier ='piano.txt'

    DonneePiano = ExtracteurDonnee(nom_fichier)

    nom_fichier ='trumpet.txt'

    DonneeTrompette = ExtracteurDonnee(nom_fichier)

    samplerate = 44100

    

    c_Piano, freq_piano = TransfoFourrier(DonneePiano,samplerate)

    c_Trompette, freq_trompette = TransfoFourrier(DonneeTrompette,samplerate)
   

        

    freq_princ_piano = CalculFréquencePrinc(c_Piano,freq_piano)
    freq_princ_trompette = CalculFréquencePrinc(c_Trompette,freq_trompette)

    #prenons la fréquence du piano comme la note principale
    #mais de toute facon la note de la trompette est la même 
    #1 octave plus haut car la fréquence est environ 2 fois plus grande




    plt = DataGraph(freq_piano,c_Piano, freq_trompette,c_Trompette)
    plt.show()



    #si nous avons La = 440 = V0
    #et la note du piano est 524,76

    v0 = 440

    n = np.log2(freq_princ_piano/v0)*12

    n = round(n)

    print("notre note est ",n,"demi tons au dessu de La c'est donc un "
          , freq_to_note(freq_princ_piano))







#problème 2

    




def Crop(x,keep_percent):

    new_x = np.array(x)
    
    new_x[int(len(new_x)*keep_percent/100):] = 0
   
    return new_x




def GraphDow(y1,y2):



   

    fig, axs = plt.subplots(2,figsize=(15, 8))

    axs[0].plot(y1, color=(1,0,0))
    axs[0].set_title("Donnée Dow Jones")
    axs[0].xaxis.set_major_locator(ticker.MultipleLocator(1000))
    axs[0].xaxis.set_minor_locator(ticker.MultipleLocator(100))
    
    axs[1].plot(y2, color=(0,0,1))
    axs[1].set_title("Donnée Dow Jones Filtrés")
    axs[1].xaxis.set_major_locator(ticker.MultipleLocator(1000))
    axs[1].xaxis.set_minor_locator(ticker.MultipleLocator(100))

   

    plt.tight_layout(pad=2.5)
    
    
    
    return plt

def main2():


    nom_fichier ='dow.txt'

    DonneeDow = ExtracteurDonnee(nom_fichier)

    #chaque jour donc 1 par jour
    samplerate = 1

    

    c_Dow, freq_Dow = TransfoFourrier(DonneeDow,samplerate)
    


    c_Dow_crop_10 = Crop(c_Dow,10)
    


    DonneDowFiltre_10 = np.fft.irfft(c_Dow_crop_10)


    plt = GraphDow(DonneeDow ,DonneDowFiltre_10)
    plt.show()
    
    
    c_Dow_crop_2 = Crop(c_Dow,2)
    
    DonneDowFiltre_2 = np.fft.irfft(c_Dow_crop_2)


    plt = GraphDow(DonneeDow ,DonneDowFiltre_2)
    plt.show()





    
main1()
main2()



















