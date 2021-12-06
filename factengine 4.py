import string
from typing import List, Tuple, Dict
from random import randint
from time import sleep
from math import sin, pi
import dessin
import fin
# Avec tout ce que j'ai commanté dans ce programme, j'espère bien que les attentes du professeur seront réalisées. J'ai pas fait tout ça pour que je survive au corona !


class Personnage:
    """-nom
    -vie
    -mana
    -energie
    -boisson
    -nouriture
    -inventaire : liste des objets
    -argent
    -deja_vu : liste des coordonnées des objets déjà vu
    -option_largeur
    _option_hauteur"""

    def __init__(self):
        self.nom = "DeFacto"
        self.vie = 8
        self.mana = 8
        self.energie = 8
        self.boisson = 8
        self.nouriture = 8
        self.inventaire = []
        self.argent = 0
        self.deja_vu = []
        self.option_largeur = 119
        self.option_hauteur = 29


mouvement_deplacement = ('z', 'q', 's', 'd')
touche_deplacement = {'z': "haut", 'q': "gauche", 's': "bas", 'd': "droite"}
objet_avec_colision = ('#', '-', '|', ' ', '\'', ',')
objet_avec_interaction = ['P', 'C', '?', '^', 'v', 'E', '$']
passage_direction = {(7, 0, 5, "5_5_5"): (6, 7, 5, "5_4_5", "Clef blanche"), (6, 7, 5, "5_4_5"): (7, 0, 5, "5_5_5", "Clef blanche"),
                     (9, 11, 5, "5_5_5"): (3, 2, 6, "5_5_6", "Clef blanche"), (3, 2, 6, "5_5_6"): (9, 11, 5, "5_5_5", "Clef blanche"),
                     (0, 7, 5, "5_5_5"): (9, 7, 5, "4_5_5", "Clef blanche"), (9, 7, 5, "4_5_5"): (0, 7, 5, "5_5_5", "Clef blanche"),
                     (6, 2, 5, "debut"): (1, 3, 5, "4_5_5", "Clef blanche"),
                     (6, 0, 5, "5_4_5"): (3, 18, 5, "labyrinthe 1", "Clef blanche"), (3, 18, 5, "labyrinthe 1"): (6, 0, 5, "5_4_5", "Clef blanche"),
                     (9, 9, 5, "5_5_5"): (9, 9, 5, "5_5_5", "Clef étrange"),
                     (5, 6, 6, "5_5_6"): (5, 6, 6, "5_5_6", "Clef bleu"),
                     (2, 6, 5, "4_5_5"): (2, 6, 5, "4_5_5", "Clef blanche"),
                     (2, 9, 5, "4_5_5"): (2, 9, 5, "4_5_5", "Clef blanche"),
                     (5, 9, 5, "4_5_5"): (5, 9, 5, "4_5_5", "Clef blanche"),
                     (13, 7, 5, "5_5_5"): (0, 7, 5, "6_5_5", "Clef blanche"), (0, 7, 5, "6_5_5"): (13, 7, 5, "5_5_5", "Clef blanche"),
                     (0, 7, 5, "4_5_5"): (6, 7, 5, "3_5_5", "Clef rouge"), (6, 7, 5, "3_5_5"): (0, 7, 5, "4_5_5", 'Clef rouge'),
                     (4, 3, 5, "4_5_5"): (4, 3, 5, "4_5_5", "Clef bleu"),
                     (0, 7, 5, '3_5_5'): (9, 7, 5, '2_5_5', 'Clef beta'), (9, 7, 5, "2_5_5"): (0, 7, 5, '3_5_5', 'Clef beta'),
                     (7, 0, 5, '2_5_5'): (7, 6, 5, '2_4_5', 'Clef beta'), (7, 6, 5, '2_4_5'): (7, 0, 5, '2_5_5', 'Clef beta'),
                     (1, 12, 5, '2_5_5'): (1, 0, 5, '2_6_5', 'Clef alpha'), (1, 0, 5, '2_6_5'): (1, 12, 5, '2_5_5', 'Clef alpha'),
                     (4, 0, 5, '2_4_5'): (4, 10, 5, '2_3_5', 'Clef gamma'), (4, 10, 5, '2_3_5'): (4, 0, 5, '2_4_5', 'Clef gamma'),
                     (8, 5, 5, '2_3_5'): (8, 5, 5, '2_3_5', 'Clef gamma'),
                     (3, 13, 5, '5_5_5'): (3, 0, 5, '5_6_5', 'Clef bleu'), (3, 0, 5, '5_6_5'): (3, 13, 5, '5_5_5', 'Clef bleu')
                     }


def boite_dialogue(texte, question, personnage):
    """ Fonction faisant une boite de dialogue, elle fonctionne avec de la magie noire :
    entrées : texte (chose à afficher), question (texte pour passer à la suite) ;
    sorties : réponse à la question."""
    attention = False
    paragraphes = []
    paragraphe = ''
    reponse = ''
    for carac in texte:
        if carac == '\\':
            attention = True
        elif carac == '$' and attention:
            attention = False
            paragraphes.append(paragraphe)
            paragraphe = ''
        else:
            if attention:
                paragraphe += '\\' + carac
            else:
                paragraphe += carac
            attention = False
    paragraphes.append(paragraphe)
    for paragraphe in paragraphes:
        aff = "\n  "
        longueur = 0
        longueur_max = 0
        texte_sergmente = []
        ligne = ""
        longueur_sans_retour = 0
        longueur_sans_retour_max = 0
        for carac in paragraphe:
            if carac == '\n':
                if longueur_sans_retour > longueur_sans_retour_max:
                    longueur_sans_retour_max = longueur_sans_retour
                longueur_sans_retour = 0
            else:
                longueur_sans_retour += 1
        if longueur_sans_retour > longueur_sans_retour_max:
            longueur_sans_retour_max = longueur_sans_retour
        if longueur_sans_retour_max > personnage.option_largeur - 6:
            mot_reserve = ""
            for carac in paragraphe:
                longueur += 1
                if carac == '\n':
                    if longueur > longueur_max:
                        longueur_max = longueur
                    texte_sergmente.append(ligne[0: -1])
                    longueur = len(mot_reserve)
                    ligne = ""
                else:
                    mot_reserve += carac
                if longueur == (personnage.option_largeur - 6):
                    if longueur > longueur_max:
                        longueur_max = longueur
                    texte_sergmente.append(ligne[0: -1])
                    longueur = len(mot_reserve)
                    ligne = ""
                elif carac in ' ':
                    ligne += mot_reserve
                    mot_reserve = ''
            ligne += mot_reserve
            texte_sergmente.append(ligne)
        else:
            # Sépare le texte en ligne si il y a des \n
            for carac in paragraphe:
                if carac == '\n':
                    if longueur > longueur_max:
                        longueur_max = longueur
                    longueur = 0
                    texte_sergmente.append(ligne)
                    ligne = ""
                else:
                    longueur += 1
                    ligne += carac
            texte_sergmente.append(ligne)
        # Calcule la longueur maximal
        if longueur > longueur_max:
            longueur_max = longueur
        longueur_max += 2
        # L'affichage
        aff += f"\n  {'_' * longueur_max}\n"
        for ligne in texte_sergmente:
            aff += f" | {ligne} {' ' * (longueur_max - len(ligne) - 2)}|\n"
        aff += f" |{'_' * longueur_max}|"
        aff += "\n" * ((personnage.option_hauteur - 4) - len(texte_sergmente))
        print(aff)
        reponse = input(question)
    return reponse


def balance(norme_1, nom_1, norme_2, nom_2, question, personnage):
    """Fonction s'occupant de l'affichage d'une balance (voir dessin.py :
    Entrée : nom (nom du matériaux), norme (la masse), question (posé), personnage (caractéristique);
    Sortie : réponse à la question (str)"""
    def sign(x):
        if x < 0:
            return -1
        if x == 0:
            return 0
        return 1
    poids = sign(norme_2 - norme_1)
    if poids == 0:
        aff = dessin.balance_0
    elif poids == -1:
        aff = dessin.balance_1
    else:
        aff = dessin.balance_2
    nom_1 += ' '*(9 - len(nom_1))
    nom_2 += ' '*(9 - len(nom_2))
    aff += f'\n _________||_________\n|{nom_1}||{nom_2}|\n|_________||_________|'
    aff += '\n' * (personnage.option_hauteur - 9)
    print('\n' + aff + question, end='')
    return input()


def fini(personnage):
    for image in fin.image:
        dessin = ''
        for ligne in image:
            dessin += ligne + '\n'
        boite_dialogue(dessin, '[Entrer] pour continuer', personnage)


def generique(personnage):
    aff = '\n' * personnage.option_hauteur
    print(aff)
    t = 16/personnage.option_hauteur
    for ligne in fin.generique:
        l = len(ligne)
        print(f'{" "* ((personnage.option_largeur - l)//2)}{ligne}')
        sleep(t)
    for i in range(len(fin.logo)):
        print(fin.logo[i])
        sleep(t)
    for _ in range(personnage.option_hauteur):
        print()
        sleep(t)


