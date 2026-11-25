
class Automate:

    def __init__(self, initial, final, transitions):
        self.initial = initial
        self.final = final
        self.transitions = transitions


class Thompson:

    # Construction d'un symbole
    def symbole(self, c, num):

        debut = num
        fin = num + 1

        transitions = [(debut, c, fin)]

        return Automate(debut, fin, transitions)

    # Construction du mot vide
    def mot_vide(self, num):

        debut = num
        fin = num + 1

        transitions = [(debut, "ε", fin)]

        return Automate(debut, fin, transitions)

    # Concatenation
    def concatener(self, a, b):

        transitions = a.transitions + b.transitions

        transitions.append((a.final, "ε", b.initial))

        return Automate(a.initial, b.final, transitions)

    # Union
    def union(self, a, b, num):

        debut = num
        fin = num + 1

        transitions = a.transitions + b.transitions

        transitions.append((debut, "ε", a.initial))
        transitions.append((debut, "ε", b.initial))
        transitions.append((a.final, "ε", fin))
        transitions.append((b.final, "ε", fin))

        return Automate(debut, fin, transitions)

    # Etoile de Kleene
    def etoile(self, a, num):

        debut = num
        fin = num + 1

        transitions = a.transitions.copy()

        transitions.append((debut, "ε", a.initial))
        transitions.append((debut, "ε", fin))
        transitions.append((a.final, "ε", a.initial))
        transitions.append((a.final, "ε", fin))

        return Automate(debut, fin, transitions)

    # Operateur plus
    def plus(self, a, num):

        debut = num
        fin = num + 1

        transitions = a.transitions.copy()

        transitions.append((debut, "ε", a.initial))
        transitions.append((a.final, "ε", a.initial))
        transitions.append((a.final, "ε", fin))

        return Automate(debut, fin, transitions)

    # Operateur optionnel
    def optionnel(self, a, num):

        debut = num
        fin = num + 1

        transitions = a.transitions.copy()

        transitions.append((debut, "ε", a.initial))
        transitions.append((debut, "ε", fin))
        transitions.append((a.final, "ε", fin))

        return Automate(debut, fin, transitions)
