"""
Partie 5 – Interface en ligne de commande.

Usage :
    python3 main.py "expression" [mot1 mot2 ...] [--dot fichier.dot]

Exemples :
    python3 main.py "(a|b)*abb" abb aabb ab
    python3 main.py "(a|b)*abb" abb --dot automates/exemple.dot
    python3 main.py "a*" ""                 (le mot vide est passé avec "")

Affiche une ligne par mot :  abb : OUI
(sans mot à tester, affiche « Expression valide »)
Code de retour : 0 si l'expression est valide,
                 1 si l'expression est invalide,
                 2 si la commande est mal utilisée.
"""

import sys

from analyseur_syntaxique import AnalyseurSyntaxique
from export_graphviz import exporter_dot
from simulation import accepte


def lire_arguments(arguments):
    """
    Sépare l'option --dot du reste.
    Renvoie (expression, liste des mots, nom du fichier .dot ou None).
    """
    fichier_dot = None
    reste = []
    i = 0

    while i < len(arguments):

        if arguments[i] == "--dot":
            if i + 1 >= len(arguments):
                raise ValueError("l'option --dot doit être suivie d'un nom de fichier")
            fichier_dot = arguments[i + 1]
            i = i + 2

        else:
            reste.append(arguments[i])
            i = i + 1

    if not reste:
        raise ValueError("il manque l'expression régulière")

    return reste[0], reste[1:], fichier_dot


def afficher_mot(mot):
    """Le mot vide est affiché "" pour rester lisible."""
    if mot == "":
        return '""'
    return mot


def main(arguments):

    # 1. lecture de la ligne de commande
    try:
        expression, mots, fichier_dot = lire_arguments(arguments)
    except ValueError as e:
        print("Usage incorrect :", e)
        print('Usage : python3 main.py "expression" [mots ...] [--dot fichier.dot]')
        return 2

    # 2. construction de l'automate (parties 2, 3 et 4)
    try:
        automate = AnalyseurSyntaxique(expression).analyser()
    except (SyntaxError, ValueError) as e:
        print(e)
        return 1                      # expression invalide : code de retour non nul

    # 3. export Graphviz si demandé
    if fichier_dot is not None:
        exporter_dot(automate, fichier_dot)

    # 4. sans mot à tester : on se contente de valider l'expression (partie 2)
    if not mots:
        print("Expression valide")

    # 5. simulation : une ligne par mot
    for mot in mots:
        if accepte(automate, mot):
            print(afficher_mot(mot), ": OUI")
        else:
            print(afficher_mot(mot), ": NON")

    return 0


if __name__ == "__main__":
    # sous Windows, une sortie redirigée n'est pas en UTF-8 par défaut :
    # on l'impose pour que les accents des messages s'affichent sans erreur
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    # la descente récursive consomme plusieurs appels par niveau d'imbrication
    sys.setrecursionlimit(20000)
    sys.exit(main(sys.argv[1:]))