def enigme_1(personnage):
    """ Fonction de l'énigme 1 :
    entrée : personnage (les caractéristiques) ;
    sortie : Booléen (False : raté, True : gagné)."""
    def resolu(dico):
        """Fonction vérifiant si c'est réussi :
        entrée : Dictionnaire (contenant les valeurs de chaque case) ;
        sortie : Booléen (False : non résolu, True : résolu)."""
        c0 = dico['A']
        c1 = dico['B']
        c2 = dico['C']
        c3 = dico['D']
        c4 = dico['E']
        c5 = dico['F']
        c6 = dico['G']
        c7 = dico['H']
        # Liste des cases voisines (un dico aurait été mieux), la case concerné puis les cases voisines, les cases allant de 0 à 7
        liste_case_voisine = [(c0, [c1, c2, c3, c4]), (c1, [c3, c4, c5]),
                              (c2, [c3, c6]), (c3, [c4, c6, c7]), (c4, [c5, c6, c7]), (c5, [c7]),
                              (c6, [c7])]
        for test in liste_case_voisine:
            case_concernee, cases_voisines = test
            for case_tester in cases_voisines:
                # vérifie pour les valeurs x-1, x et x+1
                for i in range(3):
                    j = i-1
                    if case_tester + j == case_concernee or case_concernee not in (0, 1, 2, 3, 4, 5, 6, 7):
                        return False
        cases = (c0, c1, c2, c3, c4, c5, c6, c7)
        for i in range(len(cases)):
            for j in range(i+1, len(cases)):
                if i == j:
                    return False
        return True

    def affichage_e1(dico):
        """Fonction affichant l'énigme :
        Entrée : dictionnaire des cases;
        Sortie : un string de caractère."""
        aff_e1 = f"\n       ____ ____\n      | A{dico['A']} | B{dico['B']} |\n"
        aff_e1 += "  ____|____|____|____\n"
        aff_e1 += f" | C{dico['C']} | D{dico['D']} | E{dico['E']} | F{dico['F']} |\n"
        aff_e1 += " |____|____|____|____|\n"
        aff_e1 += f"      | G{dico['G']} | H{dico['H']} |\n"
        aff_e1 += "      |____|____|\n\n"
        return aff_e1
    fini = False
    lettre_case = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0}
    aide = True

    while not fini:
        aff = affichage_e1(lettre_case)
        aff += '\n' * (personnage.option_hauteur - 17)
        if aide:
            aff += "Indications :\n"
            aff += "Cette machine est composée de 8 cases faites en 2 parties.\n"
            aff += "La première partie est une lettre désignant le nom;\n"
            aff += "La seconde partie est le numéro associé allant de 0 à 7.\n"
            aff += "Chaque case a des voisines comprennant les mitoyennes et les cases en diagonales.\n"
            aff += "L'objectif est qu'aucune des cases n'aient une voisine ayant un numéro directement inferieur, égal ou superrieur.\n"
            aff += "Il faut aussi que chaque case ait un numéro unique."
            aff += "Exemple d'entrées : \"A1\", \"H7\".\n\n"
            aide = False
        else:
            aff += "\n\n\n\n\n\n\n[?] : aide, [q] : quitter\n"
        aff += "Entre la case à changer (lettre) puis le numéro que tu veux associer (0 à 7) : "
        print(aff, end='')
        entree = input().upper()
        if entree == '?':
            aide = True
        elif entree == 'Q':
            return False
        elif len(entree) == 2:
            lettre = entree[0]
            numero = entree[1]
            if numero in ('0', '1', '2', '3', '4', '5', '6', '7') and lettre in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'):
                lettre_case[lettre] = int(numero)
        fini = resolu(lettre_case)
    if "Clef bleu" not in personnage.inventaire:
        personnage.inventaire.append("Clef bleu")
        boite_dialogue("Tu as obtenu une Clef bleu", "[entrer] pour passer", personnage)
    else:
        boite_dialogue("Tu avais déjà la Clef bleu", "[entrer] pour passer", personnage)
    return True


def enigme_2(personnage):
    """Fonction de l'énigme 2 fonctionnant avec un cryptage, Cesar :
    Entrée : Personnage (Les caractéristiques) ;
    Sortie : Personnage."""
    lettre_nbr = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9, "k": 10, "l": 11, "m": 12, "n": 13, "o": 14, "p": 15, "q": 16, "r": 17, "s": 18, "t": 19, "u": 20, "v": 21, "w": 22, "x": 23, "y": 24, "z": 25}
    nbr_lettre = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h", 8: "i", 9: "j", 10: "k", 11: "l", 12: "m", 13: "n", 14: "o", 15: "p", 16: "q", 17: "r", 18: "s", 19: "t", 20: "u", 21: "v", 22: "w", 23: "x", 24: "y", 25: "z"}
    solution = "xs gojowg eis hi sggomsfowg !"
    
    def resolu(phrase):
        """Fonction verifiant la réponse du code César:
        entrée : String (chaine de caractère de la phrase) ;
        Sortie : Bolléen (True : réussi, False :raté.
        Spécificité : Fonctionne si l'on change la phrase."""
        reponse = ""
        for carac in phrase:
            if carac in lettre_nbr:
                reponse += nbr_lettre[(lettre_nbr[carac] - 12) % 26]
            else:
                reponse += carac
        if reponse == solution:
            return True
        else:
            return False

    while True:
        # Boucle à l'infini
        choix = boite_dialogue("Nato :\n Mon ami César me cache quelque chose, aide moi à decoder !\n Texte : \"xs gojowg eis hi sggomsfowg !\".\n [?] : aide   \n [q] : quitter", "Donne moi la phrase : ", personnage).lower()
        if choix == '?':  # Indice
            boite_dialogue("Nato :\n Je te conseil d'aller voir chez lui !\n Fait attention à la ponctuation.", "[entrer] pour continuer", personnage)
        elif choix == 'q':  # Pour quitter
            boite_dialogue("Nato :\n Reviens quand tu veux.", "[entrer] pour continuer", personnage)
            return personnage
        elif resolu(choix):  # Si l'on a trouvé
            boite_dialogue("Nato :\n Bien joué !\n Il est bien drôle...", "[entrer] pour continuer", personnage)
            if "Clef étrange" in personnage.inventaire:  # Si la clef est déjà là on la redonne pas
                boite_dialogue("Tu as déjà la Clef étrange", "[entrer] pour continuer", personnage)
            else:  # Donne la clef comme il ne l'a pas
                boite_dialogue("Tu as reçu une Clef étrange", "[entrer] pour continuer", personnage)
                personnage.inventaire.append("Clef étrange")
            return personnage
        else:
            boite_dialogue("Nato :\n Très bien... Mais c'est pas la bonne réponse...", "[entrer] pour continuer", personnage)


def enigme_3(x, y, z, carte_nom, personnage):
    if x == 11 and y == 6 and z == 5 and carte_nom == '6_5_5':
        if [11, 6, 5, '6_5_5'] in personnage.deja_vu:
            boite_dialogue('Ici il y avait la Clef alpha', '[entrer] pour continuer', personnage)
        else:
            boite_dialogue('Tu as obtenue la Clef alpha', '[entrer] pour continuer', personnage)
            personnage.inventaire.append('Clef alpha')
            personnage.deja_vu.append([11, 6, 5, '6_5_5'])
    return personnage


def enigme_4(personnage):
    onde_reponse = [-2, -5, -6, -5, -3, 1, 4, 7, 7, 5, 2, -1, -4, -4, -3, -1, 1, 3, 2, 0, -3]
    def affichage_e_4(a1, b1, a2, b2, e):

        def chiffre_x(x):
            if x == -10:
                return str(x)
            if x == 10:
                return ' ' + str(x)
            if x < 0:
                return ' ' + str(x)
            else:
                return '  ' + str(x)

        def espace(x):
            if x == 13:
                return '|'
            return ' '

        def indic_lat(y, a1, b1, a2, b2, e):
            ligne_info = {1: a1, 3: b1, 5: a2, 7: b2, 9: e}
            if y == 0:
                return 'Amplitude de "o" :'
            if y == 2:
                return 'Periode de "o" :'
            if y == 4:
                return 'Amplitude de "+" :'
            if y == 6:
                return 'Periode de "+" :'
            if y == 8:
                return 'Décalage de "+" :'
            if y in ligne_info:
                return '#' * (3 + ligne_info[y]) + '.' * (2 - ligne_info[y])
            return ''
        aff = ''
        aff += ' Y |       Onde 1 et Onde 2    |        Onde clef\n'
        aff += '      -10   -5    0    5   10  |-10   -5    0    5   10\n'
        aff += '        |    |    |    |    |  |  |    |    |    |    |\n'
        liste = []
        for y in range(0, 21):
            k = y - 10
            aff += chiffre_x(k)
            f = 5 * a1 * sin((b1 * k) / pi) + 15
            g = 5 * a2 * sin((b2 * k) / pi + e) + 15
            for x in range(60):
                if x == round(f):
                    aff += 'o'
                elif x == round(g):
                    aff += '+'
                elif x == round((g+f)/2 + 26):
                    aff += '#'
                elif x-41 == onde_reponse[y]:
                    aff += '.'
                else:
                    aff += espace(x-15)
            liste.append(round((g+f)/2 - 15))
            aff += indic_lat(y, a1, b1, a2, b2, e)
            aff += '\n'
        print(aff)
        return liste

    def resolue(liste):
        print(liste)
        print(onde_reponse)
        return liste == onde_reponse
    a1 = randint(-2, 2)
    b1 = randint(-2, 2)
    a2 = randint(-2, 2)
    b2 = randint(-2, 2)
    e = randint(-2, 2)
    while True:
        resultat = affichage_e_4(a1, b1, a2, b2, e)
        if resolue(resultat):
            if 'Clef beta' in personnage.inventaire:
                boite_dialogue('Tu as déjà la Clef beta', '[entrer] pour continuer', personnage)
            else:
                boite_dialogue('Tu as obtenue la Clef beta', '[entrer] pour continuer', personnage)
                personnage.inventaire.append('Clef beta')
            return personnage, 'Tu as trouvé la solution'
        aff = ''
        aff += '\n' * (29 - personnage.option_hauteur)
        aff += 'A gauche se trouve 2 ondes "o" et "+" qui une fois aditionné donne l\'onde "#".\n'
        aff += 'A droite se trouve l\'onde "#" et ".", cette dernière étant la clef de la porte.\n'
        aff += 'L\'objectif est que "#" doit avoir les mêmes valeurs que ".".\n'
        aff += 'Les valeurs doivent être comprises entre -2 et 2 et séparées par une virgule pour pouvoir les rentrées.\n'
        aff += 'A(o), P(o), A(+), P(+), D ou [q] : quitter : '
        print(aff, end='')
        reponse = input()
        if reponse == 'q':
            return personnage, 'Tu n\'as pas fini l\'énigme.'
        else:
            nbr_tirret_ou_espace = 0
            reponse_valable = False
            for carac in reponse:
                if carac in ('-', ' '):
                    nbr_tirret_ou_espace += 1
                if carac not in ('-', '0', '1', '2', ',', ' '):
                    break
            else:
                donnees = []
                if len(reponse) == 9 + nbr_tirret_ou_espace:
                    numero = ''
                    for carac in reponse:
                        if carac in (' ', ',') and len(numero) > 0:
                            if numero in ('-2', '-1', '0', '1', '2'):
                                donnees.append(int(numero))
                                numero = ''
                            else:
                                break
                        elif carac in ('-', '1', '2', '0'):
                            numero += carac
                    if numero in ('-2', '-1', '0', '1', '2'):
                        donnees.append(int(numero))
                if len(donnees) == 5:
                    reponse_valable = True
                    a1 = donnees[0]
                    b1 = donnees[1]
                    a2 = donnees[2]
                    b2 = donnees[3]
                    e = donnees[4]
            if not reponse_valable:
                alea = []
                for _ in range(5):
                    alea.append(randint(-2, 2))
                boite_dialogue(f'L\'entrée n\'est pas valable. Voici un exemple d\'entrée valable : {alea[0]}, {alea[1]}, {alea[2]}, {alea[3]}, {alea[4]}\nLes espaces ne sont pas important, mais les virgules si.\nA : amplitude (c\'est la hauteur)\nP : période (c\'est la largeur)\nD : décallage (c\'est l\'écart de l\'onde)', '[entrer] pour continuer', personnage)


