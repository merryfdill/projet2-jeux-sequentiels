# Analyse des fonctions du cours à étendre - Projet 2 (S1)

Auteure : Yasmine (Quant / Python)

## `backward_induction` du cours
- Information parfaite, un seul plan, **première action gardée en cas d'égalité**.
- Pas de gestion des sous-jeux simultanés.
- Le plan renvoyé doit contenir l'action à **chaque** nœud (hors chemin joué inclus).

## Fonctions à écrire dans `src/jeux.py`

| Fonction | Semaine | Rôle | Test prévu |
|---|---|---|---|
| `backward_induction_tous(noeud)` | S2 | tous les plans optimaux en cas d'égalité | cas d'égalité : 2 plans |
| `sous_jeu_simultane(A, B)` | S2 | équilibre du sous-jeu (dominance, supports) → gains | dilemme, bataille des sexes |
| `stackelberg(a, b, c)` | S2 | formules fermées + vérification par induction à rebours | q1 = 45, q2 = 22,5 |
| `ultimatum(total=10)` | S2 | arbre JSON puis résolution | offre min. si le répondant accepte l'indifférence, sinon 1 |
| `mille_pattes(n)` | S3 | n étapes, Stop dès la 1re étape | n = 3 puis n quelconque |

## Conventions à fixer avec les autres groupes
- Groupe 1 (solveur de Nash) : A = gains de J1 en lignes, B = gains de J2 en colonnes, indices à partir de 0.
- Groupe 6 : chaîne « prompt | modèle | parser », format « CHOIX : ... ».

## Points de vigilance
- Comparer les flottants avec une tolérance (`TOL`).
- Ne pas confondre stratégie (plan complet) et chemin joué.
