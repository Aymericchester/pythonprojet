'''Fichier Iris et challenge KNN (à la fin)'''

#%% Challenge KNN, fichier iris

from math import sqrt
from collections import Counter
import numpy as np
import random


class individu:
    
    def __init__(self,x=0,y=0,z=0,t=0,categorie=""):
        self.x=x
        self.y=y
        self.z=z
        self.t=t
        self.categorie=categorie
        
    def Affiche(self):
        return ("individu: " + str(self.x) + ", " + str(self.y)+", "+str(self.z)+", "+str(self.t)+", "+str(self.categorie))
    
    def distance(self, other):
        distance=sqrt((self.x-other.x)**2+(self.y-other.y)**2+(self.z-other.z)**2+(self.t-other.t)**2)
        return distance

def knn(ind, k, liste):
    tab_distance=[]
    for d in liste: 
        dist=ind.distance(d)
        tab_distance.append((dist, d.categorie))
    tab_distance.sort(key=lambda x:x[0]) 
    #print(tab_distance)
                #chercher les k premiers individus
    tab=tab_distance[:k]
    c = Counter()
    cat=[]
    for i in tab:
        indiv=i[1]
        if indiv in cat:
            c[indiv]+=1
        else:
            cat.append(indiv)
            c[indiv]+=1
    m=max(c)        # m est la catégorie de l'individu max
    return m
                    #retourner la catégorie majorante des k indiv trouvés
def rechercher_k(pourcentage_test, Individu):
    data_test=[]
    data_app=[]
    for l in range(int(len(Individu)*pourcentage_test/100)):
        x=random.randint(0, len(Individu)-1)
        data_test.append(Individu[x])
        Individu.pop(x)
    for j in range(len(Individu)-int(len(Individu)*pourcentage_test/100)):
        y=random.randint(0, len(Individu)-1)
        data_app.append(Individu[y])
        Individu.pop(y)
    Liste_k=[]
    for k in range(1,10):
        mat=np.zeros((3,3))
        for d in data_test:
            c=knn(d,k,data_app) 
            if d.categorie=="Iris-setosa":  # remplir la matrice de confusion
                if c=="Iris-setosa": 
                    mat[0][0]+=1 
                elif c=="Iris-versicolor":  
                    mat[1][0]+=1
                elif c=="Iris-virginica":  
                    mat[2][0]+=1
            if d.categorie=="Iris-versicolor":  
                if c=="Iris-setosa":  
                    mat[0][1]+=1
                elif c=="Iris-versicolor": 
                    mat[1][1]+=1 
                elif c=="Iris-virginica":  
                    mat[2][1]+=1
            if d.categorie=="Iris-virginica":  
                if c=="Iris-setosa": 
                    mat[0][2]+=1 
                elif c=="Iris-versicolor":  
                    mat[1][2]+=1
                elif c=="Iris-virginica":  
                    mat[2][2]+=1
        print(mat)
        setosa=mat[:,0]
        if setosa[0]==0:
            setosa[0]=1
        x1=np.sum(setosa)/setosa[0]
        versicolor=mat[:,1]
        if versicolor[1]==0:
            versicolor[1]=1
        x2=np.sum(versicolor)/versicolor[1]
        virginica=mat[:,2]
        if virginica[2]==0:
            virginica[2]=1
        x3=np.sum(virginica)/virginica[2]
        Liste_k.append(x1+x2+x3) 
    mini=Liste_k[0]
    indice=0
    for i in range(len(Liste_k)): #selectionner la meilleur valeur de k (celle qui a le moins d'erreur dans sa matrice de conf)
        if Liste_k[i]<=mini:
            mini=Liste_k[i]
            indice=i
    return indice+1 # meilleur valeur de k