def enigme_5(personnage):
    def affichage(liste, masse):
        def plateau(liste):
            aff = '| '
            espace = 0
            for bloc in liste:
                aff += f'{bloc} '
                espace += len(bloc) + 1
            aff += ' ' * (39 - espace) + '|'
            return aff

        entrer = 0
        if masse < p_pierre + 2 * p_verre + 2 * p_bois:
            entrer = 2
        elif masse == p_pierre + 2 * p_verre + 2 * p_bois:
            entrer = 1
        aff = '\n'
        if entrer == 1:
            aff += '\n' + plateau(liste) + f'-----| {n_bois} {n_bois} {n_verre} {n_verre} {n_pierre} |\nVisualisation :\n\n{dessin.balance_0}'
        elif entrer == 2:
            aff += plateau(liste) + '-_\n' + ' ' * 44 + '-_\n' + ' ' * 46 + f'-| {n_bois} {n_bois} {n_verre} {n_verre} {n_pierre} |\n\nVisualisation :\n{dessin.balance_2}'
        else:
            aff += ' ' * 45 + f'_-| {n_bois} {n_bois} {n_verre} {n_verre} {n_pierre} |\n' + ' ' * 43 + '_-\n' + plateau(liste) + f'-\n\nVisualisation :\n{dessin.balance_1}'
        return aff

    def resolue(masse):
        if masse == p_pierre + 2 * p_verre + 2 * p_bois:
            return True
        return False

    p_bois = 1
    p_verre = 1.5
    p_pierre = 6
    p_fer = 8
    n_bois = '[bois]'
    n_verre = '[verre]'
    n_pierre = '[pierre]'
    n_fer = '[fer]'
    n_p = {n_bois: p_bois, n_verre: p_verre, n_pierre: p_pierre, n_fer: p_fer}
    carac_n = {'b': '[bois]', 'v': '[verre]', 'p': '[pierre]', 'f': '[fer]'}
    l_poids = []
    masse = 0
    for bloc in l_poids:
        masse += n_p[bloc]
    while True:
        aff = affichage(l_poids, masse)
        aff += '\n' * (personnage.option_hauteur - 17) + '\nb : bois\nv : verre\np : pierre\nf : fer\nIl faut trouver l\'équilibré, mais tu as de drois qu\'à 3 cubes !\nEntrez 3 raccourcis maximum (exemple : \'b v p\') [q] :quitter, [?] : aide :'
        reponse = input(aff).lower()
        if reponse == 'q':
            return personnage, 'Tu as quitté l\'énigme'
        if reponse == '?':
            print(affichage(l_poids, masse) + '\n' * 15 + '\nAu dessus ce trouve une balance. A droite il y a des poids que vous ne pouvez pas enlever.\nIl faut équilibrez avec 3 cubes maximum de différents matériaux.\nCompris ?', end='')
            input()
        else:
            nbr_carac = 0
            l_poids_temporaire = []
            for carac in reponse:
                if carac in ('b', 'v', 'p', 'f'):
                    l_poids_temporaire.append(carac_n[carac])
                    nbr_carac += 1
                elif carac not in (' ', ','):
                    break
                if nbr_carac > 3:
                    break
            else:
                l_poids = l_poids_temporaire
        masse = 0
        for bloc in l_poids:
            masse += n_p[bloc]
        if resolue(masse):
            if 'Clef gamma' in personnage.inventaire:
                boite_dialogue('Tu as déjà la Clef gamma', '[entrer] pour continuer', personnage)
            else:
                boite_dialogue('Tu as obtenue la Clef gamma', '[entrer] pour continuer', personnage)
                personnage.inventaire.append('Clef gamma')
            boite_dialogue('Tu as rempli ton trousseau de clef ! Ca fait beaucoup n\'es-ce pas ? Tu le sais que tu es proche de savoir !', 'Super ! Mais qui es-tu ?', personnage)
            return personnage, 'Tu as trouvé la solution.'


def enigme_6(personnage):
    lettre_nbr = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9, "k": 10, "l": 11,
                  "m": 12, "n": 13, "o": 14, "p": 15, "q": 16, "r": 17, "s": 18, "t": 19, "u": 20, "v": 21, "w": 22,
                  "x": 23, "y": 24, "z": 25}
    nbr_lettre = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h", 8: "i", 9: "j", 10: "k", 11: "l",
                  12: "m", 13: "n", 14: "o", 15: "p", 16: "q", 17: "r", 18: "s", 19: "t", 20: "u", 21: "v", 22: "w",
                  23: "x", 24: "y", 25: "z"}
    cercle = {'w': 'd', 'd': 'z', 'z': 'y', 'y': 'h', 'h': 'r', 'r': 'q', 'q': 'o', 'o': 'k', 'k': 'p', 'p': 'u', 'u': 'a', 'a': 'f', 'f': 'l', 'l': 'i', 'i': 'b', 'b': 'n', 'n': 'c', 'c': 'm', 'm': 'j', 'j': 'e', 'e': 'v', 'v': 't', 't': 's', 's': 'x', 'x': 'g', 'g': 'w'}
    ab = {'c': 'c', 'z': 'n', 'i': 'a', 'q': 'v', 'x': 'd', 'f': 'r', 's': 'm', 'y': 'e', 'u': 'p', 'o': 'h', 'l': 'w', 't': 'j', 'b': 'k'}
    ba = {'g': 'c', 'n': 'z', 'a': 'i', 'v': 'q', 'd': 'x', 'r': 'f', 'm': 's', 'e': 'y', 'p': 'u', 'h': 'o', 'w': 'l', 'j': 't', 'k': 'b'}
    solution = personnage.nom.lower()

    if 'enigme_6' in personnage.deja_vu:
        boite_dialogue('Vous m\'avez dejà parlé', '[Entrer] pour contiuer', personnage)
        return personnage, 'C\'était le professeur.'
    else:
        def resolu(pseudo):
            transforme_1 = ''
            for carac in pseudo:
                if carac in lettre_nbr:
                    transforme_1 += nbr_lettre[(lettre_nbr[carac] - 12) % 26]
                else:
                    transforme_1 += carac
            transforme_2 = ''
            for carac in transforme_1:
                if carac in cercle:
                    transforme_2 += cercle[carac]
            transforme_1 = ''
            for carac in transforme_2:
                transforme_1 = carac + transforme_1
            transforme_2 = ''
            for carac in transforme_1:
                if carac in ab:
                    transforme_2 += ab[carac]
                elif carac in ba:
                    transforme_2 += ba[carac]
            return transforme_2
        solution = resolu(solution)
        while True:
            reponse = boite_dialogue('Professeur :\n Alors une réponse ?\n [?] : aide\n [q] : quitter', 'Réponse : ', personnage).lower()
            if reponse == '?':
                boite_dialogue('Professeur :\n Ah, donc lit les panneaux attentivement.', '[entrer] pour continuer', personnage)
            elif reponse == 'q':
                return personnage, 'Relit bein les panneaux.'
            elif reponse == solution:
                fini(personnage)
                return personnage, 'fini'


def enigme_666(personnage):
    incitation = ('Alors ?', 'Tu es pas à la hauteur.', 'Sinon tu peux tricher.', 'Tu sais le code est en python.',
                  'Il suffit d\'avoir python pour tricher.', 'Regarde le code si tu veux.', 'www.python.org',
                  'Oups, j\'ai fait exprès.', 'Bon tu te décides ?', 'regarde enigme_666 !')
    nombre = 0
    while True:
        reponse = input(f'{incitation[nombre]} [q] = quitter').lower()
        if reponse == 'q':
            return personnage, 'Bravo, tu triches pas !'
        if reponse == 'je suis un tricheur et c\'est pas bien de tricher.':
            personnage.vie = 8
            personnage.boisson = 8
            personnage.energie = 8
            personnage.nouriture = 8
            personnage.mana = 8
            return personnage, 'Tu as triché'
        if nombre != len(incitation) - 1:
            nombre += 1


