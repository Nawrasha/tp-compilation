Langage : Python 3 (>= 3.8), bibliothèque standard uniquement. Graphviz (dot) pour les images.

Commande Python selon le système :
    Linux / macOS : python3
    Windows       : python   (ou py)
Dans les exemples ci-dessous, remplacer "python3" par "python" sous Windows.

Exécution (depuis le dossier du projet) :
    python3 src/main.py "(a|b)*abb" abb aabb ab
    python3 src/main.py "(a|b)*abb" abb --dot automates/exemple.dot
    python3 src/main.py "a*" ""                  # "" = mot vide
    python3 src/main.py "(a|b)*abb"              # affiche : Expression valide
    dot -Tpng automates/exemple.dot -o automates/exemple.png

Sortie : une ligne par mot, par exemple  abb : OUI
Sans mot à tester : « Expression valide » (ou le message d'erreur).
Code de retour : 0 expression valide, 1 expression invalide, 2 commande mal utilisée.

Tests de la partie 5 :
    cd src
    python3 test_partie5.py

Jeu de tests complet (partie 6) :
    python3 tests/lancer_tests.py
    -> tests/tests.txt (16 expressions), tests/erreurs.txt (9 erreurs), contrôle des 2n états
