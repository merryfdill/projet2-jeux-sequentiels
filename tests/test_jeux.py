
import pytest

from src.jeux import backward_induction, jeu_entree


def test_jeu_entree():
    """Vérifie le résultat attendu du jeu d'entrée du cours."""
    resultat = backward_induction(jeu_entree())

    assert resultat["gains"] == [2, 2]
    assert resultat["plan"]["racine"] == "Entrer"
    assert resultat["plan"]["racine/Entrer"] == "Accepter"
    assert resultat["chemin"] == ["Entrer", "Accepter"]


def test_joueur_1_maximise_son_propre_gain():
    """Vérifie que le joueur 1 maximise la deuxième composante."""
    jeu = {
        "joueur": 1,
        "actions": {
            "A": {"gains": [5, 1]},
            "B": {"gains": [0, 3]}
        }
    }

    resultat = backward_induction(jeu)

    assert resultat["gains"] == [0, 3]
    assert resultat["plan"]["racine"] == "B"
    assert resultat["chemin"] == ["B"]


def test_egalite_conserve_premiere_action():
    """Vérifie le comportement actuel en cas d'égalité."""
    jeu = {
        "joueur": 0,
        "actions": {
            "Premiere": {"gains": [5, 0]},
            "Deuxieme": {"gains": [5, 10]}
        }
    }

    resultat = backward_induction(jeu)

    assert resultat["gains"] == [5, 0]
    assert resultat["plan"]["racine"] == "Premiere"


def test_plan_complet_inclut_les_noeuds_hors_chemin():
    """Vérifie que les décisions hors du chemin joué sont conservées."""
    jeu = {
        "joueur": 0,
        "actions": {
            "Gauche": {"gains": [3, 0]},
            "Droite": {
                "joueur": 1,
                "actions": {
                    "A": {"gains": [0, 2]},
                    "B": {"gains": [0, 5]}
                }
            }
        }
    }

    resultat = backward_induction(jeu)

    assert resultat["plan"]["racine"] == "Gauche"
    assert resultat["plan"]["racine/Droite"] == "B"
    assert resultat["chemin"] == ["Gauche"]


def test_feuille_unique():
    """Vérifie le comportement lorsque le jeu est déjà terminé."""
    jeu = {"gains": [7, 4]}

    resultat = backward_induction(jeu)

    assert resultat == {
        "gains": [7, 4],
        "plan": {},
        "chemin": []
    }


def test_gains_negatifs():
    """Vérifie que le joueur choisit le gain le moins négatif."""
    jeu = {
        "joueur": 0,
        "actions": {
            "A": {"gains": [-5, 2]},
            "B": {"gains": [-2, 1]}
        }
    }

    resultat = backward_induction(jeu)

    assert resultat["gains"] == [-2, 1]
    assert resultat["plan"]["racine"] == "B"


def test_gains_decimaux():
    """Vérifie le traitement des gains décimaux."""
    jeu = {
        "joueur": 0,
        "actions": {
            "A": {"gains": [2.5, 1.5]},
            "B": {"gains": [3.75, 1.0]}
        }
    }

    resultat = backward_induction(jeu)

    assert resultat["gains"] == [3.75, 1.0]
    assert resultat["plan"]["racine"] == "B"


def test_egalite_avec_tolerance():
    """Vérifie que deux gains proches sont considérés comme égaux."""
    jeu = {
        "joueur": 0,
        "actions": {
            "A": {"gains": [5.0, 2]},
            "B": {"gains": [5.0 + 5e-10, 3]}
        }
    }

    resultat = backward_induction(jeu)

    # La différence est inférieure à TOL = 1e-9.
    # La première action doit donc être conservée.
    assert resultat["plan"]["racine"] == "A"
    assert resultat["gains"] == [5.0, 2]
