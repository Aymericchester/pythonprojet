'''TD EDP'''

import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation


print("2D heat equation solver ")

Domaine = 100 # a  modifier
meshSize = 1 # a ne pas toucher

max_iter_time = 2500 #a  modifier

alpha = 1 #  a modifier : comportement de la solution

# schema explicite : CFL doit etre respectee


delta_t=(meshSize**2)/(4*alpha)

gamma = (alpha*delta_t)/(meshSize**2)

# Initialisation de la solution : la grille de T(k,i,j)
# ou la 1ere composante est le temps, la seconde est x ,enfin la 3eme compossante correspond a y

T=np.empty((max_iter_time,Domaine,Domaine))
Errk=np.zeros(max_iter_time)
Temps=np.zeros(max_iter_time)
# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# Initialisation condition initial
# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
T_initial = 0
TOL=10

# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# valeurs qu’on impose sur les bords du domaine
# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−

T_top = 100.0
T_left = 0.0
T_bottom = 0.0
T_right = 0.0

# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# Condition initiale
# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
T.fill(T_initial)
# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# Conditions aux limite de type Dirichlet
# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
T[:,(Domaine-1):,:]=T_top
T[:,:,:1] = T_left
T[:,:1,1:] = T_bottom
T[:,:,(Domaine-1):] = T_right


def ResolutionEquationDeLaChaleur(T):
    errk=0
# 1ere boucle sur le temps
    for k in range(0, max_iter_time-1,1):
        errk=0
# 2eme et 3eme boucles sur le maillage
        for i in range(1,Domaine-1,meshSize):
            for j in range(1,Domaine-1,meshSize):
 # Schema explicite pour l'equation de chaleur avec second membre nul!
                 T[k+1,i,j] = gamma*(T[k][i+1][j] + T[k][i-1][j] + T[k][i][j+1] + T[k][i][j-1] - 4*T[k][i][j]) + T[k][i][j]
                 errk=errk+delta_t*((T[k+1,i,j]-T[k,i,j])**2)
        Errk[k+1]=errk**0.5
        Temps[k+1]=Temps[k]+delta_t
    return T,Errk,Temps

def calculate(u, Err, temp):
    k=0
    while True:
        er=0
        for i in range(1, Domaine-1, meshSize):
            for j in range(1, Domaine-1, meshSize):
                u[k + 1, i, j] = gamma * (u[k][i+1][j] + u[k][i-1][j] + u[k][i][j+1] + u[k][i][j-1] - 4*u[k][i][j]) + u[k][i][j]
                er = er + delta_t* (u[k + 1, i, j]-u[k , i, j])**2
        Err[k+1]=er**0.5
        temp[k+1]= temp[k]+delta_t
        k+=1
        if Err[k]<TOL or k==2001:
             break
        print("nb iteration:", k)
    return u, Err, temp

# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# Output
# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
def plotheatmap(T_k,k):
# Un peu de netoyage
    plt.clf()
    plt.title(f"La temperature au temps t = {k*delta_t:.3f} ")
    plt.xlabel("x")
    plt.ylabel("y")
# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# plot de T_k (T au temps t_k )
# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−

    plt.pcolormesh(T_k,cmap=plt.cm.jet,vmin=0,vmax=100)
    plt.colorbar()
    return plt
# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# Faire le calcul ici
# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
#u, err, temps =ResolutionEquationDeLaChaleur(T)
u, err, temps =calculate(T,Errk,Temps)
def animate(k):
    plotheatmap(T[k],k)

plt.plot(temps,err)
plt.show()

    
anim = animation.FuncAnimation(plt.figure(),animate,interval=1,frames=max_iter_time,repeat=False)
anim.save("heat_equation_solution.gif", writer="pillow")

print( "C’est  bien  fini , vas  voir  le  resultat!" )