def map_chargement(nom_carte: str) -> List[str]:
    """Fonction de chargement de carte à partir de fichier :
    Entrée : Le nom de la carte;
    Sortie : Une liste de caractère (la carte)."""
    with open(nom_carte + ".txt", 'r') as fichier:
        nouvelle_carte = [ligne_f.rstrip() for ligne_f in fichier]
    return nouvelle_carte


def affichage(x_personnage, y_personnage, z_personnage, carte, action, retour_a_la_ligne, hh, mm, personnage: Personnage, skin):
    """Fonction affichant tout (map et HUD):
    Entrées : [x, y, z]_personnage (coordonnées du personnage en 3D), carte (Liste de String), action (Ce qui va être affiché en bas : String),
              retour_a_la_ligne (demandant si il faut un retour à la ligne en bas : booléen), hh et mm (heure et minute : int),
              personnage (caractéristiques), skin (apparance du personnage à déplacer : string)"""
    def affichage_lat(personnage, y, hh, mm):
        """Fonction affichant les informations latérales :
        Entrées : personnages (caractéristiques), hh et mm (heure et minute : int)"""
        def get_prefix(valeur: int, v_bas, v_haut) -> str:
            """Fonction donnant le prefixe devant les caractéristiques à avoir (pas beaucoup : -, beaucoup : +)
            entrées : valeur (ce qu'il faut analyser (ex : vie) : int), v_bas et v_haut (les valeurs pour les quels il faut mettre les prefixes) ;
            Sortie : string (préfixe)."""
            if valeur <= v_bas:
                return '-'
            if valeur >= v_haut:
                return '+'
            return ' '

        line_to_statut: Dict[int, Tuple[int, int, int, str]] = {
            1: (round(personnage.vie), 2, 7, "vie"),
            2: (round(personnage.mana), 2, 7, "mana"),
            3: (round(personnage.energie), 2, 7, "energie"),
            4: (round(personnage.boisson), 2, 7, "boisson"),
            5: (round(personnage.nouriture), 2, 7, "nouritu"),
        }
        longueur = max(len(e[3]) for e in line_to_statut.values())
        if y == 0:  # La première ligne est pour l'heure et les minutes
            return f"heure {hh:02}:{mm:02}"  # Cela permet de le mettre sur 2 caractères et de mettre un 0 sinon
        if y in line_to_statut:
            v, v_basse, v_haute, nom_statut = line_to_statut[y]
            return f"{get_prefix(v, v_basse, v_haute)}{nom_statut.ljust(longueur)} {v}"
        return ''
    aff = ""
    l_actions = len(action) + 8
    # l_action (int): calcul permettant de savoir combien il y a de caractère dans "action" avec le reste, il sert plus tard.
    case_y = 0
    if len(carte) < 6:
        for _ in range(6 - len(carte)):
            carte.append('')
    for ligne in carte:
        case_x = 0
        l = len(carte[case_y])
        for case in ligne:
            if case_y == y_personnage and case_x == x_personnage:  # Si c'est les coordonnée du personnage alors on l'affiche
                aff += skin
            else:
                aff += case
            if case_x+1 <= l:
                # Partie complexe : Ayant qu'un caractère sur deux stoqué dans les ".txt", il nous faut créer de beaux espaces.
                if case_x+1 == l:  # Si l'on a rien après alors on met un espace.
                    case_tester = ' '
                else:
                    case_tester = carte[case_y][case_x+1]
                aff_case_suivante = {('-', '-'): '-', (',', '-'): '-', ('-', ','): '-', ('\'', '-'): '-', ('-', '\''): '-',
                                     ('-', '+'): '-', ('+', '-'): '-', (',', '+'): '-', ('+', ','): '-', ('P', ','): '-',
                                     ('-', 'P'): '-', ('P', '-'): '-', ('|', '-'): '-', ('-', '|'): '-', (',', 'P'): '-',
                                     ('\'', 'P'): '-', (',', '\''): '-', ('\'', ','): '-', ('P', '\''): '-', ('-', 'E'): '-', ('E', '-'): '-'}
                # aff_case_suivante (dico) : on donne deux cases consécutives et ça renvoit ce qu'il y a entre les deux.
                double = (case, case_tester)
                if double in aff_case_suivante:  # Il on met la case entre deux.
                    aff += aff_case_suivante[double]
                else:
                    aff += " "
            else:
                aff += " "
            case_x += 1
        for _ in range((personnage.option_largeur - 20)-case_x*2):
            aff += " "
        aff += affichage_lat(personnage, case_y, hh, mm) + "\n"
        case_y += 1
    for _ in range((personnage.option_hauteur - 2)-case_y - (l_actions // personnage.option_largeur)):  # l_action permet de savoir combien de ligne prend le tout
        aff += "\n"
    if retour_a_la_ligne:  # Si l'on doit faire un retour à la ligne ou pas.
        aff += f"\n{action}\n"
    else:
        aff += f"{action}\nEntre une commande. [?] : aide.\naction : "
    print(aff, end="")


def pnj(x, y, z, x_personnage, y_personnage, z_personnage, carte_nom, personnage, carte):
    """Fonction s'occupant des intéractions avec les Personnages Non Joueur :
    Entrées : x et y et z (coordonées possibles du personnage (si il y a un mur il n'ira pas, si il y en a pas)),
              [x, y, z]_personnage (coordonnées du personnages  avant déplacement (opposé de 'x', 'y' et 'z')),
              carte_nom (nom de la carte : string), personnages (caractéristiques), carte (la map (il n'y a jamais de changement)) ;
    Sorties : int et int et int ([x, y, z]_personnage : les coordonées du personnage), string (action), liste (carte), string (carte_nom)"""
    print(carte_nom)
    pnj_dialogues = {(3, 1, 5, "debut"): ("Dieu", ("Bien, tu es arrivé ici !\n Je vais te donner la Clef blanche, tout le monde l'a, elle ouvre les portes. \n Elles évitent que les vermines se propagent ! \n Je crois que je t'ai tout dit, maintenant va à la porte.", ("Merci", "D1", "Clef blanche"))),
                     (4, 2, 5, "5_5_5"): ("Nato", ("C'est agaçant ! Maintenant qu'on vit sous terre, on a plus de bière !\n On a seulement cette ignoble vodka. ", ("Ok", "R")), ("Tu veux une énigme ?", ("Oui !", "E2"), ("Non merci", "R"))),
                     (2, 3, 5, "5_5_5"): ("Barman", ("Que veux tu ?", ("De l'eau", "D3", "Gourde d'eau", 2), ("De la vodka", "D3", "Gourde de vodka", 5), ("Une patate", "D3", "Patate", 3), ("Rien merci", "S"))),
                     (10, 5, 5, "2_3_5"): ('Professeur', ('Oh comment vas-tu ?', ('Qui es-tu ?', 'R'), ('Bien et  toi ?', 'C2')), ('Je suis le professeur. Ah oui tu m\'as dit que tu t\'en suviendrait pas.\n Tu m\'as dit de te demander un mot de passe.', ('Ok...', 'E6')), ('Bien. Alors le mot de passe ?', ('Très bien', 'E6'))),
                     (1, 7, 5, '2_5_5'): ('Clochard', ('Tu veux quoi ?\n Dans tout les cas n\'en parle pas au barman il m\'aime pas.', ('De l\'eau (salle)', 'D3', 'Gourde d\'eau salle', 1), ('Du rat', 'D3', 'Rat', 2), ('Du serpent', 'D3', 'Serpent', 2), ('Rien', 'S'))),
                     (8, 4, 5, '5_6_5'): ('Sorcière', ('Que veux tu ?', ('potion étrange (donne du mana)', 'D3', 'Gourde de potion étrange', 3), ('Un steak de taupe', 'D3', 'Steak de taupe', 3), ('Du fromage', 'D3', 'Fromage', 2), ('Rien merci', 'S')))
                     }
    cpt = 0
    cpt_voulu = 0
    if (x, y, z, carte_nom) in pnj_dialogues:
        action = "C'était une gentille personne..."
        contenue = pnj_dialogues[(x, y, z, carte_nom)]
        nom_pnj = contenue[0]
        for dialogue in contenue[1: len(contenue)]:
            if cpt_voulu == 0 or (cpt == cpt_voulu and cpt_voulu != 0):
                aff = f"{nom_pnj} : \n"
                nbr_reponse = len(dialogue)
                y = 0
                aff += f" {dialogue[0]}\n"
                for reponses in dialogue[1: nbr_reponse]:
                    aff += f"  {ascii(y)}) {reponses[0]}\n"
                    y += 1
                aff = aff[0:-1]
                choix = ''
                while not (choix != '' and choix in string.digits and '0' <= choix <= str(nbr_reponse - 2)):
                    print(choix != '', choix in string.digits, choix in str(range(0, nbr_reponse - 2)), nbr_reponse - 2)
                    choix = boite_dialogue(aff, f"[0 à {nbr_reponse - 2}] Entre un numéro :", personnage)
                reponse = dialogue[int(choix) + 1][1]
                if reponse == 'S':
                    break
                if reponse == "D1":
                    if dialogue[int(choix) + 1][2] in personnage.inventaire:
                        boite_dialogue(f"Tu as déjà {dialogue[int(choix) + 1][2]}", '', personnage)
                    else:
                        boite_dialogue(f"Tu as obtenu {dialogue[int(choix) + 1][2]}", '', personnage)
                        personnage.inventaire.append(dialogue[int(choix) + 1][2])
                if reponse == "D2":
                    boite_dialogue(f"Tu as obtenu {dialogue[int(choix) + 1][2]}", '', personnage)
                    personnage.inventaire.append(dialogue[int(choix) + 1][2])
                if reponse == "D3":
                    if personnage.argent-dialogue[int(choix)+1][3] >= 0:
                        boite_dialogue(f"Tu as obtenu {dialogue[int(choix) + 1][2]}", '', personnage)
                        personnage.inventaire.append(dialogue[int(choix) + 1][2])
                        personnage.argent -= dialogue[int(choix) + 1][3]
                        boite_dialogue(f'Il te reste {personnage.argent} ¤.', '[entrer] pour continuer.', personnage)
                    else:
                        boite_dialogue(f'Tu n\'as plus assez d\'argent. Il te reste {personnage.argent} ¤.', '[Entrer] pour continuer.', personnage)
                if reponse == "E2":
                    personnage = enigme_2(personnage)
                if reponse == 'E6':
                    personnage, action = enigme_6(personnage)
                    break
                if reponse[0] == 'C':
                    cpt_voulu = int(reponse[1])
            cpt += 1
    else:
        action = "il est bien muet..."
    return x_personnage, y_personnage, z_personnage, action, False, carte, carte_nom


def interaction(x, y, z, x_personnage, y_personnage, z_personnage, carte, carte_nom, personnage: Personnage):
    """Fonction gérant les interactions avec les objets :
    Entrées : x et y et z (coordonées futur ou éventueles), [x, y, z]_personnage (coordonée actuel du joueur), carte, carte_nom, personnage (caractéristiques) ;
    Sorties : int int int (coordonnées), string (action), liste (carte), string (carte_nom).
    Spécificités : Fait appel à beaucoup de fonctions."""
    objet_interactif = {
        (6, 2, 5, "5_4_5"): ("panneau", "Vous qui passez cette porte, prennez garde à ne pas vous perdre."),
        (7, 8, 5, "5_5_5"): ("panneau", "Centre ville"),
        (6, 8, 5, "4_5_5"): ("panneau", "Maison de Nato"),
        (1, 8, 5, "4_5_5"): ("panneau", "Maison de César\n12"),
        (4, 6, 5, "3_5_5"): ("panneau", 'Mine abandonée\n(Sécurisé par le professeur)'),
        (6, 4, 5, "4_5_5"): ("coffre", "Clef rouge"),
        (1, 10, 5, "4_5_5"): ("coffre", ("Journal de César", "Gourde d'eau")),
        (10, 7, 6, "5_5_6"): ("coffre", "Journal du professeur"),
        (9, 13, 7, "labyrinthe 3"): ("coffre", ("Gourde d'eau", "Pelle")),
        (2, 11, 5, "2_5_5"): ('panneau', 'C\'est une partie de la mine très étrange.\nPasses le 4ème mur je te pris.'),
        (8, 1, 5, '2_4_5'): ('balance', (1, '3 bois', 1, '2 verres', '[entrer] pour continuer')),
        (8, 3, 5, '2_4_5'): ('balance', (1, '4 verres', 1, '1 pierre', '[entrer] pour continuer')),
        (8, 5, 5, '2_4_5'): ('balance', (1, '4 pierres', 1, '3 fers', '[entrer] pour continuer')),
        (0, 9, 5, '2_3_5'): ('panneau', f'Pensez à votre nom : "{personnage.nom.lower()}".'),
        (0, 7, 5, '2_3_5'): ('panneau', 'Pense à César et à son adresse.'),
        (0, 5, 5, '2_3_5'): ('panneau', '    R Q O K P\n   H         U\n  Y           A\n Z             F\nD /\\ tourne     L\nW   d\'un pas \\/ I\n G             B\n  X           N\n   S         C\n    T V E J M'),
        (0, 3, 5, '2_3_5'): ('panneau', 'Inverse le sens.'),
        (0, 1, 5, '2_3_5'): ('panneau', 'C-G, Z-N, I-A, Q-V, X-D, F-R, S-M, Y-E, U-P, O-H, L-W, T-J, B-K\nInverse les lettres.'),
        (4, 7, 5, '5_6_5'): ('panneau', 'Maison du barman'),
        (4, 2, 5, '5_6_5'): ('panneau', 'Maison de la sorcière')
        }

    def porte_escalier(x, y, z, x_personnage, y_personnage, z_personnage, carte, carte_nom, objet, personnage):
        """Fonction gérant le passage d'une porte ou d'un escalier :
        Entrées : x et y et z (coordonées futur ou éventueles), [x, y, z]_personnage (coordonée actuel du joueur), carte, carte_nom, personnage (caractéristiques) ;
        Sorties : int int int (coordonnées), string (action), liste (carte), string (carte_nom)."""
        def changement_map(x_passage, y_passage, z_passage, carte_nom):
            """Fonction :
            Entrées : [x, y, z]_passage (coordonnée de la porte ou de l'escalier), carte_nom ;
            Sortie : tuple (valeur : int, int, int, string)"""
            valeur = passage_direction[(x_passage, y_passage, z_passage, carte_nom)]
            return valeur

        if (x, y, z, carte_nom) in passage_direction:
            fichier_nom = {"5_5_5": "le centre ville", "5_4_5": "l'entrée du labyrinthe",
                           "5_5_6": "La maison du professeur", "4_5_5": "quartier résidentiel",
                           "6_5_5": "Laboratoire du professeur"}
            x, y, z, carte_nom_prochaine, serrure = changement_map(x, y, z, carte_nom)
            if serrure in personnage.inventaire:
                carte = map_chargement(carte_nom_prochaine)
                if carte_nom == carte_nom_prochaine:
                    action = "Tu as passé une porte."
                elif carte_nom_prochaine in fichier_nom:
                    action = f"Tu es arrivé dans {fichier_nom[carte_nom_prochaine]}."
                else:
                    action = f"Tu es arrivé dans {carte_nom_prochaine}"
                return x, y, z, action, False, carte, carte_nom_prochaine
            else:
                action = f"La porte est bloquée ! Tu as besoin de la {serrure}."
                return x_personnage, y_personnage, z_personnage, action, True, carte, carte_nom
        elif carte_nom in ("labyrinthe 1", "labyrinthe 2", "labyrinthe 3"):
            carte_nbr = int(carte_nom[11])
            if objet == '^' and (carte_nbr == 1 or carte_nbr == 2):
                carte = map_chargement(f"labyrinthe {carte_nbr + 1}")
                action = "Tu es monté d'un étage."
                return x, y, z + 1, action, False, carte, f"labyrinthe {carte_nbr + 1}"
            elif objet == 'v' and (carte_nbr == 2 or carte_nbr == 3):
                carte = map_chargement(f"labyrinthe {carte_nbr - 1}")
                action = "Tu es déscendu d'un étage."
                return x, y, z - 1, action, False, carte, f"labyrinthe {carte_nbr - 1}"
        else:
            if objet == 'P':
                action = "La porte est fermée !"
            elif objet in '^v':
                action = "L'escalier est cassé !"
            else:
                raise ValueError(objet)
            return x_personnage, y_personnage, z_personnage, action, False, carte, carte_nom
    objet = carte[y][x]
    if objet in 'P^v':  # Si c'est un escalier ou une porte
        return porte_escalier(x, y, z, x_personnage, y_personnage, z_personnage, carte, carte_nom, objet, personnage)
    elif objet == '?':  # Si c'est un objet
        if (x, y, z, carte_nom) in objet_interactif:
            categorie, contenue = objet_interactif[(x, y, z, carte_nom)]
            if categorie == "panneau":
                boite_dialogue(contenue, '', personnage)
                action = "C'était un joli panneau !"
            elif categorie == "coffre":
                if [x, y, z, carte_nom] in personnage.deja_vu:
                    boite_dialogue("Coffre :\nCe coffre est vide", "[Entrer] pour continuer", personnage)
                else:
                    if isinstance(contenue, str):
                        boite_dialogue(f"Coffre :\nTu as obtenu {contenue}", "[Entrer] pour continuer", personnage)
                        personnage.inventaire.append(contenue)
                    else:
                        for objet_coffre in contenue:
                            boite_dialogue(f"Coffre :\nTu as obtenu {objet_coffre}", "[Entrer] pour continuer", personnage)
                            personnage.inventaire.append(objet_coffre)
                    personnage.deja_vu.append([x, y, z, carte_nom])
                action = "C'était un beau coffre !"
            elif categorie == 'balance':
                balance(contenue[0], contenue[1], contenue[2], contenue[3], contenue[4], personnage)
                action = 'C\'était une balance'
            else:
                raise ValueError()
        else:
            action = "C'est juste, rien, rien de spécial."
        return x_personnage, y_personnage, z_personnage, action, True, carte, carte_nom
    elif objet == 'E':  # Si c'est une énigme
        coord_enigme = {(5, 7, 6, "5_5_6"): 1, (0, 6, 5, "3_5_5"): 4, (0, 3, 5, '2_4_5'): 5, (2, 4, 5, '2_6_5'): 666}
        if (x, y, z, carte_nom) in coord_enigme:
            numero_enigme = coord_enigme[(x, y, z, carte_nom)]
            if numero_enigme == 1:
                action = "Tu ne l'as pas fini, la machine s'est réintialisé..."
                if enigme_1(personnage):
                    action = "Tu as obtenu la clef bleu !"
            elif numero_enigme == 4:
                personnage, action = enigme_4(personnage)
            elif numero_enigme == 5:
                personnage, action = enigme_5(personnage)
            elif numero_enigme == 666:
                personnage, action = enigme_666(personnage)
            else:
                action = 'Il y a une erreur dans le programme. :/'
            return x_personnage, y_personnage, z_personnage, action, True, carte, carte_nom
        else:
            action = "C'est misterieux..."
            return x_personnage, y_personnage, z_personnage, action, True, carte, carte_nom
    elif objet == '$':  # Si c'est un pnj
        return pnj(x, y, z, x_personnage, y_personnage, z_personnage, carte_nom, personnage, carte)


def chargement(automatique):
    """Fonction chargeant une partie :
    Spécificité : Pas d'entrée ou de sortie, elle est à l'origine d'une partie justement."""
    personnage = Personnage()
    try:
        if automatique:
            with open("sauvegarde_auto.txt", 'r') as fichier:
                for ligne in fichier:
                    sauvegarde = ligne
        else:
            with open("sauvegarde.txt", 'r') as fichier:
                for ligne in fichier:
                    sauvegarde = ligne
        x_personnage, y_personnage, z_personnage, pv, pm, pe, pb, pn, inventaire, heure, minute, carte_nom, nom, argent, deja_vu, hauteur, largeur = sauvegarde.split(',')
        carte = map_chargement(carte_nom)
        personnage.vie = int(pv)
        personnage.mana = int(pm)
        personnage.energie = float(pe)
        personnage.boisson = float(pb)
        personnage.nouriture = float(pn)
        personnage.nom = nom
        personnage.argent = int(argent)
        personnage.option_hauteur = int(hauteur)
        personnage.option_largeur = int(largeur)
    except ValueError:
        boite_dialogue('Tu as essayé de tricher ! Bravo pour le ValueError.', 'Ok, désolé', personnage)
    except FileNotFoundError:
        boite_dialogue('La sauvegarde ne semble pas exister, essaye une nouvelle partie.', 'Ok', personnage)
        main(False, personnage)
    else:
        for objet in inventaire.split('.'):
            if objet != '':
                personnage.inventaire.append(objet)
        for choses in deja_vu.split('.'):
            liste = []
            nbr = 0
            if len(choses) != 0:
                for chose in choses.split(':'):
                    if nbr < 3 and chose != '':
                        liste.append(int(chose))
                    elif chose != '':
                        liste.append(chose)
                    nbr += 1
                personnage.deja_vu.append(liste)
        if len(personnage.deja_vu) == 1 and personnage.deja_vu[0] == '':
            personnage.deja_vu.remove(0)
        principale(int(x_personnage), int(y_personnage), int(z_personnage), carte, carte_nom, int(heure), int(minute), personnage, "Partie chargé.")


def principale(x_personnage, y_personnage, z_personnage, carte, carte_nom, heure, minute, personnage: Personnage, action):
    """Fonction principale gérant tout et fonctionnant à tous les tours :
    Entrées : [x, y, z]_personnage (coordonnée du personnage), carte, carte_nom (nom de la carte), heure et minute (temps), personnage (caractéristiques), action."""
    def deplacement(mouvement, x_personnage, y_personnage, z_personnage, carte, carte_nom, personnage):
        """Fonction s'occupant des déplacements et des interactions :
        Entrées : mouvement, [x, y, z]_personnage (coordonnées du personnage), carte, carte_nom (nom de la carte)n personnage (caractéristiques) ;
        Sorties : int, int, int (coordonnées), string (action), liste (carte), string (carte_nom)."""
        if mouvement.strip() == '':
            return interaction(x_personnage, y_personnage, z_personnage, x_personnage, y_personnage, z_personnage,
                               carte, carte_nom, personnage)
        elif mouvement in mouvement_deplacement:
            deplacement_coordonnee = {"haut": (0, -1), "gauche": (-1, 0), "bas": (0, 1), "droite": (1, 0)}
            deplacement_action = {"haut": "Tu es allé au Nord.", "gauche": "Tu es allé à l'Ouest.",
                                  "bas": "Tu es allé au Sud.", "droite": "Tu es allé à l'Est."}
            coord_verification = deplacement_coordonnee[touche_deplacement[mouvement]]
        else:
            raise ValueError()
        x, y = coord_verification
        x += x_personnage
        y += y_personnage
        z = z_personnage
        if y > len(carte) - 1 or x > len(carte[y]) - 1 or carte[y][x] in objet_avec_colision or x < 0 or y < 0:
            action = "Tu essayes de te manger le mur !"
            return x_personnage, y_personnage, z_personnage, action, False, carte, carte_nom
        elif carte[y][x] in objet_avec_interaction:
            return interaction(x, y, z, x_personnage, y_personnage, z_personnage, carte, carte_nom, personnage)
        else:
            action = deplacement_action[touche_deplacement[mouvement]]
            return x, y, z_personnage, action, False, carte, carte_nom

    def f_inventaire(personnage, x_personnage, y_personnage, z_personnage, carte_nom):
        """Fonction gérant l'affichage et l'utilisation des objets dans l'inventaire :
        Entrée : personnage (caractéristiques, surtout l'inventaire ici) ;
        Sorties : class (personnage), string (action)."""
        action = "Tu n'as rien fait dans ton inventaire..."
        objet_mangeable = {"Gourde d'eau": (0, 0, 0, 2, 0), "Gourde de vodka": (0, 1, 0, 1, 0), "Patate": (0, 0, 0.5, 0, 1.5), "Fromage": (0, -0.5, 0, -0.5, 2), "Steak de taupe": (0, -0.5, 0.5, 0, 1.5), "Serpent": (-0.5, 0.5, 0, 0, 1), 'Rat': (-0.5, -1, 0, 0, 1), 'Gourde d\'eau salle': (0, -0.5, 0, 1, 0), 'Gourde de potion étrange': (0, 3, 0, 0.5, 0)}
        action_inventaire = {"Gourde d'eau": "Tu as bu.", "Gourde de vodka.": "Tu as bu.", 'Patate': 'Tu as mangé.', 'Fromage': 'Tu as mangé.', 'Steak de taupe': 'Tu as mangé.', 'Serpent': 'Tu as mangé.', 'Gourde de potion étrange': 'Tu as bu.'}
        papiers = {"Journal de César": "Ce soir-là comme un chaque soir mon ami Nato et moi nous nous retrouvons au bar du centre-ville, rapidement nous nous retrouvons au milieu de notre partie de carte habituelle, nous buvons comme à l’accoutumée un bon verre de vodka.  Mais, en le voyant triché, je décide de jouer le même jeu que lui. Mais Nato n’est pas d’accord avec ma façon de jouer et le ton monte rapidement entre nous. Mais, ce sac de taupe pense vraiment que je vais rien faire face à ses conneries !!! Mais pour qui il se prend ce tricheur !!!",
                   "Journal du professeur": "journal : \nAujourd'hui, c'est décidé : je tente de fabriquer un matériau solide mais qui est assez souple et élastique. Ca va être compliqué. L'autre jour des villageois ayant entendu parler de mon projet n'ont rien trouvé de mieux que de s'en moquer. Ils vont voir ces maudits cloportes, tous aussi gluants et rampants que des verres de terre.\\$journal : \nBon c'est bien beau d'avoir cette idée, maintenant il fraudrait que je trouve à partir de quoi faire ce fameux matériau... Du ciment et de l'eau, de la terre chauffée à très haute température ou de l'argile. Bon on verra, ça plus tard maintenant il faut que j'avance aussi sur mes autres projets, car il serait dommage de ne faire qu'un seul projet à la fois. Mon cerveau de génie mérite de pouvoir s'amuser.\\$journal : \nQuelle belle journée qui s'annonce ! Grâce à mon intelligence j'ai pu imaginer un système pouvant fournir de l'énergie à partir du courant d'une rivière sous-terraine. La partie théorique est terminée, il ne reste que la partie pratique ce qui risque d'être long sachant que personne ne peut aider \"un vieux fou arrogant\" comme le diraient certains.\\$journal : \nJe détestes ces fichues expériences ! Rien ne va jamais comme je le veux. Encore aujourd'hui, mon hypothèse de fabriquer ce fameux matérieux souple a échoué ! Ca fait déjà trois mois que j'essaye de chauffer à très haute température différents matériaux comme l'argile... D'ailleurs le test avec l'hydrocarbure a pas eu besoin d'être jeté, il a brulé tout seul ! Je n'en pouvais plus de tous ces echecs. Peut-être que je suis vraiment qu'un simple homme qui n'a rien d'exceptionnel et qui ressemble aux autres...\\$journal : \nJ'AI REUSSI ! Pourquoi chauffer à haute température ? L'or ! L'or c'est souple, c'est inoxydable, c'est joli... C'est parfait mais faudrait-il encore en trouver... D'ailleurs je déménage, je laisse celui du centre ville vide au cas où.\\$journal : \nJe note ça pour mon moi du future : si tu cherches à revenir dans ton nouveau labo tu devras te CREUSER la tête  en cherchant l'or dans ton encien labo."}
        reponse = ''
        while reponse == '':
            aff = f"Inventaire :\nArgent : {personnage.argent} ¤\n"
            y = 0
            for ligne in personnage.inventaire:
                aff += ascii(y) + '-' + ligne + '\n'
                y += 1
            aff += '\n' * (26 - y)
            print(aff + "\nQuel objet veux-tu essayer ? Entre le nombre : ", end='')
            reponse = input().upper()
        for carac in reponse:
            if carac not in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                boite_dialogue('Il faut donner un nombre, pas une lettre', '[Entrer] pour continuer', personnage)
                break
        else:
            if int(reponse)+1 > len(personnage.inventaire):
                boite_dialogue('Le nombre est trop grand', '[Entrer] pour continuer', personnage)
            elif personnage.inventaire[int(reponse)] in objet_mangeable:
                personnage.vie += objet_mangeable[personnage.inventaire[int(reponse[0])]][0]
                personnage.mana += objet_mangeable[personnage.inventaire[int(reponse[0])]][1]
                personnage.energie += objet_mangeable[personnage.inventaire[int(reponse[0])]][2]
                personnage.boisson += objet_mangeable[personnage.inventaire[int(reponse[0])]][3]
                personnage.nouriture += objet_mangeable[personnage.inventaire[int(reponse[0])]][4]
                if personnage.vie > 8:
                    personnage.vie = 8
                if personnage.mana > 8:
                    personnage.mana = 8
                if personnage.energie > 8:
                    personnage.energie = 8
                if personnage.boisson > 8:
                    personnage.boisson = 8
                if personnage.nouriture > 8:
                    personnage.nouriture = 8
                print(personnage.inventaire[int(reponse[0])])
                action = action_inventaire[personnage.inventaire[int(reponse[0])]]
                personnage.inventaire.remove(personnage.inventaire[int(reponse[0])])
            elif personnage.inventaire[int(reponse)] in papiers:
                boite_dialogue(papiers[personnage.inventaire[int(reponse[0])]], "[Entrer] pour continuer", personnage)
            elif personnage.inventaire[int(reponse)] == 'Pelle':
                personnage = enigme_3(x_personnage, y_personnage, z_personnage, carte_nom, personnage)
        return personnage, action
    
    def sauvegarde(x_personnage, y_personnage, z_personnage, personnage, heure, minute, carte_nom, automatique):
        if automatique:
            with open("sauvegarde_auto.txt", 'w') as fichier:
                inventaire = ''
                for objet in personnage.inventaire:
                    inventaire += objet + '.'
                inventaire = inventaire[0:-1]
                deja_vu = ''
                for choses in personnage.deja_vu:
                    for chose in choses:
                        deja_vu += f"{chose}:"
                    deja_vu = deja_vu[0: -1] + '.'
                deja_vu = deja_vu[0:-1]
                fichier.write(
                    f"{x_personnage},{y_personnage},{z_personnage},{personnage.vie},{personnage.mana},{personnage.energie},{personnage.boisson},{personnage.nouriture},{inventaire},{heure},{minute},{carte_nom},{personnage.nom},{personnage.argent},{deja_vu},{personnage.option_hauteur},{personnage.option_largeur}")
        else:
            with open("sauvegarde.txt", 'w') as fichier:
                inventaire = ''
                for objet in personnage.inventaire:
                    inventaire += objet + '.'
                inventaire = inventaire[0:-1]
                deja_vu = ''
                for choses in personnage.deja_vu:
                    for chose in choses:
                        deja_vu += f"{chose}:"
                    deja_vu = deja_vu[0: -1] + '.'
                deja_vu = deja_vu[0:-1]
                fichier.write(
                    f"{x_personnage},{y_personnage},{z_personnage},{personnage.vie},{personnage.mana},{personnage.energie},{personnage.boisson},{personnage.nouriture},{inventaire},{heure},{minute},{carte_nom},{personnage.nom},{personnage.argent},{deja_vu},{personnage.option_hauteur},{personnage.option_largeur}")
        
    def menu(x_personnage, y_personnage, z_personnage, personnage, heure, minute, carte_nom):
        """Fonction s'occupant du menu dans le jeu :
        Entrée : personnage (caractéristiques) ;
        Sorties class (personnage), string (sert plus tard)."""
        def option(personnage):
            """Fonction gérant les options :
            Entrée : personnage (caractéristiques) ;
            Sortie : class (personnage)."""
            while True:
                reponse = boite_dialogue("[p] changer de pseudo\n[a] : paramètre d'affichages\n[q] : quitter", 'choix : ', personnage)
                if reponse == 'p':
                    personnage.nom = input('Paramètre du pseudo' + "\n" * personnage.option_hauteur + "Choisis ton nouveau pseudo : ")
                    print(f"Ton pseudo est : {personnage.nom}")
                elif reponse == 'a':
                    while reponse not in ('0', '1', '2'):
                        reponse = boite_dialogue('[0] 119*29 : petite fenêtre\n[1] 210*49 : grande fenêtre\n[2] xxx*yy : personnalisé', 'choix : ', personnage)
                    if reponse == '2':
                        while reponse not in ('q', 'o'):
                            reponse = boite_dialogue('Tu vas être rediriger vers les parametres d\'affichage personnaliser.\nIl peut que ça prenne un peu de temps.\n[q] : quitter\n[o] : oui', 'choix : ', personnage)
                        if reponse == 'q':
                            break
                        else:
                            personnage = para_aff(personnage)
                            break
                    else:
                        formats = [(119, 29), (210, 49)]
                        personnage.option_largeur, personnage.option_hauteur = formats[int(reponse)]
                elif reponse == 'q':
                    return personnage

        while True:
            aff = ''
            with open("menu in game.txt", "r") as fichier:
                menu = [ligne_f for ligne_f in fichier]
            for ligne in menu:
                if ligne == '/\\non/\\\n':
                    aff += '\n' * (personnage.option_hauteur - 13)
                else:
                    aff += ligne
            print(aff + "\nchoix : ", end='')
            action_menu = input().lower()
            if action_menu == 'o':
                personnage = option(personnage)
            elif action_menu == 'r':
                return personnage, ''
            elif action_menu == 'c':
                return personnage, 'c'
            elif action_menu == 'a':
                return personnage, 'a'
            elif action_menu == 'q':
                return personnage, 'q'
            elif action_menu == 'e':
                sauvegarde(x_personnage, y_personnage, z_personnage, personnage, heure, minute, carte_nom, False)
                return personnage, 'e'

    actions_totales = action
    menu_reponse = ''
    fini = False
    while not (fini or menu_reponse in ('c', 'q', 'a')):
        affichage(x_personnage, y_personnage, z_personnage, carte, actions_totales, False, heure, minute, personnage, '@')
        mouvements_reponse = input().lower()
        actions_totales = ''
        if len(mouvements_reponse) == 2 and mouvements_reponse[0] in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
            mouvements_reponse = f"{mouvements_reponse[1]*int(mouvements_reponse[0])}"
        if mouvements_reponse == '':
            mouvements_reponse = ' '
        for mouvement in mouvements_reponse:
            if mouvement in mouvement_deplacement or (carte[y_personnage][x_personnage] in ('^', 'v', 'P') and mouvement.strip() == ''):
                sortie = deplacement(mouvement, x_personnage, y_personnage, z_personnage, carte, carte_nom, personnage)
                x_personnage = sortie[0]
                y_personnage = sortie[1]
                z_personnage = sortie[2]
                action = sortie[3]
                # Ici on vérifie qu'on rentre qu'une seule fois dans un objet avec inteaction comme un pnj²
                if sortie[4]:
                    actions_totales += f"{action} "
                    break
                if len(sortie) == 7:
                    carte = sortie[5]
                    carte_nom = sortie[6]
            elif mouvement == 'e':
                sauvegarde(x_personnage, y_personnage, z_personnage, personnage, heure, minute, carte_nom, False)
                action = "Tu as enregistré."
            elif mouvement == '?':
                with open("aide.txt", 'r') as fichier:
                    aff = ""
                    y = 0
                    for ligne in fichier:
                        aff += ligne
                        y += 1
                aff += "\n" * (29-y)
                print(aff+"\nfini ?", end='')
                input()
            elif mouvement == 'i':
                personnage, action = f_inventaire(personnage, x_personnage, y_personnage, z_personnage, carte_nom)
            elif mouvement == '(':
                reponse = input('x')
                nombres = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20')
                if reponse in nombres:
                    x_personnage = int(reponse)
                reponse = input('y')
                if reponse in nombres:
                    y_personnage = int(reponse)
                reponse = input('z')
                if reponse in nombres:
                    z_personnage = int(reponse)
                carte_nom = input('c_n')
                carte = map_chargement(carte_nom)
            elif mouvement == ')':
                action = f"{x_personnage},{y_personnage},{z_personnage},{personnage.vie},{personnage.mana},{personnage.energie},{personnage.boisson},{personnage.nouriture},{personnage.inventaire},{heure},{minute},{carte_nom},{personnage.nom}, {personnage.argent},{personnage.deja_vu},{personnage.option_hauteur},{personnage.option_largeur}"
            elif mouvement == 'm':
                personnage, menu_reponse = menu(x_personnage, y_personnage, z_personnage, personnage, heure, minute, carte_nom)
                if menu_reponse == 'e':
                    action = 'Tu as enregistré.'
                elif menu_reponse == 'r':
                    action = 'Tu as repris la partie.'
            elif mouvement.strip() == '':
                action = "Tu as attendu."
            else:
                action = "Oui, oui... Mais ça ne veut rien dire."
            if minute//10 == 0:
                sauvegarde(x_personnage, y_personnage, z_personnage, personnage, heure, minute, carte_nom, True)
            if mouvement in mouvement_deplacement or mouvement.strip() == '':
                minute += 1
            if minute == 60:
                minute = 0
                heure += 1
            if heure == 24:
                heure = 0
                personnage.energie = personnage.energie - 8 / (1440*2)
            personnage.boisson = personnage.boisson - 8 / 1440
            personnage.nouriture = personnage.nouriture - 8 / (1440*3)
            if personnage.energie > 6 and personnage.boisson > 6 and personnage.nouriture > 6:
                personnage.vie += 0.05
            if personnage.vie > 8:
                personnage.vie = 8
            if personnage.energie < 0:
                personnage.energie = 0
            if personnage.boisson < 0:
                personnage.boisson = 0
            if personnage.nouriture < 0:
                personnage.nouriture = 0
            if personnage.energie == 0 or personnage.boisson == 0 or personnage.nouriture == 0 and personnage.mana > 4:
                personnage.vie -= 0.1
            actions_totales += f"{action} "
        if action == 'fini':
            boite_dialogue('Vous avez fini le jeu, votre mémoire a été effacé.', '[Entrer] pour finir', personnage)
            generique(personnage)
            break
    if menu_reponse == 'c':
        chargement(False)
    elif menu_reponse == 'a':
        chargement(True)
    else:
        if menu_reponse == 'q':
            sauvegarde(x_personnage, y_personnage, z_personnage, personnage, heure, minute, carte_nom, True)
            boite_dialogue('Une sauvegarde automatique a été faite', '[Entrer] pour continuer', personnage)
        main(False, personnage)


def display_menu(phrase, personnage):
    """Fonction s'occupant du menu au début."""
    aff = ''
    with open("menu.txt", "r") as fichier:
        menu = [ligne_f for ligne_f in fichier]
    for ligne in menu:
        if ligne == '/\\oui/\\\n':
            aff += phrase + '\n'
        elif ligne == '/\\non/\\\n':
            aff += '\n' * (personnage.option_hauteur - 14)
        else:
            aff += ligne
    print(aff + "\nchoix : ", end='')


def tuto(personnage):
    """Fonction de tuto :
    Entrée : personnage (caractéristique)."""
    def animation_tuto(carte_animee, mouvement, hh, mm, personnage):
        """Fonction d'animation du tuto :
        Entrées : carte_animee (carte), mouvement (liste des mouvements), hh et mm (temps), personnage (caractéristiques)."""
        x, y = mouvement[0]
        action = "Je n'ai pas encore bougé."
        l = len(mouvement)
        affichage(x, y, 5, carte_animee, action, True, hh, mm, personnage, '$')
        input("[Entrer] pour commencer")
        action = ''
        for coordonnee in mouvement[1:l]:
            x_arrive, y_arrive = coordonnee
            while x_arrive != x or y_arrive != y:
                if x_arrive > x:
                    x += 1
                    action = f"Je suis allé à l'Est avec : {mouvement_deplacement[3]}"
                elif x_arrive < x:
                    x -= 1
                    action = f"Je suis allé à l'Ouest avec : {mouvement_deplacement[1]}"
                elif y_arrive > y:
                    y += 1
                    action = f"Je suis allé au Sud avec : {mouvement_deplacement[2]}"
                elif y_arrive < y:
                    y -= 1
                    action = f"Je suis allé au Nord avec : {mouvement_deplacement[0]}"
                affichage(x, y, 5, carte_animee, action, True, hh, mm, personnage, '$')
                input("[Entrer] pour continuer")
        return

    phrases = ("Oh tu viens de te réveiller !\nC'est étrange, personne ne se souvient de toi...",
               "Reprenons depuis le début :\nTu as de la vie, tu as besoin de boire, manger, dormir...\nFait attention à ça.",
               "Bon toi tu ressemble à ça : @.\nEt nous autre humains on a cette tête : $.",
               "Les portes 'P' et les escaliers '^', 'v' permettent de passer d'un endroit à un autre.\nLes '?' sont des objets, regarde les tous.")
    for phrase in phrases:
        boite_dialogue(phrase, "[entrer] pour continuer", personnage)
    correct = False
    while not correct:
        personnage.nom = boite_dialogue("Dit moi comment tu t'appelles.", "Choisis un nom : ", personnage).strip()
        if personnage.nom.lower() in ('', 'bite', 'petite merde', 'connard', 'petit con', 'hitler', 'staline', 'mao'):
            boite_dialogue("Ce n'est pas vraiment un nom ça.", "Ok...", personnage)
        else:
            correct = True
    boite_dialogue(f"Ravis de te rencontrer {personnage.nom}.\nSi tu as besoin d'aide fait [?], ça te donnera toutes les informations.", "[entrer] pour continuer", personnage)
    reponse = ''
    while reponse != '?':
        reponse = boite_dialogue('Essaye de faire [?], pour voir.', 'Choix :', personnage)
    with open("aide.txt", 'r') as fichier:
        aff = ""
        y = 0
        for ligne in fichier:
            aff += ligne
            y += 1
    aff += "\n" * (29 - y)
    print(aff + "\nfini ?", end='')
    input()
    boite_dialogue(f"Je vais me déplacer, regarde moi faire.", "[entrer] pour continuer", personnage)
    carte_animee = map_chargement("debut")
    carte_animee[1] = '|...|'
    carte_animee[2] = '|@..++P'
    animation_tuto(carte_animee, [(1, 2), (3, 2), (3, 1)], 00, 00, personnage)
    boite_dialogue(f"Pour te déplacer utilise {mouvement_deplacement}.\nSache que tu peux te déplacer sur plusieurs cases avec une seul commande :\n-Soit en rentrant plusieurs fois des déplacements, exemple : \"ddzzdd\" ;\n-Soit en mettant un nombre (1 à 9) suivit de l'instruction, exemple : \"4q\".", "[entrer] pour continuer", personnage)


def para_aff(personnage):
    def saut():
        print('\n'*100)
    x = 50
    y = 5

    def hauteur(personnage):
        while True:
            saut()
            aff = 'Haut'
            aff += '\n[+] pour augmenter la hauteur, [-] pour diminuer la hauteur (si tu ne vois pas Haut), [o] pour valider.'
            aff += '\nTu peux mettre plusieurs [+] ou [-] à la suite.'
            aff += '\n' * (personnage.option_hauteur - 2)
            aff += 'Bas'
            reponse = input(aff).lower()
            print(reponse)
            for carac in reponse:
                if carac == '+':
                    personnage.option_hauteur += 1
                elif carac == '-':
                    personnage.option_hauteur -= 1
                elif carac == 'o':
                    if 'oui' == boite_dialogue('Es-tu sur ?', '[oui] ou [non] : ', personnage):
                        return personnage
                else:
                    boite_dialogue('Je n\'ai pas compris. Entre [+], [-] ou [o].', '[Entrer] pour continuer', personnage)
                    break

    def largeur(personnage):
        while True:
            saut()
            aff = 'Gauche'
            aff += ' ' * (personnage.option_largeur - 12) + 'Droite'
            aff += '\n[+] pour augmenter la largeur, [-] pour diminuer la largeur (si Droite fait un retour à la ligne), [o] pour valider.'
            aff += '\nTu peux mettre plusieurs [+] ou [-] à la suite.'
            aff += '\n' * (personnage.option_hauteur - 2)
            reponse = input(aff).lower()
            print(reponse)
            for carac in reponse:
                if carac == '+':
                    personnage.option_largeur += 1
                elif carac == '-':
                    personnage.option_largeur -= 1
                elif carac == 'o':
                    if 'oui' == boite_dialogue('Es-tu sur ?', '[oui] ou [non] : ', personnage):
                        return personnage
                else:
                    boite_dialogue('Je n\'ai pas compris. Entre [+], [-] ou [o].', '[Entrer] pour continuer', personnage)
                    break
    reponse = ''
    x_pro = personnage.option_largeur
    y_pro = personnage.option_hauteur
    personnage.option_largeur = x
    personnage.option_hauteur = y
    while reponse not in ('oui', 'non'):
        reponse = boite_dialogue('Veux-tu regler la taille de la fenêtre ? Si tu as déjà une partie, la charger modifira la taille.', '[oui] ou [non] : ', personnage)
    if reponse == 'non':
        personnage.option_hauteur = y_pro
        personnage.option_largeur = x_pro

        return personnage
    while True:
        saut()
        aff = f'Bonjour, commençons par regler ta fenetre. Il y a {y} ligne(s) et {x} colonnes. Regle ta fenetre à la taille souhaitée (tu peux zoomer avec "CTRL + molette").'
        boite_dialogue(aff, '[Entrer] pour continuer', personnage)
        saut()
        aff = 'Maintenant met les coins dans les coins de la fenetre. Je vais te poser des questions, réponds-y.'
        boite_dialogue(aff, '[Entrer] pour continuer', personnage)
        personnage = hauteur(personnage)
        personnage = largeur(personnage)
        reponse = ''
        while reponse not in ('oui', 'non'):
            reponse = boite_dialogue('Es-tu satisfait ?', '[oui] ou [non] : ', personnage)
        if reponse == 'oui':
            return personnage


def main(debut, personnage):
    """Fonction lancé au début."""
    action = ' '
    phrases = ('Un chat sauvage est là !', 'J\'ai aqua-poney... :/', 'Ca va pas suffire !', 'C\'est Billy qui a eu l\'idée de ses phrases', 'En science c\'est pas "pourquoi ?" mais "pourquoi pas ?" !', 'C\'est vraiment un bon jeu !', '<3', 'Je code avec le...', 'Medic !', 'Oh ! Du diams !', 'Quel bébé !', 'Il est pas gentil de Lord régent. :c', 'The cake is a lie!', 'Troisième loi de Newton : On ne mange pas avec les doigts.', 'Beta-testeurs : Billy, Billy, Xord, Tita...')
    phrase = phrases[randint(0, len(phrases)-1)]
    if debut:
        personnage = para_aff(personnage)
    while action not in ('n', 'c', 'q', 'a'):
        display_menu(phrase, personnage)
        action = input().lower()
    if action == 'n':
        carte = map_chargement("debut")
        tuto(personnage)
        personnage.argent = 100
        principale(1, 2, 5,  carte, "debut", 8, 0, personnage, "Tu as commencé une nouvelle partie.")
    if action == 'c':
        chargement(False)
    if action == 'a':
        chargement(True)
    if action == 'q':
        boite_dialogue('Le jeu se ferme', 'Ok', personnage)


if __name__ == "__main__":
    personnage = Personnage()
    main(True, personnage)