fichier=open("C:\\Users\\aches\\Documents\\ESILV\\A3\\Info\\DIA\\IA3-ml_data_iris.txt","r")
Individu1=[]
for ligne in fichier:
    ligne=ligne.strip('\n')
    L=ligne.split(",")
    i=individu(float(L[0]),float(L[1]),float(L[2]),float(L[3]),L[4])  #lecture fichier à faire avant knn
    Individu1.append(i)
test=individu(5.7,2.9,4.2,1.3,"?")
t=knn(test,5,Individu1)
print("L'algorithme KNN renvoie: ",t)             
print("La meilleur valeur de k est: ",rechercher_k(50, Individu1)) 
fichier.close()

#%% Challenge KNN, fichier data

from math import sqrt
from collections import Counter
import numpy as np
import random

class individu2:
    
    def __init__(self,x=0,y=0,z=0,t=0,x1=0,y1=0,z1=0,categorie=""):
        self.x=x
        self.y=y
        self.z=z
        self.t=t
        self.x1=x1
        self.y1=y1
        self.z1=z1
        self.categorie=categorie
        
    def Affiche(self):
        return ("individu: " + str(self.x) + ", " + str(self.y)+", "+str(self.z)+", "+str(self.t)+", "+ str(self.x1) + ", " + str(self.y1)+", "+str(self.z1)+", "+str(self.categorie))
    
    def distance(self, other):
        distance=sqrt((self.x-other.x)**2+(self.y-other.y)**2+(self.z-other.z)**2+(self.t-other.t)**2+(self.x1-other.x1)**2+(self.y1-other.y1)**2+(self.z1-other.z1)**2)
        return distance
    
def knn2(ind, k, liste):
                #trouver les k plus proches voisins de individus
    tab_distance=[]
    for d in liste: 
        dist=ind.distance(d)
        tab_distance.append((dist, d.categorie))
    tab_distance.sort(key=lambda x:x[0]) 
    #print(tab_distance)
                #chercher les k premiers individus
    tab=tab_distance[:k]
    c = Counter()
    cat=[]
    for i in tab:
        indiv=i[1]
        if indiv in cat:
            c[indiv]+=1
        else:
            cat.append(indiv)
            c[indiv]+=1
    m=max(c)        # m est la catégorie de l'individu max
    return m

def rechercher_k2(pourcentage_test, Individu):
    data_test=[]
    data_app=[]
    for l in range(int(len(Individu)*pourcentage_test/100)):
        x=random.randint(0, len(Individu)-1)
        data_test.append(Individu[x])
        Individu.pop(x)
    for j in range(len(Individu)-int(len(Individu)*pourcentage_test/100)):
        y=random.randint(0, len(Individu)-1)
        data_app.append(Individu[y])
        Individu.pop(y)
    Liste_k=[]
    for k in range(1,10):
        mat=np.zeros((4,4))
        for d in data_test:
            c=knn2(d,k,data_app) 
            if d.categorie=="0":  # remplir la matrice de confusion
                if c=="0": 
                    mat[0][0]+=1 
                elif c=="1":  
                    mat[1][0]+=1
                elif c=="2":  
                    mat[2][0]+=1
                elif c=="3":  
                    mat[3][0]+=1
            if d.categorie=="1":  
                if c=="0":  
                    mat[0][1]+=1
                elif c=="1": 
                    mat[1][1]+=1 
                elif c=="2":  
                    mat[2][1]+=1
                elif c=="3":  
                    mat[3][1]+=1
            if d.categorie=="2":  
                if c=="0": 
                    mat[0][2]+=1 
                elif c=="1":  
                    mat[1][2]+=1
                elif c=="2":  
                    mat[2][2]+=1
                elif c=="3":  
                    mat[3][2]+=1
            if d.categorie=="3":  
                if c=="0": 
                    mat[0][3]+=1 
                elif c=="1":  
                    mat[1][3]+=1
                elif c=="2":  
                    mat[2][3]+=1
                elif c=="3":  
                    mat[3][3]+=1
        print(mat)
        c1=mat[:,0]
        if c1[0]==0:
            c1[0]=1
        x1=np.sum(c1)/c1[0]
        c2=mat[:,1]
        if c2[1]==0:
            c2[1]=1
        x2=np.sum(c2)/c2[1]
        c3=mat[:,2]
        if c3[2]==0:
            c3[2]=1
        x3=np.sum(c3)/c3[2]
        c4=mat[:,3]
        if c4[3]==0:
            c4[3]=1
        x4=np.sum(c4)/c4[3]
        Liste_k.append(x1+x2+x3+x4) 
    mini=Liste_k[0]
    indice=0
    for i in range(len(Liste_k)): #selectionner la meilleur valeur de k (celle qui a le moins d'erreur dans sa matrice de conf)
        if Liste_k[i]<=mini:
            mini=Liste_k[i]
            indice=i
    return indice+1 # meilleur valeur de k

