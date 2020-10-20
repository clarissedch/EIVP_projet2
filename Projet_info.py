###consignes

# ❖ Afficher des courbes montrant l’évolution d’une variable en fonction du temps. Avec
# éventuellement la possibilité de spécifier un intervalle de temps dans la ligne de commande.
#  Par exemple:
# python MONSCRIPT.py <action> <variable> <start_date> <end_date>
#  avec action = “display”, variable = “température” et optionnellement,
# start_date = “2019-01-01” et end_date = “2019-02-01”
# ❖ Afficher les valeurs statistiques sur la courbe :
# ➢ min, max, écart-type, moyenne*, variance, médiane, etc.
# Par exemple:
# python MONSCRIPT.py <action> <variable> <start_date> <end_date>
# avec action = “displayStat”, variable = “température” et optionnellement,
# start_date = “2019-01-01” et end_date = “2019-02-01”
# ❖ Calculer l’indice “humidex”
#  Par exemple :
# python MONSCRIPT.py <action> <variable> <start_date> <end_date>
# avec action = “display”, variable = “humidex” et optionnellement, start_date
# = “2019-01-01” et end_date = “2019-02-01”
# ❖ Calculer l’indice de corrélation entre un couple de variables
# ➢ Afficher la valeur dans la console (print)
# ➢ Bonus : Sur le même graphe, affichez deux courbes représentant les deux variables
# en fonction du temps et indiquer dans la légende la valeur de l’indice de corrélation.
#
# Sujet 2 - Groupe B & D
# ❖ Mesurer similarités des capteurs pour chaque dimension, qu’en concluez-vous ? Proposez et
# implémentez un algorithme permettant de mesurer la similarité automatiquement et de la
# montrer sur les courbes.
# Bonus : Trouvez automatiquement les périodes horaires d’occupations des bureaux
# #


### import des données csv
from os import chdir, getcwd, mkdir
import csv
#import numpy as np

#pour executer le fichier il faut que tu remplaces la ligne 39 par le chemin d'acces du fichier EIVP_KM
chdir('C:\\Users\\baret\\Documents\\EIVP\\Outils numériques\\Python\\projet S1')
dossier_courant=getcwd()# get current directory

def convertisseur(dossier_courant, variable=[0,1,2,3,4,5,6]):
    '''renvoie les 7 listes (au format numérique) correspondant aux colonnes du fichier csv '''

    list = [] # liste des lignes du fichier csv
    id = []
    noise = []
    temp = []
    humidity = []
    lum = []
    co2 = []
    sent_at = []

    #ouverture et lecture du fichier csv
    f = open(dossier_courant+'\\'+'EIVP_KM.csv')
    csv_f = csv.reader(f)
    for row in csv_f:
        list.append(row[0].split(';'))
    f.close

    #conversion du fichier en liste et des strings en nombre
    for i in range(1,len(list)-1):
        id.append(int(list[i][0]))
        noise.append(float(list[i][1]))
        temp.append(float(list[i][2]))
        humidity.append(float(list[i][3]))
        lum.append(int(list[i][4]))
        co2.append(int(list[i][5]))
        sent_at.append(list[i][6][:-len(' 0+200')]) # enlève le fuseau horaire commun à tous les elts

    #renvoie des données conditionné par variable
    res =[]
    if 0 in variable:
        res.append(id)
    if 1 in variable:
        res.append(noise)
    if 2 in variable:
        res.append(temp)
    if 3 in variable:
        res.append(humidity)
    if 4 in variable:
        res.append(lum)
    if 5 in variable:
        res.append(co2)
    if 6 in variable:
        res.append(sent_at)
    return res

id,noise,temp,humidity,lum,co2,sent_at=convertisseur(dossier_courant)

## fonctions d'affichage
import matplotlib.pyplot as plt
import datetime
def input_var():
    '''demande à l'utilisateur de rentrer une date de debut et de fin (la plage des données à étudier)
       le format des arguments est AAAA-MM-JJ HH:MM:SS /!\ sans les '' : ils sont rajoutés par input() '''
    debut=input('Date de debut au format AAAA-MM-JJ HH:MM:SS : ')
    while type(debut)!= datetime.datetime:
        try :
            debut=datetime.datetime.strptime(debut, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            debut=input('Erreur de conversion \n\tDate de debut au format AAAA-MM-JJ HH:MM:SS ')
        finally:
            print('2',type(debut),debut)
    fin=input('Date de fin au format AAAA-MM-JJ HH:MM:SS : ')
    while type(fin)!= datetime.datetime:
        try :
            fin=datetime.datetime.strptime(fin, '%Y-%m-%d %H:%M:%S')
        except ValueErrorError:
            fin=input('Erreur de conversion \n\tDate de fin au format AAAA-MM-JJ HH:MM:SS ')

def calcul_temps(debut,fin):
    '''renvoie la liste des indices des lignes qui correspondent à l'intervalle de temps choisi.'''
    L=[]
    for i in range(len(sent_at)):
        date=datetime.datetime.strptime(sent_at[i], '%Y-%m-%d %H:%M:%S')
        if debut<date<fin:
            L.append(i)
    return L

# deb=datetime.datetime.strptime(sent_at[0], '%Y-%m-%d %H:%M:%S')
# fin=datetime.datetime.strptime(sent_at[-1], '%Y-%m-%d %H:%M:%S')
# x=calcul_temps(fin,deb)

#temp_d=[temp[i] for i in calcul_temps(debut,fin)]# exemple
# import copy
# temptri= copy.deepcopy(temp)
# temptri.sort()
def affichage(x,y,xlabel='x',ylabel='y',titre='titre'):
    '''affichage de la courbe'''
    plt.clf()
    plt.plot(y,x,'+g',linewidth=2,label='lbl 1')
    # plt.plot(x,z,'--r',linewidth=3,label='lbl2')
    # plt.xlabel(xlabel)
    # plt.ylabel(ylabel)
    # plt.title(titre)
    #plt.xlim([1,2])
    # plt.legend(loc=0)
    plt.show()


##calculs des valeurs statistiques
# ➢ min, max, écart-type, moyenne*, variance, médiane
id,noise,temp,humidity,lum,co2,sent_at=convertisseur(dossier_courant)

import statistics as st
from math import sqrt,log,exp

def outils_st(L):
    m=min(L)
    M=max(L)
    mu=st.mean(L)
    median=st.median(L)
    var=st.pvariance(L,mu)
    print("min={},max={},moyenne={},mediane={}, variance={}, écart-type={}".format(m,M,mu,median,var,sqrt(var)))
    return(m,M,mu,median,var,sqrt(var))
def humidex(temp,humidity):
    ''' renvoie la temperature de rosée selon la formule de Heinrich Gustav Magnus-Tetens
        Domaine de validité :
        0<T< 60 °C
        0,01 (1 %)<humidity< 1 (100 %)
        0<point de rosée< 50 °C'''
    a=17.27
    b=237.7
    def f(t,h):
        return (a*t/(b+t)+ log(h))
    # print(b*f(15,0.5) / (a-f(15,0.5)))
    humidex=[]
    for i in range(len(temp)):
        tempros=b*f(temp[i],humidity[i]) / (a-f(temp[i],humidity[i]))

        humidex.append(temp[i]+0.5555*(6.11*exp(5417.7530*(1/273.16-1/(273.15+tempros)))-10))
    return humidex


###indice de correlation
### mesure de similarité
### période horaire des bureaux
