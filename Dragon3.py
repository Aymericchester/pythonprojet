import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

print("2D heat equation solver")

# Définition des paramètres

Domaine = 100 # A modifier
meshSize = 1 # à ne pas toucher 

max_iter_time = 300 # à modifier 

alpha = 3 # à modifier, comportement de la solution

# schema explicite : CFL doit etre respectee
delta_t = (meshSize**2) / (4 * alpha)

gamma = (alpha * delta_t) / (meshSize**2)

T = np.empty((max_iter_time, Domaine, Domaine))
Errk = np.zeros(max_iter_time)
Temps = np.zeros(max_iter_time)

T_initial = 0
TOL = 1e-7

#Conditions aux limites

T_top = 0.0
T_left = 0.0
T_bottom = 0.0
T_right = 0.0

# Initialisation du tableau de la solution numérique

T.fill(T_initial)
T[:, (Domaine - 1):, :] = T_top
T[:, :, :1] = T_left
T[:, :1, 1:] = T_bottom
T[:, :, (Domaine - 1):] = T_right

# Position initiale et température du dragon. 

x0 = 1
t0 = 0
v = 20

#Définition de la solution analytique.

def analytic_solution(x, t, n):
    Tn = np.zeros_like(x)
    for i in range(1, n+1):
        Tn += np.sin(i * np.pi * x) * np.exp(- (i * np.pi)**2 * alpha * t)
    return Tn

# Impulsion de Dirac pour représenter le feu du dragon.

def impulsion_dirac(x, x0):
    if x == x0:
        return 1e5
    else:
        return 0

# Ajout de la chaleur du dragon dans le domaine.

for i in range(Domaine):
    T[t0, i, x0] += impulsion_dirac(i, x0)

#Résolution de l'équation de la chaleur.

def ResolutionEquationDeLaChaleur(T):
    errk = 0
    for k in range(0, max_iter_time - 1, 1):
        errk = 0
        x0 = 10

        x0 = x0 + v * delta_t

        for i in range(1, Domaine - 1, meshSize):
            for j in range(1, Domaine - 1, meshSize):
                T[k + 1, i, j] = gamma * (T[k][i + 1][j] + T[k][i - 1][j] + T[k][i][j + 1] + T[k][i][j - 1] - 4 * T[k][i][j]) + T[k][i][j]
                errk = errk + delta_t * ((T[k + 1, i, j] - T[k, i, j])**2)
        
        # Ajout de la chaleur du dragon dans le domaine.

        for i in range(Domaine):
            T[k + 1, i, int(x0)] += impulsion_dirac(i, x0)

        # Itération de l'erreur et du temps de propagation du feu. 

        Errk[k + 1] = errk**0.5
        Temps[k + 1] = Temps[k] + delta_t

    return T, Errk, Temps

# Affectation de la température, de l'erreur et de l'évolution de la chaleur en fonction du temps.

u, err, temps = ResolutionEquationDeLaChaleur(T)

# Fonction permettant la création de la carte thermique. 

def plotheatmap(T_k, k):
    plt.clf()
    plt.title(f"La temperature au temps t = {k * delta_t:.3f} en K")
    plt.xlabel("x (dam)")
    plt.ylabel("y (dam)")
    im = plt.imshow(T_k, cmap=plt.cm.jet, vmin=0, vmax=3000)
    plt.colorbar(im)
    plt.show()

# Fonction qui permet de constater l'évolution de la température venant des flammes du dragon. 

def animate(k):
    plotheatmap(T[k], k)

animation.FuncAnimation(plt.figure(), animate, interval=1, frames=max_iter_time//10, repeat=False).save("heat_equation_solution.gif", writer="pillow")

# Tracé de l'évolution de l'erreur quadratique totale de la solution en fonction du temps. 

plt.plot(temps, err)
plt.title("Evolution de l'erreur quadratique totale de la solution")
plt.show()

# Affichage de la solution numérique et de la solution analytique

# Solution numérique. 

plt.figure()
x = np.linspace(0, Domaine, Domaine)
t = np.linspace(0, max_iter_time * delta_t, max_iter_time)

n = 100
Tn = analytic_solution(x, t[-1], n)
plt.plot(x, T[-1, :, int(x0)], label='Tracé de la solution numérique')
plt.plot(x, Tn, label=f"Solution analytique pour n = {n}")

# Echelonnage du graphe. 

plt.legend()
plt.xlabel('x')
plt.ylabel('Temperature')
plt.show()

print("C’est bien fini, vas voir le resultat!")