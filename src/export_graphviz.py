"""
Partie 5 – Export Graphviz.

Écrit l'automate dans un fichier .dot :
  - l'état initial est signalé par une flèche entrante (noeud __start) ;
  - l'état d'acceptation est dessiné en double cercle ;
  - les ε-transitions sont étiquetées ε ;
  - les transitions parallèles (même source, même cible) sont regroupées
    en une seule arête, avec une étiquette telle que a,b.

Visualisation : dot -Tpng automate.dot -o automate.png
"""


def regrouper_transitions(transitions):
    """
    Regroupe les étiquettes des transitions qui ont la même source et la même cible.
    Exemple : [(0,'a',1), (0,'b',1)]  ->  {(0,1): ['a', 'b']}
    L'ordre d'apparition est conservé et une étiquette n'est jamais répétée.
    """
    aretes = {}

    for (source, etiquette, cible) in transitions:

        if (source, cible) not in aretes:
            aretes[(source, cible)] = []

        if etiquette not in aretes[(source, cible)]:
            aretes[(source, cible)].append(etiquette)

    return aretes


def automate_vers_dot(automate):
    """Renvoie le texte du fichier .dot de l'automate."""
    lignes = []

    lignes.append("digraph AFN {")
    lignes.append("  rankdir=LR;")
    lignes.append("  node [shape=circle];")

    # état initial : flèche entrante venant d'un point invisible
    lignes.append("  __start [shape=point];")
    lignes.append("  __start -> " + str(automate.initial) + ";")

    # état d'acceptation : double cercle
    lignes.append("  " + str(automate.final) + " [shape=doublecircle];")

    # une seule arête par couple (source, cible)
    aretes = regrouper_transitions(automate.transitions)

    for (source, cible), etiquettes in aretes.items():
        label = ",".join(etiquettes)
        lignes.append("  " + str(source) + " -> " + str(cible)
                      + " [label=\"" + label + "\"];")

    lignes.append("}")

    return "\n".join(lignes) + "\n"


def exporter_dot(automate, nom_fichier):
    """Écrit l'automate dans le fichier nom_fichier (encodage UTF-8 pour ε)."""
    with open(nom_fichier, "w", encoding="utf-8") as f:
        f.write(automate_vers_dot(automate))
