"""Tests de verification S2 (partie Quant). Les tests complets sont ceux d'Imane."""
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from src.jeux import (backward_induction, backward_induction_tous, est_nash,
                      jeu_entree, sous_jeu_simultane, stackelberg, ultimatum)


def test_eps_jeu_entree():
    r = backward_induction(jeu_entree())
    assert r["chemin"] == ["Entrer", "Accepter"] and r["gains"] == [2, 2]


def test_plan_contient_les_noeuds_hors_chemin():
    arbre = {"joueur": 0, "actions": {
        "G": {"joueur": 1, "actions": {"a": {"gains": [3, 1]}, "b": {"gains": [0, 0]}}},
        "D": {"joueur": 1, "actions": {"c": {"gains": [1, 2]}, "d": {"gains": [0, 0]}}}}}
    plan = backward_induction_tous(arbre)[0]["plan"]
    assert set(plan) == {"racine", "racine/G", "racine/D"}


def test_egalite_deux_plans():
    arbre = {"joueur": 0, "actions": {"G": {"gains": [1, 0]}, "D": {"gains": [1, 5]}}}
    assert len(backward_induction_tous(arbre)) == 2
    assert backward_induction(arbre)["plan"]["racine"] == "G"      # premiere action


def test_stackelberg_ferme_et_grille():
    r = stackelberg(100, 1, 10)
    assert r["q_meneur"] == 45 and r["q_suiveur"] == 22.5
    assert r["profit_meneur"] == pytest.approx(1012.5)
    assert r["verification_grille"]["coincide"]
    assert r["verification_grille"]["q_meneur_grille"] == 45


def test_ultimatum():
    assert ultimatum(10, True)["offres_eps"] == [0]
    assert ultimatum(10, False)["offres_eps"] == [1]
    assert ultimatum(10, None)["offres_eps"] == [0, 1]


def test_sous_jeu_dilemme_et_bataille_des_sexes():
    dil = sous_jeu_simultane([[3, 0], [5, 1]], [[3, 5], [0, 1]])
    assert dil["gains"] == [1.0, 1.0]
    A, B = [[2, 0], [0, 1]], [[1, 0], [0, 2]]
    bs = sous_jeu_simultane(A, B)
    assert len(bs["equilibres"]) == 3
    mixte = [e for e in bs["equilibres"] if e["type"] == "mixte"][0]
    assert mixte["x"] == pytest.approx([2 / 3, 1 / 3])
    assert mixte["y"] == pytest.approx([1 / 3, 2 / 3])
    for e in bs["equilibres"]:
        assert est_nash(A, B, e["x"], e["y"])


def test_pierre_feuille_ciseaux():
    A = [[0, -1, 1], [1, 0, -1], [-1, 1, 0]]
    B = [[0, 1, -1], [-1, 0, 1], [1, -1, 0]]
    eq = sous_jeu_simultane(A, B)["equilibres"][0]
    assert eq["x"] == pytest.approx([1 / 3] * 3)


def test_sous_jeu_dans_un_arbre():
    arbre = {"joueur": 0, "actions": {
        "Entrer": {"sous_jeu": {"A": [[3, 0], [5, 1]], "B": [[3, 5], [0, 1]]}},
        "Rester": {"gains": [0, 2]}}}
    assert backward_induction(arbre)["gains"] == [1.0, 1.0]
