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
import numpy as np

#pour executer le fichier il faut que tu remplaces la ligne 39 par le chemin d'acces du fichier EIVP_KM
chdir('C:\\Users\\baret\\Documents\\EIVP\\Outils numériques\\Python\\projet S1')
dossier_courant=getcwd()# get current directory

def convertisseur(dossier_courant, variable=[0,1,2,3,4,5,6,7]):
    '''renvoie les 7 listes (au format numérique) correspondant aux colonnes du fichier csv '''

    ligne = [] # liste des lignes du fichier csv
    indice=[]
    identifiant = []
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
        ligne.append(row[0].split(';'))

    f.close

    #conversion du fichier en liste et des strings en nombre
    for i in range(1,len(ligne)-1):

        indice.append(int(ligne[i][0]))
        identifiant.append(int(ligne[i][1]))
        noise.append(float(ligne[i][2]))
        theta.append(float(ligne[i][3]))
        humidity.append(float(ligne[i][4]))
        lum.append(int(ligne[i][5]))
        co2.append(int(ligne[i][6]))
        sent_at.append(datetime.datetime.strptime(ligne[i][7][:-len(' 0+200')], '%Y-%m-%d %H:%M:%S'))
         # enlève le fuseau horaire et applique le format de date à tous les elts
    #renvoie des données conditionné par variable
    res =[]
    if 0 in variable:
        res.append(indice)
    if 1 in variable:
        res.append(identifiant)
    if 2 in variable:
        res.append(noise)
    if 3 in variable:
        res.append(theta)
    if 4 in variable:
        res.append(humidity)
    if 5 in variable:
        res.append(lum)
    if 6 in variable:
        res.append(co2)
    if 7 in variable:
        res.append(sent_at)
    return res

indice,identifiant,noise,theta,humidity,lum,co2,sent_at=convertisseur(dossier_courant)
L=convertisseur(dossier_courant)

##calculs des valeurs statistiques
# ➢ min, max, écart-type, moyenne*, variance, médiane
# * il y a différente moyenne
import statistics as st
from math import sqrt,log,exp

def outils_st(L,unité="unité"):
    m=min(L)
    M=max(L)
    mu=st.mean(L)
    median=st.median(L)
    var=st.pvariance(L,mu)
    print(f"min={m} {unité}\nmax={M} {unité}\nmoyenne={round(mu,2)} {unité}\nmediane={median} {unité}\nvariance={round(var,2)} {unité}^2\nécart-type={round(sqrt(var),2)} {unité}\n")
    return m,M,mu,median,var,sqrt(var)

# def select_id(id,var):
#     L=[]
#     for i in range(len(var)) :
#         if identifiant[i]==id :
#             L.append(var[i])
#     return L
#
# for i in range(1,7):
#     L=select_id(i,theta)
#     outils_st(L)
# def min(l):
#     m=l[0]
#     for e in l:
#         if e<m:
#             m=e
#     return m
#
# def max(l):
#     m=l[0]
#     for e in l:
#         if e>m:
#             m=e
#     return m
# def moyenne(l):
#     s=0
#     for e in l:
#         s+=e
#     return s/len(l)
#
# def mediane(l):
#     L=copy.deepcopy(l)
#     sort(L)
#     if len(L)%2==0:
#         return (L[len(L)//2]+L[len(L)//2+1])/2
#     else:
#         return L[len(L)//2+1]
# import math
# def variance_ecart_type(l):
#     m=moyenne(l)
#     s=0
#     for e in l:
#        s+=e**2
#     v=s/len(l)-m**2
#     return v, math.sqrt(v)

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
    hx=[]
    for i in range(len(theta)):
        theta_ros=b*f(theta[i],humidity[i]) / (a-f(theta[i],humidity[i]))

        hx.append(theta[i]+0.5555*(6.11*exp(5417.7530*(1/273.16-1/(273.15+theta_ros)))-10))
    return hx
hx=humidex(theta,humidity)
## fonctions d'affichage
import matplotlib.pyplot as plt

mintps=datetime.datetime(2019, 8, 11, 11, 30, 50)#=min(sent_at)
maxtps=datetime.datetime(2019, 8, 25, 17, 47, 8) #=max(sent_at)

def calcul_temps(debut=mintps,fin=maxtps):
    '''renvoie la liste des indices des lignes qui correspondent à l'intervalle de temps choisi.'''
    L=[]
    for i in range(len(sent_at)):
        if debut<=sent_at[i]<=fin:
            L.append(i)
    return L,[sent_at[i] for i in L]

def affichage(indice,id,tps,var,xlabel='t',ylabel='variable',titre='titre'):
    '''affichage de la courbe y en fct de tps et des différents ID'''
    fig = plt.figure()
    y=[var[i] for i in indice]
    var_id=[[],[],[],[],[],[]]
    tps_id=[[],[],[],[],[],[]]
    for i in indice :
        (var_id[id[i]-1]).append(y[i])
        (tps_id[id[i]-1]).append(tps[i])

    for i in range(6):#len(temps_id)
        plt.plot(tps_id[i],var_id[i],'+',label="id="+str(i+1))
    plt.legend(loc="best")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(titre)
    return fig

