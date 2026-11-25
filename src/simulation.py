"""
Partie 5 – Simulation de l'AFN sur un mot w.

  1. on calcule l'ε-fermeture de l'état initial ;
  2. pour chaque caractère c de w, l'ensemble courant S est remplacé par
     l'ε-fermeture des états atteints depuis S par une transition étiquetée c ;
  3. le mot est accepté si l'état d'acceptation appartient à l'ensemble final.
"""

EPSILON = "ε"


def epsilon_fermeture(automate, etats):
    """
    Ensemble des états accessibles depuis 'etats' en suivant uniquement des ε-transitions.

    Parcours en profondeur avec l'ensemble 'visites' des états déjà rencontrés :
    un état n'est jamais traité deux fois, ce qui évite de boucler à l'infini
    sur les cycles d'ε-transitions, par exemple avec (a*)*.
    """
    visites = set(etats)
    a_traiter = list(etats)          # pile des états dont on n'a pas encore suivi les ε

    while a_traiter:
        p = a_traiter.pop()

        for (source, etiquette, cible) in automate.transitions:
            if source == p and etiquette == EPSILON and cible not in visites:
                visites.add(cible)
                a_traiter.append(cible)

    return visites


def transiter(automate, etats, c):
    """Ensemble des états atteints depuis 'etats' par une transition étiquetée c."""
    atteints = set()

    for (source, etiquette, cible) in automate.transitions:
        if source in etats and etiquette == c:
            atteints.add(cible)

    return atteints


def accepte(automate, mot):
    """Renvoie True si l'automate reconnaît le mot, False sinon."""

    # 1. ε-fermeture de l'état initial
    S = epsilon_fermeture(automate, {automate.initial})

    # 2. lecture du mot, caractère par caractère
    for c in mot:
        S = epsilon_fermeture(automate, transiter(automate, S, c))

        if not S:                    # plus aucun état possible : inutile de continuer
            return False

    # 3. accepter si l'état d'acceptation est dans l'ensemble final
    return automate.final in S
