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
import datetime
#import numpy as np

#pour executer le fichier il faut que tu remplaces la ligne 39 par le chemin d'acces du fichier EIVP_KM
chdir('C:\\Users\\baret\\Documents\\EIVP\\Outils numériques\\Python\\projet S1')
dossier_courant=getcwd()# get current directory

def convertisseur(dossier_courant, variable=[0,1,2,3,4,5,6]):
    '''renvoie les 7 listes (au format numérique) correspondant aux colonnes du fichier csv '''

    list = [] # liste des lignes du fichier csv
    id = []
    noise = []
    theta = []
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
        theta.append(float(list[i][2]))
        humidity.append(float(list[i][3]))
        lum.append(int(list[i][4]))
        co2.append(int(list[i][5]))
        sent_at.append(datetime.datetime.strptime(list[i][6][:-len(' 0+200')], '%Y-%m-%d %H:%M:%S'))
         # enlève le fuseau horaire et applique le format de date à tous les elts

    #renvoie des données conditionné par variable
    res =[]
    if 0 in variable:
        res.append(id)
    if 1 in variable:
        res.append(noise)
    if 2 in variable:
        res.append(theta)
    if 3 in variable:
        res.append(humidity)
    if 4 in variable:
        res.append(lum)
    if 5 in variable:
        res.append(co2)
    if 6 in variable:
        res.append(sent_at)
    return res

id,noise,theta,humidity,lum,co2,sent_at=convertisseur(dossier_courant)

##calculs des valeurs statistiques
# ➢ min, max, écart-type, moyenne*, variance, médiane
# * il y a différente moyenne
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


def humidex(theta,humidity):
    ''' renvoie l'indice humidex calculé à partir de la température de rosée selon la formule de Heinrich Gustav Magnus-Tetens
        Domaine de validité :
        0<T< 60 °C
        0,01 (1 %)<humidity< 1 (100 %)
        0<point de rosée< 50 °C'''
    a=17.27
    b=237.7
    def f(t,h):
        return (a*t/(b+t+log(h)-2))
    humidex=[]
    for i in range(len(theta)):
        theta_ros=b*f(theta[i],humidity[i]) / (a-f(theta[i],humidity[i]))

        humidex.append(theta[i]+0.5555*(6.11*exp(5417.7530*(1/273.16-1/(273.15+theta_ros)))-10))
    return humidex

humidex=humidex(theta,humidity)

## fonctions d'affichage
import matplotlib.pyplot as plt

def input_var():
    '''demande à l'utilisateur de rentrer une date de debut et de fin (la plage des données à étudier)
       le format des arguments est AAAA-MM-JJ HH:MM:SS /!\ sans les '' : ils sont rajoutés par input() '''
    debut=input('Date de debut au format AAAA-MM-JJ HH:MM:SS : ')
    while type(debut)!= datetime.datetime:
        try :
            debut=datetime.datetime.strptime(debut, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            debut=input('Erreur de conversion \n\tDate de debut au format AAAA-MM-JJ HH:MM:SS ')
        # finally:
            # print('2',type(debut),debut)
    fin=input('Date de fin au format AAAA-MM-JJ HH:MM:SS : ')
    while type(fin)!= datetime.datetime:
        try :
            fin=datetime.datetime.strptime(fin, '%Y-%m-%d %H:%M:%S')
        except ValueErrorError:
            fin=input('Erreur de conversion \n\tDate de fin au format AAAA-MM-JJ HH:MM:SS ')
    return debut,fin



def calcul_temps(debut=min(sent_at),fin=max(sent_at)):
    '''renvoie la liste des indices des lignes qui correspondent à l'intervalle de temps choisi.'''
    L=[]
    while fin<=debut:
        print("l'intervale de temps n'est pas valide : veuillez recommencer ")
        debut,fin=input_var()
    for i in range(len(sent_at)):
        if debut<=sent_at[i]<=fin:
            L.append(i)
    return L,[sent_at[i] for i in L]


# indice,temps=calcul_temps()


def affichage(tps,y,xlabel='t',ylabel='variable',titre='titre'):
    '''affichage de la courbe'''
    var_id=[[],[],[],[],[],[]]
    tps_id=[[],[],[],[],[],[]]
    for i in range(len(tps)) :
        (var_id[id[i]-1]).append(y[i])
        (tps_id[id[i]-1]).append(tps[i])
    for i in range(6):#len(temps_id)
        plt.plot(tps_id[i],var_id[i],'+',label="id="+str(i+1))
    plt.legend(loc="best")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(titre)
    plt.legend(loc="best")

def courbe(variable=''):
    indice,tps=calcul_temps()
    plt.close()
    plt.clf()
    if variable=="bruit":
        [noise]=convertisseur(dossier_courant,[1])
        y=[noise[i] for i in indice]
        affichage(tps,y,'temps en jour','bruit en dB','bruit mesuré en fonction du temps')
    elif variable=="température":
        [theta]=convertisseur(dossier_courant,[2])
        y=[theta[i] for i in indice]
        affichage(tps,y,'temps en jour','température en °C','évolution de la température en fonction du temps')
    elif variable=="humidité":
        [humidity]=convertisseur(dossier_courant,[3])
        y=[humidity[i] for i in indice]
        affichage(tps,y,'temps en jour',"degré d'humidité en %","évolution de l'humidité en fonction du temps")
    elif variable=="luminosité":
        [lum]=convertisseur(dossier_courant,[4])
        y=[lum[i] for i in indice]
        affichage(tps,y,'temps en jour',"lumière en lux","lumière en fonction du temps")
    elif variable=="CO2":
        [co2]=convertisseur(dossier_courant,[5])
        y=[co2[i] for i in indice]
        affichage(tps,y,'temps en jour',"CO2 en ppm","taux de CO2 en fonction du temps")
    plt.show()

###indice de correlation
### mesure de similarité
### période horaire des bureaux