def courbe(variable,debut=mintps,fin=maxtps):
    '''affiche la courbe temporelle se referant à la variable passée en argument : l'argument doit être une chaine de charactère parmi 'bruit','température','humidité','luminosité','CO2','humidex' '''
    indice,tps=calcul_temps(debut,fin)
    # plt.close()
    # plt.clf()
    if variable=="bruit":
        identifiant,noise=convertisseur(dossier_courant,[1,2])
        fig=affichage(indice,identifiant,tps,noise,'temps','bruit en dB','bruit mesuré en fonction du temps')
        unité="dB"
        '''je n'arrive pas a afficher le texe sur le graphe'''
        # m,M,mu,median,var,sigma=outils_st(noise,unité)
        # plt.text(1,1,f"min={m} {unité}\nmax={M} {unité}\nmoyenne={round(mu,2)} {unité}\nmediane={median} {unité}\nvariance={round(var,2)} {unité}**2\nécart-type={round(sigma,2)} {unité}\n",bbox=dict(facecolor='red', alpha=0.5),transform=fig.transFigure)
        plt.show()

    elif variable=="température":
        identifiant,theta=convertisseur(dossier_courant,[1,3])
        affichage(indice,identifiant,tps,theta,'temps','température en °C','évolution de la température en fonction du temps')
        plt.show()

    elif variable=="humidité":
        identifiant,humidity=convertisseur(dossier_courant,[1,4])
        affichage(indice,identifiant,tps,humidity,'temps',"degré d'humidité en %","évolution de l'humidité en fonction du temps")
        plt.show()

    elif variable=="luminosité":
        identifiant,lum=convertisseur(dossier_courant,[1,5])
        affichage(indice,identifiant,tps,lum,'temps',"lumière en lux","lumière en fonction du temps")
        plt.show()

    elif variable=="CO2":
        identifiant,co2=convertisseur(dossier_courant,[1,6])
        affichage(indice,identifiant,tps,co2,'temps',"CO2 en ppm","taux de CO2 en fonction du temps")
        plt.show()

    elif variable=="humidex":
        identifiant,theta,humidity=convertisseur(dossier_courant,[1,3,4])
        y=humidex(theta,humidity)
        affichage(indice,identifiant,tps,y,'temps',"indice humidex","humidex en fonction du temps")
        plt.show()
    else :
        print("erreur : l'argument doit être une chaine de charactère parmi 'bruit','température','humidité','luminosité','CO2','humidex'")
###displayStats

def displayStats(var,debut=mintps,fin=maxtps):
    ''''''
    indice,noise,theta,humidity,lum,co2,sent_at= convertisseur(getcwd(),[0,2,3,4,5,6,7])
    ind,dates=calcul_temps(debut,fin)
    if var == 'bruit':
        outils_st([noise[k] for k in ind],"dB")
    elif var == 'température':
        outils_st([theta[k] for k in ind],"°C")
    elif var == 'humidité' :
        outils_st([humidity[k] for k in ind],"%")
    elif var == 'luminosité':
        outils_st([lum[k] for k in ind],"lux")
    elif var == 'co2':
        outils_st([co2[k] for k in ind],"ppm")
    elif var == 'humidex':
        hx = humidex(theta,humidity)
        outils_st([hx[k] for k in ind],"%")
    else :
        print("Argument non valide. La variable doit figurer parmis les valeurs suivantes : 'bruit', 'température', 'humidité', 'luminosité', 'co2', 'humidex'. ")


### interface utilisateur

def input_tps():
    '''demande à l'utilisateur de rentrer une date de debut et de fin (la plage des données à étudier)
       le format des arguments est AAAA-MM-JJ HH:MM:SS /!\ sans les '' : ils sont rajoutés par input() '''
    debut=input('Date de debut au format AAAA-MM-JJ HH:MM:SS : ')
    while type(debut)!= datetime.datetime:
        try :
            debut=datetime.datetime.strptime(debut, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            debut=input('Erreur de conversion \n\tDate de debut au format AAAA-MM-JJ HH:MM:SS ')
    fin=input('Date de fin au format AAAA-MM-JJ HH:MM:SS : ')
    while type(fin)!= datetime.datetime:
        try :
            fin=datetime.datetime.strptime(fin, '%Y-%m-%d %H:%M:%S')
        except ValueErrorError:
            fin=input('Erreur de conversion \n\tDate de fin au format AAAA-MM-JJ HH:MM:SS ')
    while fin<=debut:
        print("l'intervale de temps n'est pas valide : veuillez recommencer ")
        debut,fin=input_tps()
    return debut,fin

def input_var()  :
    n=input("choisissez une variable parmi \n'bruit', \n'température', \n'humidité', \n'luminosité', \n'CO2', \n'humidex'\n ")

###indice de correlation
def  cor(X,Y):
    c=np.cov([X,Y])
    print(c)
    return c[0,1]/(st.pvariance(X)**(1/2)*st.pvariance(Y)**(1/2))

def graphe(L):
    plt.close()
    fig=plt.figure

    for I in L:
        mu=st.mean(I)
        sigma=np.sqrt(st.pvariance(I,mu))
        I=[(i-mu)/sigma for i in I]
        plt.plot(sent_at,I,'+')
    M=np.ones((len(L),len(L)))
    for i in range(len(M)):
        for j in range(len(M[0])):
            if i!=j:
                M[i,j]=cor(L[i],L[j])
    plt.show()
    return M
### mesure de similarité
### période horaire des bureaux