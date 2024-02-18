from math import inf
from collections import Counter
import itertools
from time import time

TIME_LIMIT = 1

#fonction qui prend les coordonnées x et y (ligne et colonne) 
#d'une case dans la grille de 9x9 et renvoie l'index correspondant dans la représentation linéaire
#de la grille
def Index(x, y):
    x -= 1
    y -= 1
    return ((x//3)*27) + ((x % 3)*3) + ((y//3)*9) + (y % 3)

#fonction qui renvoie le numéro du sous-morpion auquel appartient la case avec les coordonnées 
#x et y
def Box(x, y):
    return Index(x, y) // 9

# fonction quirenvoie l'index du prochaine sous morpion à jouer, en fonction de l'index actuel i
def Next(i):
    return i % 9

#fonction qui renvoie la liste des indices des cases dans le sous morpion
def Indices(b):
    return list(range(b*9, b*9 + 9))

# fonction qui affiche l'état actuel de la grille de jeu
def Board(state):
    for row in range(1, 10):
        row_str = ["|"]
        for col in range(1, 10):
            row_str += [state[Index(row, col)]]
            if (col) % 3 == 0:
                row_str += ["|"]
        if (row-1) % 3 == 0:
            print("-"*(len(row_str)*2-1))
        print(" ".join(row_str))
    print("-"*(len(row_str)*2-1))

# fonction qui renvoie l'état de la grille après avoir effectué le mouvement du joueur
def Result(state, move, player):
    if not isinstance(move, int):
        move = Index(move[0], move[1])
    return state[: move] + player + state[move+1:]

#fonction qui vérifie si l'un des joueurs a gagné le sous-morpion
def Check_Small_Box(box_str):
    global possible_goals
    for idxs in possible_goals:
        (x, y, z) = idxs
        if (box_str[x] == box_str[y] == box_str[z]) and box_str[x] != ".":
            return box_str[x]
    return "."

# fonction qui vérifie si l'un des joueurs a gagné un sous-morpion ou si la grille de jeu est 
#pleine. Elle renvoie une liste de l'état de chaque sous morpion

def Terminal_Test(state):
    temp_box_win = ["."] * 9
    for b in range(9):
        idxs_box = Indices(b)
        box_str = state[idxs_box[0]: idxs_box[-1]+1]
        temp_box_win[b] = Check_Small_Box(box_str)
    return temp_box_win

# fonction qu renvoie les indices des cases dans le sous morpion suivant à jouer, 
#en fonction du dernier mouvement effectué

def Actions(last_move):
    global box_won
    if not isinstance(last_move, int):
        last_move = Index(last_move[0], last_move[1])
    box_to_play = Next(last_move)
    idxs = Indices(box_to_play)
    if box_won[box_to_play] != ".":
        pi_2d = [Indices(b) for b in range(9) if box_won[b] == "."]
        possible_indices = list(itertools.chain.from_iterable(pi_2d))
    else:
        possible_indices = idxs
    return possible_indices

#fonction qui génère une liste de tous les états possibles après le prochain coup pour le joueur

def Successeurs(state, player, last_move):
    succ = []
    moves_idx = []
    possible_indexes = Actions(last_move)
    for idx in possible_indexes:
        if state[idx] == ".":
            moves_idx.append(idx)
            succ.append(Result(state, idx, player))
    return zip(succ, moves_idx)
 
#fonction qui affiche les successeurs possibles de l'état actuel du jeu pour le joueur    

def AfficheSuccessors(state, player, last_move):
    for st in Successeurs(state, player, last_move):
        Board(st[0])
 
#fonction qui renvoie le joueur adverse de celui donné en argument   
 
def Opponent(p):
    return "O" if p == "X" else "X"
 
# Cette fonction évalue l'état d'une boîte (sous-morpion) donnée en attribuant un score en 
#fonction des combinaisons possibles de victoire.

def Evaluate_Small_Box(box_str, player):
    global possible_goals
    score = 0
    three = Counter(player * 3)
    two = Counter(player * 2 + ".")
    one = Counter(player * 1 + "." * 2)
    three_opponent = Counter(Opponent(player) * 3)
    two_opponent = Counter(Opponent(player) * 2 + ".")
    one_opponent = Counter(Opponent(player) * 1 + "." * 2)
    for idxs in possible_goals:
        (x, y, z) = idxs
        current = Counter([box_str[x], box_str[y], box_str[z]])
        if current == three:
            score += 100
        elif current == two:
            score += 10
        elif current == one:
            score += 1
        elif current == three_opponent:
            score -= 100
            return score
        elif current == two_opponent:
            score -= 10
        elif current == one_opponent:
            score -= 1
    return score

# fonction qui évalue l'état global du jeu en attribuant un score en fonction de l'état de chaque sous-morpion

def Evaluate(state, last_move, player):
    global box_won
    score = 0
    score += Evaluate_Small_Box(box_won, player) * 200
    for b in range(9):
        idxs = Indices(b)
        box_str = state[idxs[0]: idxs[-1]+1]
        score += Evaluate_Small_Box(box_str, player)
    return score
 
#fonction implémente l'algorithme MiniMax avec élagage alpha-bêta pour déterminer 
#le meilleur coup à jouer
   
 
def MiniMax(state, last_move, player, depth, s_time):
    succ = Successeurs(state, player, last_move)
    best_move = (-inf, None)
    for s in succ:
        val = Tour_Min(s[0], s[1], Opponent(player), depth-1, s_time,
                       -inf, inf)
        if val > best_move[0]:
            best_move = (val, s)
    return best_move[1]

#fonction auxiliaire pour l'algorithme MiniMax. 
#Elle représente le tour du joueur MAX (l'IA) et cherche à maximiser le score

def Tour_Max(state, last_move, player, depth, s_time, alpha, beta):
    global box_won
    if depth <= 0 or Check_Small_Box(box_won) != ".":# or time() - s_time >= 20:
        return Evaluate(state, last_move, player)
    succ = Successeurs(state, player, last_move)
    for s in succ:
        val = Tour_Min(s[0], s[1], Opponent(player), depth-1, s_time,
                       alpha, beta)
        if alpha < val:
            alpha = val
        if alpha >= beta:
            break
    return alpha

#fonction auxiliaire pour l'algorithme MiniMax. 
#Elle représente le tour du joueur MIN (l'adversaire) et cherche à minimiser le score

def Tour_Min(state, last_move, player, depth, s_time, alpha, beta):
    global box_won
    if depth <= 0 or Check_Small_Box(box_won) != ".":# or time() - s_time >= 10:
        return Evaluate(state, last_move, Opponent(player))
    succ = Successeurs(state, player, last_move)
    for s in succ:
        val = Tour_Max(s[0], s[1], Opponent(player), depth-1, s_time,
                       alpha, beta)
        if val < beta:
            beta = val
        if alpha >= beta:
            break
    return beta

#vérifie si un mouvement est valide dans l'état actuel du jeu

def Sortie_Valide(state, move):
    global box_won
    if not (0 < move[0] < 10 and 0 < move[1] < 10):
        return False
    if box_won[Box(move[0], move[1])] != ".":
        return False
    if state[Index(move[0], move[1])] != ".":
        return False
    return True

#permet à l'utilisateur de saisir son mouvement. Elle prend en compte le dernier mouvement 
#effectué par l'ia pour restreindre les mouvements possibles si un sous morpion 
#a déjà été remporté

def Prendre_Entree(state, bot_move):
    all_open_flag = False
    if bot_move == -1 or len(Actions(bot_move)) > 9:
        all_open_flag = True
    if all_open_flag:
        print("Allez où vous voulez !")
    else:
        box_dict = {1: "Coin supérieur gauche", 2: "Au-dessus du centre", 3: "Coin supérieur droit",
                    4: "A gauche du centre", 5: "Centre", 6: "Centre droit",
                    7: "Coin inférieur gauche", 8: "En dessous du centre", 9: "Le coin inférieur droit"}
        print("Où voulez-vous placer votre 'X' ? DOIT ÊTRE DANS LE Morpion : ~"
              + box_dict[Next(bot_move)+1])
    x = int(input("Ligne = "))
    if x == -1:
        raise SystemExit
    y = int(input("Colonne = "))
    print("")
    if bot_move != -1 and Index(x, y) not in Actions(bot_move):
        raise ValueError
    if not Sortie_Valide(state, (x, y)):
        raise ValueError
    return (x, y)

#Explicite. 

def Demander_Choix_Joueur():
    while True:
        choix = input("Voulez-vous commencer ? (Oui/Non) : ")
        choix = choix.lower()
        if choix == "oui":
            return True
        elif choix == "non":
            return False
        else:
            print("Veuillez entrer une réponse valide (Oui/Non).")

# fonction principale qui gère le déroulement du jeu

def Play(state="." * 81, depth=20):
    global box_won, possible_goals
    possible_goals = [(0, 4, 8), (2, 4, 6)]
    possible_goals += [(i, i+3, i+6) for i in range(3)]
    possible_goals += [(3*i, 3*i+1, 3*i+2) for i in range(3)]
    box_won = Terminal_Test(state)
    Board(state)

    joueur_commence = Demander_Choix_Joueur()
    if joueur_commence:
        bot_move = -1
    else:
        print("L'ordinateur commence.")
        print("Attendez un moment...")
        s_time = time()
        state, bot_move = MiniMax(state, -1, "O", depth, s_time)
        Board(state)
    while True:
        try:
            user_move = Prendre_Entree(state, bot_move)
        except ValueError:
            print("ENTRER D'AUTRES VALEURS")
            Board(state)
            continue
        except SystemError:
            print("Jeu d'erreur arrêté !")
            break
        user_state = Result(state, user_move, "X")
        Board(user_state)
        box_won = Terminal_Test(user_state)
        game_won = Check_Small_Box(box_won)
        if game_won != ".":
            print("Félicitation, vous avez gagné le morpion !")
            break
        print("Attendez un moment...")
        s_time = time()
        bot_state, bot_move = MiniMax(user_state, user_move, "O", depth, s_time)
        print("L'ordinateur a mis 'O' dans", bot_move, "\n")
        Board(bot_state)
        state = bot_state
        box_won = Terminal_Test(bot_state)
        game_won = Check_Small_Box(box_won)
        if game_won != ".":
            break
    if game_won == "X":
        print("Vous avez gagné ce cadre ! sélectionnez-en un autre pour continuer à jouer")
    else:
        print("Vous avez perdu ce quadrant !, sélectionnez-en un autre pour continuer à jouer")
    if game_won == "O":
        print("Félicitation, vous avez gagné le morpion !")
    return state

#Fonction qui déclenche le code.

if __name__ == "__main__":
    INITIAL_STATE = "." * 81
    final_state = Play(INITIAL_STATE, depth=5)