fichier2=open("C:\\Users\\aches\\Documents\\ESILV\\A3\\Info\\DIA\\data.txt","r")
Individu2=[]
for ligne in fichier2:
    ligne=ligne.strip('\n')
    L=ligne.split(";")
    i=individu2(float(L[0]),float(L[1]),float(L[2]),float(L[3]),float(L[4]),float(L[5]),float(L[6]),L[7])  
    Individu2.append(i)
test=individu2(5.7,2.9,4.2,1.3,4,5,7,"?")
t=knn2(test,5,Individu2)
print("L'algorithme KNN renvoie: ",t)
print("La meilleur valeur de k est: ",rechercher_k2(50, Individu2))
fichier2.close()


#%% Challenge KNN, fichier pretest

from math import sqrt
from collections import Counter
import numpy as np
import random

class individu3:
    
    def __init__(self,x=0,y=0,z=0,t=0,x1=0,y1=0,z1=0,categorie=""):
        self.x=x
        self.y=y
        self.z=z
        self.t=t
        self.x1=x1
        self.y1=y1
        self.z1=z1
        self.categorie=categorie
        
    def Affiche(self):
        return ("individu: " + str(self.x) + ", " + str(self.y)+", "+str(self.z)+", "+str(self.t)+", "+ str(self.x1) + ", " + str(self.y1)+", "+str(self.z1)+", "+str(self.categorie))
    
    def distance(self, other):
        distance=sqrt((self.x-other.x)**2+(self.y-other.y)**2+(self.z-other.z)**2+(self.t-other.t)**2+(self.x1-other.x1)**2+(self.y1-other.y1)**2+(self.z1-other.z1)**2)
        return distance
    
def knn3(ind, k, liste):
                #trouver les k plus proches voisins de individus
    tab_distance=[]
    for d in liste: 
        dist=ind.distance(d)
        tab_distance.append((dist, d.categorie))
    tab_distance.sort(key=lambda x:x[0]) 
    #print(tab_distance)
                #chercher les k premiers individus
    tab=tab_distance[:k]
    c = Counter()
    cat=[]
    for i in tab:
        indiv=i[1]
        if indiv in cat:
            c[indiv]+=1
        else:
            cat.append(indiv)
            c[indiv]+=1
    m=max(c)        # m est la catégorie de l'individu max
    return m

