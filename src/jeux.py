"""
src/jeux.py - Projet 2 : jeux sequentiels (Groupe 2, ENSA Safi)
Semaine 1 : squelette du module (fonctions pures, sans LangChain).

Etat d'avancement
-----------------
  [S1] backward_induction (version du cours, un seul plan)  -> FAIT
  [S2] backward_induction_tous, sous_jeu_simultane,
       stackelberg, ultimatum                               -> A FAIRE
  [S3] mille_pattes a n etapes                              -> A FAIRE

Conventions
-----------
* Joueurs indices a partir de 0 (J1 = 0, J2 = 1).
* A = gains de J1 (lignes), B = gains de J2 (colonnes), indices a partir de 0
  (meme convention que le Groupe 1).
* Format d'arbre (compatible JSON) :
    - feuille            : {"gains": [g1, g2]}
    - noeud de decision  : {"joueur": 0 ou 1, "actions": {"Nom": sous_arbre, ...}}
    - sous-jeu simultane : {"sous_jeu": {"A": [[..]], "B": [[..]]}}
* Identifiant d'un noeud = chemin des actions depuis la racine ("racine/Entrer").
  Un PLAN associe une action a CHAQUE noeud de decision, y compris hors du
  chemin joue : {"racine": "Entrer", "racine/Entrer": "Accepter"}.
"""
from __future__ import annotations

TOL = 1e-9          # tolerance pour comparer des flottants
RACINE = "racine"


# ----------------------------------------------------------------------------
# Utilitaires
# ----------------------------------------------------------------------------
def _est_feuille(noeud):
    return "gains" in noeud


def _est_sous_jeu(noeud):
    return "sous_jeu" in noeud


# ----------------------------------------------------------------------------
# Induction a rebours : version du cours (un seul plan)
# ----------------------------------------------------------------------------
def _resoudre(noeud, id_):
    """Retourne (gains, plan) pour le sous-arbre de racine `noeud`."""
    if _est_feuille(noeud):
        return tuple(noeud["gains"]), {}
    j = noeud["joueur"]
    meilleur, best_a, plan = None, None, {}
    for action, sous_arbre in noeud["actions"].items():
        gains, sous_plan = _resoudre(sous_arbre, f"{id_}/{action}")
        plan.update(sous_plan)                       # plan complet, hors chemin joue inclus
        if meilleur is None or gains[j] > meilleur[j] + TOL:   # egalite : 1re action gardee
            meilleur, best_a = gains, action
    plan[id_] = best_a
    return meilleur, plan


def chemin_joue(noeud, plan):
    """Suite d'actions jouees en suivant le plan depuis la racine."""
    chemin, id_ = [], RACINE
    while not _est_feuille(noeud):
        a = plan[id_]
        chemin.append(a)
        noeud, id_ = noeud["actions"][a], f"{id_}/{a}"
    return chemin


def backward_induction(noeud):
    """Induction a rebours (information parfaite) : un plan optimal.
    En cas d'egalite, la premiere action est gardee (comportement du cours)."""
    gains, plan = _resoudre(noeud, RACINE)
    return {"gains": list(gains), "plan": plan, "chemin": chemin_joue(noeud, plan)}


# ----------------------------------------------------------------------------
# A coder (S2 et S3)
# ----------------------------------------------------------------------------
def backward_induction_tous(noeud, prefere=None, max_plans=1000):
    """[S2] TOUS les plans optimaux en cas d'egalite (EPS purs)."""
    raise NotImplementedError("S2")


def sous_jeu_simultane(A, B):
    """[S2] Equilibre(s) de Nash d'un sous-jeu simultane (dominance, supports) -> gains."""
    raise NotImplementedError("S2")


def stackelberg(a, b, c):
    """[S2] Formules fermees + verification par induction a rebours sur grille."""
    raise NotImplementedError("S2")


def ultimatum(total=10):
    """[S2] Construit l'arbre JSON de l'ultimatum puis le resout."""
    raise NotImplementedError("S2")


def mille_pattes(n=3):
    """[S3] Arbre du mille-pattes a n etapes (Stop des la 1re etape predit)."""
    raise NotImplementedError("S3")


def jeu_entree():
    """Jeu d'entree : E (joueur 0) Entrer / Rester_dehors ; si Entrer, M (joueur 1)
    Accepter / Combattre. EPS attendu (cours) : Entrer, Accepter, gains (2, 2).
    ATTENTION : les gains hors EPS sont a REMPLACER par ceux du cours si differents."""
    return {"joueur": 0, "actions": {
        "Entrer": {"joueur": 1, "actions": {
            "Accepter": {"gains": [2, 2]}, "Combattre": {"gains": [0, 0]}}},
        "Rester_dehors": {"gains": [1, 5]}}}


if __name__ == "__main__":
    print("EPS jeu d'entree :", backward_induction(jeu_entree()))
