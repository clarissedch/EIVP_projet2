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
mintps=datetime.datetime(2019, 8, 11, 11, 30, 50)#=min(sent_at)
maxtps=datetime.datetime(2019, 8, 25, 17, 47, 8) #=max(sent_at)

### interface utilisateur

def input_tps():
    '''demande à l'utilisateur de rentrer une date de debut et de fin (la plage des données à étudier)
       le format des arguments est AAAA-MM-JJ HH:MM:SS /!\ sans les '' : ils sont rajoutés par input() '''
    debut=input(f'Date de debut au format AAAA-MM-JJ HH:MM:SS\nentre {mintps} et {maxtps} : \n')
    while type(debut)!= datetime.datetime:
        try :
            debut=datetime.datetime.strptime(debut, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            debut=input('Erreur de conversion \n\tDate de debut au format AAAA-MM-JJ HH:MM:SS :\n')
    fin=input('Date de fin au format AAAA-MM-JJ HH:MM:SS : \n')
    while type(fin)!= datetime.datetime:
        try :
            fin=datetime.datetime.strptime(fin, '%Y-%m-%d %H:%M:%S')
        except ValueErrorError:
            fin=input('Erreur de conversion \n\tDate de fin au format AAAA-MM-JJ HH:MM:SS\n ')
    while fin<=debut:
        print("l'intervale de temps n'est pas valide : veuillez recommencer ")
        debut,fin=input_tps()
    return debut,fin

# def input_var()  :
#     n=input("choisissez une variable parmi \n'bruit', \n'température', \n'humidité', \n'luminosité', \n'CO2', \n'humidex'\n ")

def calcul_temps(debut=mintps,fin=maxtps):
    '''renvoie la liste des indices des lignes qui correspondent à l'intervalle de temps choisi.'''
    L=[]
    for i in range(len(sent_at)):
        if debut<=sent_at[i]<=fin:
            L.append(i)
    return L,[sent_at[i] for i in L]

##calculs des valeurs statistiques
import statistics as st
from math import sqrt,log,exp

def outils_st(L,unité="unité"):
    '''renvoie le min,le max, la moyenne arithmétique, la médiane, la variance et l'écart type de L et l'affiche avec l'unité renseignée'''
    if L==[]:return 0,0,0,0,0,0
    else:
        m=min(L)
        M=max(L)
        mu=st.mean(L)
        median=st.median(L)
        var=st.pvariance(L,mu)
        print(f"min={round(m,2)} {unité}\nmax={round(M,2)} {unité}\nmoyenne={round(mu,2)} {unité}\nmediane={round(median,2)} {unité}\nvariance={round(var,2)} {unité}^2\nécart-type={round(sqrt(var),2)} {unité}\n")
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
#

#def min(l):
#     m=l[0]
#     for e in l:
#         if e<m:
#             m=e
#     return m

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

# def mediane(l):
#     L=copy.deepcopy(l)
#     sort(L)
#     if len(L)%2==0:
#         return (L[len(L)//2]+L[len(L)//2+1])/2
#     else:
#         return L[len(L)//2+1]

# def variance_ecart_type(l):
#     m=moyenne(l)
#     s=0
#     for e in l:
#        s+=e**2
#     v=s/len(l)-m**2
#     return v, v**(1/2)
### humidex
def humidex(theta,humidity):
    ''' renvoie l'indice humidex calculé à partir de la température de rosée selon la formule de Heinrich Gustav Magnus-Tetens
        Domaine de validité :
        0<T< 60 °C
        0,01 (1 %)<humidity< 1 (100 %)
        0<point de rosée< 50 °C'''
    a=17.27
    b=237.7
    def f(t,h):
        return (a*t/(b+t)+log(h)-2*log(10))
    hx=[]
    for i in range(len(theta)):
        theta_ros=b*f(theta[i],humidity[i]) / (a-f(theta[i],humidity[i]))

        hx.append(theta[i]+5/9*(-10+6.11*exp(5417.7530*(1/273.16-1/(273.15+theta_ros)))))
    return hx
hx=humidex(theta,humidity)

## fonctions d'affichage
import matplotlib.pyplot as plt

def courbetps(variable,boolborne=False,boolstat=True):
    '''affiche la variable choisie en fonction du temps avec les bornes modifiables'''
    plt.close()
    if boolborne:
        debut,fin=input_tps()
        indice,tps=calcul_temps(debut,fin)
    else:
        indice,tps=calcul_temps()
    if variable=="bruit":
        i=2
        ylabel='bruit mesuré en fonction du temps'
        titre="bruit mesuré en fonction du temps"
        unité="dB"
    elif variable=="température":
        i=3
        ylabel="température en °C"
        titre='évolution de la température en fonction du temps'
        unité="°C"
    elif variable=="humidité":
        i=4
        ylabel="degré d'humidité en %"
        titre="évolution de l'humidité en fonction du temps"
        unité="%"
    elif variable=="luminosité":
        i=5
        ylabel,titre="lumière en lux","lumière en fonction du temps"
        unité="lux"
    elif variable=="CO2":
        i=6
        ylabel,titre="CO2 en ppm","taux de CO2 en fonction du temps"
        unité="ppm"
    elif variable=="humidex":
        ylabel,titre="indice humidex","humidex en fonction du temps"
        t,hy=convertisseur(dossier_courant,[3,4])
        hx=humidex(t,hy)
        hx= [hx[i] for i in indice]
        fig = plt.figure()
        plt.plot(tps,hx,'+',label=variable)
        plt.xlabel("temps")
        plt.ylabel(ylabel)
        plt.title(titre)
        plt.show()
        if boolstat:
            unité=" "
            m,M,mu,median,_,sigma=outils_st(var,unité)
            plt.text(0,0,f"min={m} {unité}\nmax={M} {unité}\nmoyenne={round(mu,2)} {unité}\nmédiane={median} {unité}\nécart-type={round(sigma,2)} {unité}\n",bbox=dict(facecolor='white', alpha=0.9),transform=fig.transFigure)
        return None
    else :
        print("erreur : l'argument  var doit être une chaine de charactère parmi 'bruit','température','humidité','luminosité','CO2','humidex'")
        return None

    [var]=convertisseur(dossier_courant,[i])
    print(len(var),len(indice))
    var=[var[i] for i in indice]
    fig = plt.figure()
    plt.plot(tps,var,'+',label=variable)
    plt.xlabel("temps")
    plt.ylabel(ylabel)
    plt.title(titre)
    plt.show()

    if boolstat:
        m,M,mu,median,_,sigma=outils_st(var,unité)
        plt.text(0,0,f"min={m} {unité}\nmax={M} {unité}\nmoyenne={round(mu,2)} {unité}\nmédiane={median} {unité}\nécart-type={round(sigma,2)} {unité}\n",bbox=dict(facecolor='white', alpha=0.9),transform=fig.transFigure)
    return None

def affichage(indice,id,tps,var,xlabel='t',ylabel='variable',titre='titre',unité="unit"):
    '''affichage de la courbe y en fct de tps et des différents ID'''
    fig = plt.figure()
    y=[var[i] for i in indice]
    var_id=[[],[],[],[],[],[]]
    tps_id=[[],[],[],[],[],[]]
    for i in indice :
        (var_id[id[i]-1]).append(y[i])
        (tps_id[id[i]-1]).append(tps[i])

    for i in range(6):
        plt.plot(tps_id[i],var_id[i],"+",label="id="+str(i+1))
        outils_st(var_id[i],unité)
    plt.legend(loc="best")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(titre)
    return fig

def courbe(variable,bool=True):
    '''affiche la courbe temporelle se referant à la variable passée en argument : l'argument doit être une chaine de charactère parmi 'bruit','température','humidité','luminosité','CO2','humidex' bool permet d'afficheer les stats'''
    indice,tps=calcul_temps()
    plt.close()
    if variable=="bruit":
        i=2
        ylabel,titre='bruit en dB','bruit mesuré en fonction du temps'
        unité="dB"
    elif variable=="température":
        i=3
        unité="°C"
        ylabel,titre='température en °C','évolution de la température en fonction du temps'

    elif variable=="humidité":
        i=4
        unité="%"
        ylabel,titre="degré d'humidité en %","évolution de l'humidité en fonction du temps"

    elif variable=="luminosité":
        i=5
        ylabel,titre="lumière en lux","lumière en fonction du temps"
        unité="lux"
    elif variable=="CO2":
        i=6
        ylabel,titre="CO2 en ppm","taux de CO2 en fonction du temps"
        unité="ppm"

    elif variable=="humidex":
        identifiant,theta,humidity=convertisseur(dossier_courant,[1,3,4])
        y=humidex(theta,humidity)
        fig=affichage(indice,identifiant,tps,y,'temps',"indice humidex","humidex en fonction du temps",unité)
        if bool:
            unité=" "
            m,M,mu,median,var,sigma=outils_st(y,unité)
            plt.text(0,0,f"min={round(m,2)} {unité}\nmax={round(M,2)} {unité}\nmoyenne={round(mu,2)} {unité}\nmédiane={round(median,2)} {unité}\nécart-type={round(sigma,2)} {unité}\n",bbox=dict(facecolor='white', alpha=0.9),transform=fig.transFigure)
        plt.show()
        return None
    else :
        print("erreur : l'argument  var doit être une chaine de charactère parmi 'bruit','température','humidité','luminosité','CO2','humidex'")
        return None
    identifiant,var=convertisseur(dossier_courant,[1,i])
    fig=affichage(indice,identifiant,tps,var,'temps',ylabel,titre,unité)
    plt.show()
    if bool:
        m,M,mu,median,_,sigma=outils_st(var,unité)
        plt.text(0,0,f"min={m} {unité}\nmax={M} {unité}\nmoyenne={round(mu,2)} {unité}\nmédiane={median} {unité}\nécart-type={round(sigma,2)} {unité}\n",bbox=dict(facecolor='white', alpha=0.9),transform=fig.transFigure)
        return None


def split_id(var,id,indice):
    ''' renvoie une liste de 6 listes correspondants à la variable prise en argument séparer selon identifiant et une autre de 6 listes pour les indices correspondant.'''
    var_id=[[],[],[],[],[],[]]
    ind_id=[[],[],[],[],[],[]]
    for i in indice :
        (var_id[id[i]-1]).append(var[i])
        (ind_id[id[i]-1]).append(indice[i])

    return var_id,ind_id
def display_stats(var,boolborne=False):
    '''affiche les statistiques entre les bornes renseignées ou celles de toutes la liste argument si elles ne sont pas précisées '''
    if boolborne:
        debut,fin=input_tps()
        ind,tps=calcul_temps(debut,fin)
    else:
        ind,tps=calcul_temps()
    noise,theta,humidity,lum,co2= convertisseur(getcwd(),[2,3,4,5,6])

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
        outils_st([hx[k] for k in ind]," ")
    else :
        print("Argument non valide. La variable doit figurer parmi les valeurs suivantes : 'bruit', 'température', 'humidité', 'luminosité', 'co2', 'humidex'. ")

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