def rechercher_k3(pourcentage_test, Individu):
    data_test=[]
    data_app=[]
    for l in range(int(len(Individu)*pourcentage_test/100)):
        x=random.randint(0, len(Individu)-1)
        data_test.append(Individu[x])
        Individu.pop(x)
    for j in range(len(Individu)-int(len(Individu)*pourcentage_test/100)):
        y=random.randint(0, len(Individu)-1)
        data_app.append(Individu[y])
        Individu.pop(y)
    Liste_k=[]
    for k in range(1,10):
        mat=np.zeros((4,4))
        for d in data_test:
            c=knn3(d,k,data_app) 
            if d.categorie=="0":  # remplir la matrice de confusion
                if c=="0": 
                    mat[0][0]+=1 
                elif c=="1":  
                    mat[1][0]+=1
                elif c=="2":  
                    mat[2][0]+=1
                elif c=="3":  
                    mat[3][0]+=1
            if d.categorie=="1":  
                if c=="0":  
                    mat[0][1]+=1
                elif c=="1": 
                    mat[1][1]+=1 
                elif c=="2":  
                    mat[2][1]+=1
                elif c=="3":  
                    mat[3][1]+=1
            if d.categorie=="2":  
                if c=="0": 
                    mat[0][2]+=1 
                elif c=="1":  
                    mat[1][2]+=1
                elif c=="2":  
                    mat[2][2]+=1
                elif c=="3":  
                    mat[3][2]+=1
            if d.categorie=="3":  
                if c=="0": 
                    mat[0][3]+=1 
                elif c=="1":  
                    mat[1][3]+=1
                elif c=="2":  
                    mat[2][3]+=1
                elif c=="3":  
                    mat[3][3]+=1
        print(mat)
        c1=mat[:,0]
        if c1[0]==0:
            c1[0]=1
        x1=np.sum(c1)/c1[0]
        c2=mat[:,1]
        if c2[1]==0:
            c2[1]=1
        x2=np.sum(c2)/c2[1]
        c3=mat[:,2]
        if c3[2]==0:
            c3[2]=1
        x3=np.sum(c3)/c3[2]
        c4=mat[:,3]
        if c4[3]==0:
            c4[3]=1
        x4=np.sum(c4)/c4[3]
        Liste_k.append(x1+x2+x3+x4) 
    mini=Liste_k[0]
    indice=0
    for i in range(len(Liste_k)): #selectionner la meilleur valeur de k (celle qui a le moins d'erreur dans sa matrice de conf)
        if Liste_k[i]<=mini:
            mini=Liste_k[i]
            indice=i
    return indice+1 # meilleur valeur de k

fichier3=open("C:\\Users\\aches\\Documents\\ESILV\\A3\\Info\\DIA\\pretest.txt","r")
Individu3=[]
for ligne in fichier3:
    ligne=ligne.strip('\n')
    L=ligne.split(";")
    i=individu3(float(L[0]),float(L[1]),float(L[2]),float(L[3]),float(L[4]),float(L[5]),float(L[6]),L[7])  
    Individu3.append(i)

test=individu3(5.7,2.9,4.2,1.3,4,5,7,"?")
t=knn3(test,5,Individu3)
print("L'algorithme KNN renvoie: ",t)
print("La meilleur valeur de k est: ",rechercher_k3(50, Individu3))
fichier3.close()

#%% Challenge KNN, fichier finalTest

from math import sqrt
from collections import Counter
import numpy as np
import random

class individu4:
    
    def __init__(self,x=0,y=0,z=0,t=0,x1=0,y1=0,z1=0,categorie=""):
        self.x=x
        self.y=y
        self.z=z
        self.t=t
        self.x1=x1
        self.y1=y1
        self.z1=z1
        self.categorie=categorie
        
    def Affiche(self):
        return ("individu: " + str(self.x) + ", " + str(self.y)+", "+str(self.z)+", "+str(self.t)+", "+ str(self.x1) + ", " + str(self.y1)+", "+str(self.z1)+", "+str(self.categorie))
    
    def distance(self, other):
        distance=sqrt((self.x-other.x)**2+(self.y-other.y)**2+(self.z-other.z)**2+(self.t-other.t)**2+(self.x1-other.x1)**2+(self.y1-other.y1)**2+(self.z1-other.z1)**2)
        return distance
    
