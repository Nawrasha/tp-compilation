class Token:

    def __init__(self, nature, valeur, position):
        self.nature = nature
        self.valeur = valeur
        self.position = position


def analyse_lexicale(expression):

    tokens = []
    i = 0

    while i < len(expression):

        c = expression[i]

        if c.isascii() and c.isalnum():
            nature = "SYMBOLE"

        elif c == "|":
            nature = "UNION"

        elif c == "*":
            nature = "ETOILE"

        elif c == "+":
            nature = "PLUS"

        elif c == "?":
            nature = "OPTIONNEL"

        elif c == "(":
            nature = "PARENTHESE_OUVRANTE"

        elif c == ")":
            nature = "PARENTHESE_FERMANTE"

        elif c == "@":
            nature = "MOT_VIDE"

        else:
            raise ValueError(
                "Erreur à la position " + str(i)
                + " : caractère '" + c + "' hors de l'alphabet"
            )

        tokens.append(Token(nature, c, i))

        i = i + 1

    tokens.append(Token("FIN", "", i))

    return tokens
