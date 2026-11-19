"""
src/jeux.py - Projet 2 : jeux sequentiels (Groupe 2, ENSA Safi)
Fonctions pures (sans LangChain).

Etat d'avancement
-----------------
  [S1] backward_induction (version du cours, un seul plan)      -> FAIT
  [S2] backward_induction_tous, sous_jeu_simultane, est_nash,
       stackelberg, ultimatum                                   -> FAIT
  [S3] mille_pattes a n etapes                                  -> A FAIRE

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

import itertools
import math

import numpy as np

TOL = 1e-9          # tolerance pour comparer des flottants
RACINE = "racine"


# ----------------------------------------------------------------------------
# Utilitaires
# ----------------------------------------------------------------------------
def _json(x):
    """Convertit recursivement les types NumPy en types Python (sortie JSON)."""
    if isinstance(x, dict):
        return {str(k): _json(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_json(v) for v in x]
    if isinstance(x, np.ndarray):
        return _json(x.tolist())
    if isinstance(x, np.integer):
        return int(x)
    if isinstance(x, np.floating):
        return float(x)
    return x


def _est_feuille(noeud):
    return "gains" in noeud


def _est_sous_jeu(noeud):
    return "sous_jeu" in noeud


# ----------------------------------------------------------------------------
# 1. Sous-jeu simultane : dominance stricte + enumeration des supports
# ----------------------------------------------------------------------------
def _elimination_dominance(A, B):
    """Elimination iterative des strategies pures strictement dominees.
    Retourne (lignes_restantes, colonnes_restantes) (indices d'origine)."""
    lignes = list(range(A.shape[0]))
    cols = list(range(A.shape[1]))
    change = True
    while change:
        change = False
        for i in lignes[:]:
            if any(all(A[k, j] > A[i, j] + TOL for j in cols) for k in lignes if k != i):
                lignes.remove(i)
                change = True
        for j in cols[:]:
            if any(all(B[i, l] > B[i, j] + TOL for i in lignes) for l in cols if l != j):
                cols.remove(j)
                change = True
    return lignes, cols


def est_nash(A, B, x, y, tol=TOL):
    """Verifie les deux conditions de non-deviation (J1 puis J2)."""
    A, B = np.asarray(A, float), np.asarray(B, float)
    x, y = np.asarray(x, float), np.asarray(y, float)
    u1, u2 = x @ A @ y, x @ B @ y
    return bool(np.max(A @ y) <= u1 + tol and np.max(x @ B) <= u2 + tol)


def sous_jeu_simultane(A, B, tol=TOL):
    """Equilibres de Nash d'un jeu bimatrice (dominance, puis supports de meme taille).

    Retourne {"equilibres": [{"x", "y", "gains", "type"}, ...],
              "gains": gains du 1er equilibre (les purs d'abord),
              "elimine": {"lignes": [...], "colonnes": [...]}}.
    Hypothese : jeu non degenere (sinon des equilibres peuvent manquer).
    """
    A, B = np.asarray(A, float), np.asarray(B, float)
    if A.shape != B.shape:
        raise ValueError("A et B doivent avoir la meme forme")
    m, n = A.shape
    L, C = _elimination_dominance(A, B)
    Ar, Br = A[np.ix_(L, C)], B[np.ix_(L, C)]
    mr, nr = Ar.shape
    trouves = []
    for k in range(1, min(mr, nr) + 1):
        for I in itertools.combinations(range(mr), k):
            for J in itertools.combinations(range(nr), k):
                I_, J_ = list(I), list(J)
                # y sur J rend J1 indifferent sur I : A[I,J] y = v1 ; somme y = 1
                M = np.zeros((k + 1, k + 1))
                M[:k, :k] = Ar[np.ix_(I_, J_)]
                M[:k, k] = -1.0
                M[k, :k] = 1.0
                rhs = np.zeros(k + 1)
                rhs[k] = 1.0
                # x sur I rend J2 indifferent sur J : B[I,J]^T x = v2 ; somme x = 1
                N = np.zeros((k + 1, k + 1))
                N[:k, :k] = Br[np.ix_(I_, J_)].T
                N[:k, k] = -1.0
                N[k, :k] = 1.0
                try:
                    ysol = np.linalg.solve(M, rhs)
                    xsol = np.linalg.solve(N, rhs)
                except np.linalg.LinAlgError:
                    continue
                yJ, xI = ysol[:k], xsol[:k]
                if np.any(yJ <= tol) or np.any(xI <= tol):
                    continue
                x = np.zeros(mr)
                y = np.zeros(nr)
                x[I_], y[J_] = xI, yJ
                if not est_nash(Ar, Br, x, y, 1e-7):    # non-deviation hors des supports
                    continue
                X, Y = np.zeros(m), np.zeros(n)
                X[L], Y[C] = x, y
                if any(np.allclose(X, e["x"], atol=1e-7) and np.allclose(Y, e["y"], atol=1e-7)
                       for e in trouves):
                    continue
                trouves.append({"x": X, "y": Y,
                                "gains": [float(X @ A @ Y), float(X @ B @ Y)],
                                "type": "pur" if k == 1 else "mixte"})
    if not trouves:
        raise ValueError("Aucun equilibre trouve (jeu degenere ?)")
    return _json({"equilibres": trouves, "gains": trouves[0]["gains"],
                  "elimine": {"lignes": sorted(set(range(m)) - set(L)),
                              "colonnes": sorted(set(range(n)) - set(C))}})


# ----------------------------------------------------------------------------
# 2. Induction a rebours : un plan (cours) ou tous les plans (egalites)
# ----------------------------------------------------------------------------
def _options(noeud, id_, tous, prefere, max_plans):
    """Liste de (gains, plan) : un element par plan optimal (tous=True) ou un seul."""
    if _est_feuille(noeud):
        return [(tuple(noeud["gains"]), {})]

    if _est_sous_jeu(noeud):
        sj = noeud["sous_jeu"]
        res = sous_jeu_simultane(sj["A"], sj["B"])
        eqs = res["equilibres"] if tous else res["equilibres"][:1]
        return [(tuple(e["gains"]), {id_: {"x": e["x"], "y": e["y"]}}) for e in eqs]

    j = noeud["joueur"]
    listes = {a: _options(s, f"{id_}/{a}", tous, prefere, max_plans)
              for a, s in noeud["actions"].items()}

    if not tous:   # comportement du cours : premiere action gardee en cas d'egalite
        meilleur, best_a = None, None
        for a, opts in listes.items():
            if meilleur is None or opts[0][0][j] > meilleur + TOL:
                meilleur, best_a = opts[0][0][j], a
        plan = {id_: best_a}
        for opts in listes.values():
            plan.update(opts[0][1])
        return [(listes[best_a][0][0], plan)]

    noms = list(listes)
    if math.prod(len(listes[a]) for a in noms) > max_plans:
        raise ValueError(f"Plus de {max_plans} plans optimaux : explosion combinatoire")
    resultats = []
    for combo in itertools.product(*(listes[a] for a in noms)):
        valeurs = [c[0][j] for c in combo]
        vmax = max(valeurs)
        meilleurs = [k for k, v in enumerate(valeurs) if v >= vmax - TOL]
        if prefere:                                   # departage les egalites
            pref = [k for k in meilleurs if noms[k] in prefere]
            meilleurs = pref or meilleurs
        plan_base = {}
        for c in combo:
            plan_base.update(c[1])
        for k in meilleurs:
            plan = dict(plan_base)
            plan[id_] = noms[k]
            resultats.append((combo[k][0], plan))
    return resultats


def chemin_joue(noeud, plan):
    """Suite d'actions jouees en suivant le plan depuis la racine."""
    chemin, id_ = [], RACINE
    while not _est_feuille(noeud) and not _est_sous_jeu(noeud):
        a = plan[id_]
        chemin.append(a)
        noeud, id_ = noeud["actions"][a], f"{id_}/{a}"
    if _est_sous_jeu(noeud):
        chemin.append("sous-jeu simultane")
    return chemin


def backward_induction(noeud):
    """Version du cours : un seul plan (premiere action gardee en cas d'egalite)."""
    gains, plan = _options(noeud, RACINE, False, None, 1)[0]
    return {"gains": list(gains), "plan": _json(plan), "chemin": chemin_joue(noeud, plan)}


def backward_induction_tous(noeud, prefere=None, max_plans=1000):
    """TOUS les plans optimaux (equilibres parfaits en sous-jeux purs).

    prefere   : liste d'actions departageant les egalites (ex. ["Accepter"]) ;
    max_plans : plafond contre l'explosion combinatoire.
    Chaque plan contient l'action a chaque noeud, hors chemin joue compris."""
    opts = _options(noeud, RACINE, True, prefere, max_plans)
    if len(opts) > max_plans:
        raise ValueError(f"Plus de {max_plans} plans optimaux")
    return [{"gains": list(g), "plan": _json(p), "chemin": chemin_joue(noeud, p)}
            for g, p in opts]


# ----------------------------------------------------------------------------
# 3. Stackelberg
# ----------------------------------------------------------------------------
def stackelberg_arbre(a, b, c, pas_meneur=5.0, pas_suiveur=2.5, qmax=None):
    """Arbre discret : le meneur choisit q1 sur une grille, puis le suiveur q2.
    Astuce : pas_meneur = 2 * pas_suiveur. La meilleure reponse (a-c-b q1)/(2b)
    tombe alors toujours sur la grille du suiveur : pas d'egalites artificielles
    dont le meneur profiterait (avec deux grilles identiques, il gagne trop)."""
    qmax = (a - c) / b if qmax is None else qmax
    g_m = [round(k * pas_meneur, 10) for k in range(int(qmax / pas_meneur) + 1)]
    g_s = [round(k * pas_suiveur, 10) for k in range(int(qmax / pas_suiveur) + 1)]
    arbre = {"joueur": 0, "actions": {}}
    for q1 in g_m:
        suiveur = {"joueur": 1, "actions": {}}
        for q2 in g_s:
            p = max(a - b * (q1 + q2), 0.0)
            suiveur["actions"][f"{q2:g}"] = {"gains": [q1 * (p - c), q2 * (p - c)]}
        arbre["actions"][f"{q1:g}"] = suiveur
    return arbre


def stackelberg(a, b, c, verifier=True, pas_meneur=5.0, pas_suiveur=2.5):
    """Formules fermees de Stackelberg (+ verification par induction a rebours sur grille).
    Demande P = a - b Q, cout marginal c, a > c."""
    if not (a > c and b > 0):
        raise ValueError("Il faut a > c et b > 0")
    q1 = (a - c) / (2 * b)
    q2 = (a - c) / (4 * b)
    res = {"q_meneur": q1, "q_suiveur": q2, "Q": q1 + q2,
           "prix": a - b * (q1 + q2),
           "profit_meneur": (a - c) ** 2 / (8 * b),
           "profit_suiveur": (a - c) ** 2 / (16 * b)}
    if verifier:
        sol = backward_induction(stackelberg_arbre(a, b, c, pas_meneur, pas_suiveur))
        g1, g2 = float(sol["chemin"][0]), float(sol["chemin"][1])
        res["verification_grille"] = {
            "pas_meneur": pas_meneur, "pas_suiveur": pas_suiveur,
            "q_meneur_grille": g1, "q_suiveur_grille": g2,
            "gains_grille": sol["gains"],
            "coincide": abs(g1 - q1) <= pas_meneur / 2 + TOL
                        and abs(g2 - q2) <= pas_suiveur / 2 + TOL}
    return _json(res)


# ----------------------------------------------------------------------------
# 4. Ultimatum
# ----------------------------------------------------------------------------
def construire_ultimatum(total=10):
    """Arbre JSON : le proposant offre x dans {0..total}; le repondant accepte ou refuse."""
    return {"joueur": 0, "actions": {
        f"offre_{x}": {"joueur": 1, "actions": {
            "Accepter": {"gains": [total - x, x]},
            "Refuser": {"gains": [0, 0]}}}
        for x in range(total + 1)}}


def ultimatum(total=10, accepte_indifference=True):
    """Construit l'arbre puis le resout.

    accepte_indifference=True  : le repondant accepte quand il est indifferent -> offre 0
    accepte_indifference=False : il refuse quand il est indifferent -> offre de 1 unite
    accepte_indifference=None  : tous les EPS (les deux cas)."""
    arbre = construire_ultimatum(total)
    prefere = None if accepte_indifference is None else (
        ["Accepter"] if accepte_indifference else ["Refuser"])
    plans = backward_induction_tous(arbre, prefere=prefere)
    offres = sorted({int(p["chemin"][0].split("_")[1]) for p in plans})
    return {"total": total, "accepte_indifference": accepte_indifference,
            "offres_eps": offres, "gains": plans[0]["gains"],
            "nb_plans": len(plans), "plans": plans, "arbre": arbre}


# ----------------------------------------------------------------------------
# A coder (S3)
# ----------------------------------------------------------------------------
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
    import json
    print("EPS jeu d'entree  :", backward_induction(jeu_entree()))
    print("Stackelberg       :", json.dumps(stackelberg(100, 1, 10)))
    for acc in (True, False, None):
        u = ultimatum(10, acc)
        print("Ultimatum", acc, ":", "offres EPS", u["offres_eps"], "gains", u["gains"])
    print("Sous-jeu (dilemme):", sous_jeu_simultane([[3, 0], [5, 1]], [[3, 5], [0, 1]])["gains"])