def knn4(ind, k, liste):
                #trouver les k plus proches voisins de individus
    tab_distance=[]
    for d in liste: 
        dist=ind.distance(d)
        tab_distance.append((dist, d.categorie))
    tab_distance.sort(key=lambda x:x[0])  #trie en fonction de la distance
    #print(tab_distance)
                #chercher les k premiers individus
    tab=tab_distance[:k]
    c = Counter()
    cat=[]
    for i in tab:
        indiv=i[1]
        if indiv in cat:
            c[indiv]+=1
        else:
            cat.append(indiv)
            c[indiv]+=1
    m=max(c)        # m est la catégorie de l'individu max
    return m


def rechercher_k4(pourcentage_test, Individu):
    data_test=[]
    data_app=[]
    for l in range(int(len(Individu)*pourcentage_test/100)):
        x=random.randint(0, len(Individu)-1)
        data_test.append(Individu[x])
        Individu.pop(x) # pour éviter de reselectionner le même individu
    for j in range(len(Individu)-int(len(Individu)*pourcentage_test/100)):
        y=random.randint(0, len(Individu)-1)
        data_app.append(Individu[y])
        Individu.pop(y)
    Liste_k=[]
    for k in range(1,10):
        mat=np.zeros((4,4))
        for d in data_test:
            c=knn4(d,k,data_app) 
            if d.categorie=="0":  # remplir la matrice de confusion
                if c=="0": 
                    mat[0][0]+=1 
                elif c=="1":  
                    mat[1][0]+=1
                elif c=="2":  
                    mat[2][0]+=1
                elif c=="3":  
                    mat[3][0]+=1
            if d.categorie=="1":  
                if c=="0":  
                    mat[0][1]+=1
                elif c=="1": 
                    mat[1][1]+=1 
                elif c=="2":  
                    mat[2][1]+=1
                elif c=="3":  
                    mat[3][1]+=1
            if d.categorie=="2":  
                if c=="0": 
                    mat[0][2]+=1 
                elif c=="1":  
                    mat[1][2]+=1
                elif c=="2":  
                    mat[2][2]+=1
                elif c=="3":  
                    mat[3][2]+=1
            if d.categorie=="3":  
                if c=="0": 
                    mat[0][3]+=1 
                elif c=="1":  
                    mat[1][3]+=1
                elif c=="2":  
                    mat[2][3]+=1
                elif c=="3":  
                    mat[3][3]+=1
        #print(mat)
        c1=mat[:,0]
        if c1[0]==0: 
            c1[0]=1     # pour éviter la division par 0
        x1=np.sum(c1)/c1[0]
        c2=mat[:,1]
        if c2[1]==0:
            c2[1]=1
        x2=np.sum(c2)/c2[1]
        c3=mat[:,2]
        if c3[2]==0:
            c3[2]=1
        x3=np.sum(c3)/c3[2]
        c4=mat[:,3]
        if c4[3]==0:
            c4[3]=1
        x4=np.sum(c4)/c4[3]
        Liste_k.append(x1+x2+x3+x4) 
    mini=Liste_k[0]
    indice=0
    for i in range(len(Liste_k)): #selectionner la meilleur valeur de k (celle qui a le moins d'erreur dans sa matrice de confusion)
        if Liste_k[i]<=mini:
            mini=Liste_k[i]
            indice=i
    return indice+1 # meilleur valeur de k


fichier2=open("C:\\Users\\aches\\Documents\\ESILV\\A3\\Info\\DIA\\data.txt","r")
Individu2=[]
for ligne in fichier2:
    ligne=ligne.strip('\n')
    L=ligne.split(";")
    i=individu2(float(L[0]),float(L[1]),float(L[2]),float(L[3]),float(L[4]),float(L[5]),float(L[6]),L[7])  
    Individu2.append(i)
    
fichier3=open("C:\\Users\\aches\\Documents\\ESILV\\A3\\Info\\DIA\\pretest.txt","r")
Individu3=[]
for ligne in fichier3:
    ligne=ligne.strip('\n')
    L=ligne.split(";")
    i=individu3(float(L[0]),float(L[1]),float(L[2]),float(L[3]),float(L[4]),float(L[5]),float(L[6]),L[7])  
    Individu3.append(i)
    
