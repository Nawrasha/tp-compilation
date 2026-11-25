
from lexer import analyse_lexicale
from automate import Thompson


# Nom de chaque nature de jeton dans les messages d'erreur
NOMS = {
    "SYMBOLE": "symbole",
    "MOT_VIDE": "'@'",
    "UNION": "'|'",
    "ETOILE": "'*'",
    "PLUS": "'+'",
    "OPTIONNEL": "'?'",
    "PARENTHESE_OUVRANTE": "'('",
    "PARENTHESE_FERMANTE": "')'",
    "FIN": "fin de l'expression",
}


class AnalyseurSyntaxique:

    def __init__(self, expression):

        self.tokens = analyse_lexicale(expression)
        self.pos = 0
        self.th = Thompson()

    def courant(self):

        return self.tokens[self.pos]

    def avancer(self):

        if self.pos < len(self.tokens) - 1:
            self.pos = self.pos + 1

    def erreur(self, attendus):

        # attendus : liste des natures de jetons acceptables a cet endroit
        t = self.courant()

        noms = [NOMS[n] for n in attendus]

        if len(noms) == 1:
            texte_attendu = noms[0]
        else:
            texte_attendu = ", ".join(noms[:-1]) + " ou " + noms[-1]

        if t.nature == "FIN":
            texte_trouve = "fin de l'expression"
        else:
            texte_trouve = "'" + t.valeur + "'"

        raise SyntaxError(
            "Erreur à la position " + str(t.position)
            + " : " + texte_attendu + " attendu, "
            + texte_trouve + " trouvé"
        )

    def accepter(self, nature):

        if self.courant().nature == nature:
            self.avancer()
        else:
            self.erreur([nature])

    # Lancement de l'analyse
    def analyser(self):

        resultat = self.Z()

        # a ce stade, seul ')' peut rester (les autres jetons sont consommes
        # ou deja signales) : on attend la fin de l'expression
        if self.courant().nature != "FIN":
            self.erreur(["FIN"])

        return resultat

    # Production 0 : Z -> R
    def Z(self):

        num = 0

        resultat, suiv = self.R(num)

        return resultat

    # Production 1 : R -> T R'
    def R(self, num):

        a, suiv = self.T(num)

        resultat, suiv = self.R_prime(a, suiv)

        return resultat, suiv

    # Productions 2 et 3
    def R_prime(self, h, num):

        # R' -> | T R'
        if self.courant().nature == "UNION":

            self.avancer()

            b, suiv = self.T(num)

            resultat = self.th.union(h, b, suiv)

            num = suiv + 2

            resultat, suiv = self.R_prime(resultat, num)

            return resultat, suiv

        # R' -> epsilon
        elif self.courant().nature in [
            "PARENTHESE_FERMANTE",
            "FIN"
        ]:

            return h, num

        else:

            self.erreur(["UNION", "PARENTHESE_FERMANTE", "FIN"])

    # Production 4 : T -> F T'
    def T(self, num):

        a, suiv = self.F(num)

        resultat, suiv = self.T_prime(a, suiv)

        return resultat, suiv

    # Productions 5 et 6
    def T_prime(self, h, num):

        # T' -> F T'
        if self.courant().nature in [
            "SYMBOLE",
            "MOT_VIDE",
            "PARENTHESE_OUVRANTE"
        ]:

            b, suiv = self.F(num)

            resultat = self.th.concatener(h, b)

            num = suiv

            resultat, suiv = self.T_prime(resultat, num)

            return resultat, suiv

        # T' -> epsilon
        elif self.courant().nature in [
            "UNION",
            "PARENTHESE_FERMANTE",
            "FIN"
        ]:

            return h, num

        else:

            self.erreur(["SYMBOLE", "MOT_VIDE", "PARENTHESE_OUVRANTE",
                         "UNION", "PARENTHESE_FERMANTE", "FIN"])

    # Production 7 : F -> A F'
    def F(self, num):

        a, suiv = self.A(num)

        resultat, suiv = self.F_prime(a, suiv)

        return resultat, suiv

    # Productions 8, 9, 10 et 11
    def F_prime(self, h, num):

        nature = self.courant().nature

        # F' -> * F'
        if nature == "ETOILE":

            self.avancer()

            resultat = self.th.etoile(h, num)

            num = num + 2

            resultat, suiv = self.F_prime(resultat, num)

            return resultat, suiv

        # F' -> + F'
        elif nature == "PLUS":

            self.avancer()

            resultat = self.th.plus(h, num)

            num = num + 2

            resultat, suiv = self.F_prime(resultat, num)

            return resultat, suiv

        # F' -> ? F'
        elif nature == "OPTIONNEL":

            self.avancer()

            resultat = self.th.optionnel(h, num)

            num = num + 2

            resultat, suiv = self.F_prime(resultat, num)

            return resultat, suiv

        # F' -> epsilon
        elif nature in [
            "SYMBOLE",
            "MOT_VIDE",
            "PARENTHESE_OUVRANTE",
            "UNION",
            "PARENTHESE_FERMANTE",
            "FIN"
        ]:

            return h, num

        else:

            self.erreur(["ETOILE", "PLUS", "OPTIONNEL", "SYMBOLE", "MOT_VIDE",
                         "PARENTHESE_OUVRANTE", "UNION",
                         "PARENTHESE_FERMANTE", "FIN"])

    # Productions 12, 13 et 14
    def A(self, num):

        nature = self.courant().nature

        # A -> ( R )
        if nature == "PARENTHESE_OUVRANTE":

            self.avancer()

            resultat, suiv = self.R(num)

            self.accepter("PARENTHESE_FERMANTE")

            return resultat, suiv

        # A -> SYMBOLE
        elif nature == "SYMBOLE":

            c = self.courant().valeur

            self.avancer()

            resultat = self.th.symbole(c, num)

            suiv = num + 2

            return resultat, suiv

        # A -> @
        elif nature == "MOT_VIDE":

            self.avancer()

            resultat = self.th.mot_vide(num)

            suiv = num + 2

            return resultat, suiv

        else:

            self.erreur(["PARENTHESE_OUVRANTE", "SYMBOLE", "MOT_VIDE"])
