"""
Partie 6 – Lance tout le jeu de tests.

Usage (depuis le dossier du projet) :
    python3 tests/lancer_tests.py

1. tests.txt   : pour chaque expression, vérifie les mots acceptés et rejetés
                 et la propriété « au plus 2n états » ;
2. erreurs.txt : chaque expression doit être refusée par le programme
                 (message d'erreur + code de retour non nul).

Code de retour : 0 si tous les tests passent, 1 sinon.
"""

import os
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ICI, "..", "src")
sys.path.insert(0, SRC)
sys.setrecursionlimit(20000)

from analyseur_syntaxique import AnalyseurSyntaxique   # noqa: E402
from simulation import accepte                          # noqa: E402


def lignes_utiles(nom_fichier):
    """Lignes non vides et qui ne sont pas des commentaires (#)."""
    with open(os.path.join(ICI, nom_fichier), encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.strip()
            if ligne and not ligne.startswith("#"):
                yield ligne


def mots(champ):
    """'a @ ab' -> ['a', '', 'ab']  (@ représente le mot vide)."""
    return ["" if m == "@" else m for m in champ.split()]


def nombre_n(expression):
    """n = symboles, @, |, *, +, ? (la concaténation et les parenthèses ne comptent pas)."""
    return sum(1 for c in expression if c not in "()")


def nombre_etats(automate):
    etats = {automate.initial, automate.final}
    for (p, _, q) in automate.transitions:
        etats.add(p)
        etats.add(q)
    return len(etats)


def affiche(mot):
    return "@" if mot == "" else mot


def tester_expressions():
    echecs = 0
    total = 0

    print("=== Jeu de tests (tests.txt) ===")
    for ligne in lignes_utiles("tests.txt"):
        expression, oui, non = [champ.strip() for champ in ligne.split(";")]
        automate = AnalyseurSyntaxique(expression).analyser()
        problemes = []

        for mot in mots(oui):
            total += 1
            if not accepte(automate, mot):
                problemes.append(affiche(mot) + " devrait être accepté")
        for mot in mots(non):
            total += 1
            if accepte(automate, mot):
                problemes.append(affiche(mot) + " devrait être rejeté")

        # propriété : au plus 2n états
        total += 1
        n, etats = nombre_n(expression), nombre_etats(automate)
        if etats > 2 * n:
            problemes.append(str(etats) + " états > 2n = " + str(2 * n))

        statut = "OK " if not problemes else "ECHEC"
        print(f"  [{statut}] {expression:<14} {etats:>2} états <= 2n = {2 * n:<3}"
              + ("" if not problemes else " -> " + " ; ".join(problemes)))
        echecs += len(problemes)

    return total, echecs


def tester_erreurs():
    echecs = 0
    total = 0
    main = os.path.join(SRC, "main.py")

    print("=== Tests d'erreur (erreurs.txt) ===")
    for ligne in lignes_utiles("erreurs.txt"):
        expression, commentaire = [champ.strip() for champ in ligne.split(";", 1)]
        total += 1
        r = subprocess.run([sys.executable, main, expression],
                           capture_output=True, text=True, encoding="utf-8")
        message = (r.stdout + r.stderr).strip()
        refusee = r.returncode != 0 and message != ""
        if not refusee:
            echecs += 1
        statut = "OK " if refusee else "ECHEC"
        print(f"  [{statut}] {expression:<6} code {r.returncode}  {message}   ({commentaire})")

    return total, echecs


if __name__ == "__main__":
    # sous Windows, une sortie redirigée n'est pas en UTF-8 par défaut
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    t1, e1 = tester_expressions()
    t2, e2 = tester_erreurs()
    total, echecs = t1 + t2, e1 + e2
    print()
    print(f"{total - echecs}/{total} vérifications réussies")
    sys.exit(0 if echecs == 0 else 1)
