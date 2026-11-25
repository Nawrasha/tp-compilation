"""Tests de la partie 5 :  python3 test_partie5.py"""

import os
import subprocess
import sys
import tempfile
import unittest

from analyseur_syntaxique import AnalyseurSyntaxique
from automate import Automate
from export_graphviz import automate_vers_dot, regrouper_transitions
from simulation import accepte, epsilon_fermeture

sys.setrecursionlimit(20000)
ICI = os.path.dirname(os.path.abspath(__file__))


def construire(expression):
    return AnalyseurSyntaxique(expression).analyser()


# (expression, mots acceptés, mots rejetés) – "" = mot vide
CAS = [
    ("a", ["a"], ["b", "aa", ""]),
    ("a|b", ["a", "b"], ["ab", ""]),
    ("ab*", ["a", "abbb"], ["b", "aba"]),
    ("(a|b)*abb", ["abb", "aabb", "babb"], ["ab", "abba", ""]),
    ("(ab)+", ["ab", "abab"], ["aba", ""]),
    ("a?b", ["b", "ab"], ["a", "aab"]),
    ("(a*)*", ["a", "aaa", ""], ["b"]),
    ("a(b|c)*d", ["ad", "abcbd"], ["a", "abc"]),
    ("@", [""], ["a"]),
    ("a*+", ["", "a", "aaaa"], ["b"]),
    ("(((a*)*)*)", ["", "aaa"], ["ab"]),
]


class TestSimulation(unittest.TestCase):
    def test_cas_de_l_enonce(self):
        for expression, oui, non in CAS:
            automate = construire(expression)
            for mot in oui:
                with self.subTest(expression=expression, mot=mot):
                    self.assertTrue(accepte(automate, mot))
            for mot in non:
                with self.subTest(expression=expression, mot=mot):
                    self.assertFalse(accepte(automate, mot))

    def test_fermeture_termine_sur_un_cycle(self):
        # cycle d'ε : 0 -> 1 -> 2 -> 0 ; le parcours doit s'arrêter
        a = Automate(0, 2, [(0, "ε", 1), (1, "ε", 2), (2, "ε", 0)])
        self.assertEqual(epsilon_fermeture(a, {0}), {0, 1, 2})


class TestExportDot(unittest.TestCase):
    def test_regroupement_des_transitions_paralleles(self):
        aretes = regrouper_transitions([(0, "a", 1), (0, "b", 1), (0, "a", 1), (1, "ε", 2)])
        self.assertEqual(aretes, {(0, 1): ["a", "b"], (1, 2): ["ε"]})

    def test_contenu_du_fichier(self):
        a = Automate(0, 2, [(0, "a", 1), (0, "b", 1), (1, "ε", 2)])
        texte = automate_vers_dot(a)
        self.assertIn("rankdir=LR;", texte)
        self.assertIn("__start [shape=point];", texte)
        self.assertIn("__start -> 0;", texte)
        self.assertIn("2 [shape=doublecircle];", texte)
        self.assertIn('0 -> 1 [label="a,b"];', texte)
        self.assertIn('1 -> 2 [label="ε"];', texte)
        self.assertEqual(texte.count("0 -> 1"), 1)


class TestLigneDeCommande(unittest.TestCase):
    def lancer(self, *arguments):
        return subprocess.run([sys.executable, os.path.join(ICI, "main.py"), *arguments],
                              capture_output=True, text=True, encoding="utf-8")

    def test_exemple_de_l_enonce(self):
        r = self.lancer("(a|b)*abb", "abb", "aabb", "ab")
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout.splitlines(), ["abb : OUI", "aabb : OUI", "ab : NON"])

    def test_mot_vide(self):
        r = self.lancer("a*", "")
        self.assertEqual(r.stdout.strip(), '"" : OUI')

    def test_option_dot(self):
        with tempfile.TemporaryDirectory() as d:
            chemin = os.path.join(d, "automate.dot")
            r = self.lancer("a|b", "a", "--dot", chemin)
            self.assertEqual(r.returncode, 0)
            with open(chemin, encoding="utf-8") as f:
                self.assertTrue(f.read().startswith("digraph AFN {"))

    def test_expression_invalide(self):
        r = self.lancer("a||b", "ab")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("Erreur", r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