fichier4=open("C:\\Users\\aches\\Documents\\ESILV\\A3\\Info\\DIA\\finalTest.txt","r")
Individu4=[]
for ligne in fichier4:
    ligne=ligne.strip('\n')
    L=ligne.split(";")
    i=individu4(float(L[0]),float(L[1]),float(L[2]),float(L[3]),float(L[4]),float(L[5]),float(L[6]))  
    Individu4.append(i)
    
BDD=Individu2+Individu3
n1=len(BDD)
n2=len(Individu4)

#test=individu4(5.7,2.9,4.2,1.3,4,5,7)
#t=knn4(test,rechercher_k4(int(100*n1/(n2+n1)), BDD),BDD)
#print("L'algorithme KNN renvoie: ",t)

# 1ère approche en faisant la méthode de rechercher_k pour calculer knn avecla meilleur valeur de k

fichier5=open("C:\\Users\\aches\\Documents\\ESILV\\A3\\Info\\DIA\\Sasha_Rommelfangen_Aymeric_Chesterikoff_groupeJ.txt","w")

k=rechercher_k4(int(100*n2/(n2+n1)), BDD) # On détermine la meilleur valeur de k avec le % de valeur de test que l'on va réalisé par rapport au valeur déjà connu dans la BDD
print(k)

for i in Individu4:
    predictioncategorie=knn4(i,k,BDD)
    fichier5.write(predictioncategorie + "\n")
    
# 2ème approche en faisant la valeur princpale trouvé pour 10 valeurs de k

fichier6=open("C:\\Users\\aches\\Documents\\ESILV\\A3\\Info\\DIA\\Sasha_Rommelfangen_Aymeric_Chesterikoff_groupeJ2.txt","w")

R=[]
for i in Individu4:
    predictioncategorie=knn4(i,1,BDD)
    R.append(predictioncategorie)
    predictioncategorie=knn4(i,2,BDD)
    R.append(predictioncategorie)
    predictioncategorie=knn4(i,3,BDD)
    R.append(predictioncategorie)
    predictioncategorie=knn4(i,4,BDD)
    R.append(predictioncategorie)
    predictioncategorie=knn4(i,5,BDD)
    R.append(predictioncategorie)
    predictioncategorie=knn4(i,6,BDD)
    R.append(predictioncategorie)
    predictioncategorie=knn4(i,7,BDD)
    R.append(predictioncategorie)
    predictioncategorie=knn4(i,8,BDD)
    R.append(predictioncategorie)
    predictioncategorie=knn4(i,9,BDD)
    R.append(predictioncategorie)
    predictioncategorie=knn4(i,10,BDD)
    R.append(predictioncategorie)
    
Corr=[]
for k in range(0,len(R),10):
    if R[k]==R[k+1]==R[k+2]==R[k+3]==R[k+4]==R[k+5]:
        Corr.append(R[k])
    elif R[k+6]==R[k+1]==R[k+2]==R[k+3]==R[k+4]==R[k+5]:
        Corr.append(R[k+6])
    elif R[k+6]==R[k+7]==R[k+2]==R[k+3]==R[k+4]==R[k+5]:
        Corr.append(R[k+6])
    elif R[k+6]==R[k+7]==R[k+8]==R[k+3]==R[k+4]==R[k+5]:
        Corr.append(R[k+6]) 
    elif R[k+6]==R[k+7]==R[k+8]==R[k+9]==R[k+4]==R[k+5]:
        Corr.append(R[k+6])
    else: # Les cas non trait�s (moins de 6 valeurs identiques), on priorise la premi�re valeur de k car on est surement a une zone fronti�re
        Corr.append(R[k])

for i in range(len(Corr)):
    fichier6.write(Corr[i]+"\n")
    
fichier2.close()
fichier3.close()
fichier4.close()
fichier5.close()
fichier6.close()