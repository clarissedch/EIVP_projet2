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
    humidex_list=[]
    for i in range(len(theta)):
        theta_ros=b*f(theta[i],humidity[i]) / (a-f(theta[i],humidity[i]))

        humidex_list.append(theta[i]+0.5555*(6.11*exp(5417.7530*(1/273.16-1/(273.15+theta_ros)))-10))
    return humidex_list

## fonctions d'affichage
import matplotlib.pyplot as plt

mintps=datetime.datetime(2019, 8, 11, 11, 31, 42)#=min(sent_at)
maxtps=datetime.datetime(2020, 9, 25, 17, 47, 8) #=max(sent_at)

def calcul_temps(debut=mintps,fin=maxtps):
    '''renvoie la liste des indices des lignes qui correspondent à l'intervalle de temps choisi.'''
    L=[]
    for i in range(len(sent_at)):
        if debut<=sent_at[i]<=fin:
            L.append(i)
    return L,[sent_at[i] for i in L]

def affichage(indice,tps,var,xlabel='t',ylabel='variable',titre='titre'):
    '''affichage de la courbe y en fct de tps et des différents ID'''
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

def courbe(variable,debut=mintps,fin=maxtps):
    '''affiche la courbe temporelle se referant à la variable passée en argument : l'argument doit être une chaine de charactère parmi 'bruit','température','humidité','luminosité','CO2','humidex' '''
    indice,tps=calcul_temps(debut,fin)
    plt.close()
    plt.clf()
    if variable=="bruit":
        [noise]=convertisseur(dossier_courant,[1])
        affichage(indice,tps,noise,'temps en jour','bruit en dB','bruit mesuré en fonction du temps')

    elif variable=="température":
        [theta]=convertisseur(dossier_courant,[2])
        affichage(indice,tps,theta,'temps en jour','température en °C','évolution de la température en fonction du temps')

    elif variable=="humidité":
        [humidity]=convertisseur(dossier_courant,[3])
        affichage(indice,tps,humidity,'temps en jour',"degré d'humidité en %","évolution de l'humidité en fonction du temps")

    elif variable=="luminosité":
        [lum]=convertisseur(dossier_courant,[4])
        affichage(indice,tps,lum,'temps en jour',"lumière en lux","lumière en fonction du temps")

    elif variable=="CO2":
        [co2]=convertisseur(dossier_courant,[5])
        affichage(indice,tps,co2,'temps en jour',"CO2 en ppm","taux de CO2 en fonction du temps")

    elif variable=="humidex":
        theta,humidity=convertisseur(dossier_courant,[2,3])
        y=humidex(theta,humidity)
        affichage(indice,tps,y,'temps en jour',"indice humidex","humidex en fonction du temps")
    else :
        print("erreur : l'argument doit être une chaine de charactère parmi 'bruit','température','humidité','luminosité','CO2','humidex'")
    plt.show()
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
    input("choisissez une variable en entrant le numéro correspondant: \n 1 : 'bruit', \n 2 : 'température', \n 3 : 'humidité', \n 4 : 'luminosité', \n 5 : 'CO2', \n 6 : 'humidex'\n ")

###displayStats

def displayStats(var):
    début,fin=input_tps()
    indices,dates=calcul_temps(début,fin)
    L = convertisseur(getcwd(),[1,2,3,4,5])
    theta=[L[1][k] for k in indices]
    humidity=[L[2][k] for k in indices]
    if var == 'bruit':
        outils_st([L[0][k] for k in indices])
    elif var == 'température':
        outils_st(theta)
    elif var == 'humidité' :
        outils_st(humidity)
    elif var == 'luminosité':
        outils_st([L[3][k] for k in indices])
    elif var == 'co2':
        outils_st([L[4][k] for k in indices])
    elif var == 'humidex':
        hx = humidex(theta,humidity)
        outils_st(hx)
    else :
        print("Argument non valide. La variable doit figurer parmis les valeurs suivantes : 'bruit', 'température', 'humidité', 'luminosité', 'co2', 'humidex'. ")
    
    
 def graphe(L):
    '''prend une liste de variable a afficher en fonction du temps et les affiche sur un meme graphe en les centrants et en les réduisant pour s'affranchir de problème d'unité.'''
    plt.close()
    fig=plt.figure
    i=0
    for I in L:
        mu=st.mean(I)
        sigma=np.sqrt(st.pvariance(I,mu))
        I=[(i-mu)/sigma for i in I]
        plt.plot(sent_at,I,'+',label=i)
        i+=1
    M=np.ones((len(L),len(L)))
    for i in range(len(M)):
        for j in range(len(M[0])):
            if i!=j:
                M[i,j]=cor(L[i],L[j])
    plt.legend()
    plt.show()
    return M
    
    
    
###indice de correlation

def  cor(X,Y):
    '''renvoie le coefficient de correlation entre deux variable en utilisant la matrice de covarience numpy.'''
    c=np.cov([X,Y])
    return c[0,1]/(st.pvariance(X)**(1/2)*st.pvariance(Y)**(1/2))

# def covariances(var1,var2,debut,fin):
#     indices,dates=calcul_temps(debut,fin)
#     res = []
#     l1=[var1[j] for j in indices]
#     l2=[var2[k] for k in indices]
#     m1=st.mean(l1)
#     m2=st.mean(l2)
#     for i in indices :
#         res.append ((var1[i]-m1)*(var2[i]-m2))
#     return st.mean(res),sqrt(st.pvariance(l1,m1)),sqrt(st.pvariance(l2,m2))

# def correlation(var1,var2,debut,fin):
#     v,s1,s2=covariances(var1,var2,debut,fin)
#     return v/(s1*s2)



def covariances(var1,var2,debut,fin):
    indices,dates=calcul_temps(debut,fin)
    res = 0
    l1=[var1[j] for j in indices]
    l2=[var2[k] for k in indices]
    m1=st.mean(l1)
    m2=st.mean(l2)
    for i in indices :
        res += var1[i]*var2[i]
    return res-(m1*m2),math.sqrt(st.pvariance(l1,m1)),math.sqrt(st.pvariance(l2,m2))

def correlation(var1,var2):
    debut,fin=input_tps()
    v,s1,s2=covariances(var1,var2,debut,fin)
    return r/(s1*s2)



### mesure de similarité
### période horaire des bureaux

### temps d'occupation des bureaux :
def temps_occupé():
    dirac=[]
    plt.close()
    for i in indice :
        if noise[i]>39:
            dirac.append(1)
        else: dirac.append(0)
    plt.plot(sent_at,dirac,"+r")
    plt.show()
    intervalle=[]
    j=11
    while j<=25:
        L=[]
        for i in indice:
            if datetime.datetime(2019, 8,j, 0, 0, 0)< sent_at[i]:
                if datetime.datetime(2019, 8,j+1, 0, 0, 0)> sent_at[i]:
                    if dirac[i]:
                        L.append(sent_at[i])
        try:
            intervalle.append((min(L),max(L)))
        except ValueError:
            None
        j+=1
    for i in intervalle:
        print(i[0].strftime("%m/%d/%Y, %H:%M:%S"),i[1].strftime(" %H:%M:%S"))
        print(i[1]-i[0])






