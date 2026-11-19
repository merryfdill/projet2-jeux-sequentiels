# Point d'avancement S1 – Cadrage et théorie

**Groupe 2 – Projet 2 : Jeux séquentiels** · Présenté par : Meryem (chef de projet / théorie) · Semaine 1

## 1. Travail réalisé

| Attendu S1 (guide du prof) | Responsable | Statut | Preuve dans le dépôt |
|---|---|---|---|
| Dépôt GitHub créé, 4 membres | Meryem | fait | dépôt + historique des commits |
| Fiche de lecture (Phase 0) | Meryem | fait | `docs/fiche_lecture.pdf` (source : `docs/fiche_de_lecture.md`) |
| Fonctions du cours à étendre identifiées | Yasmine | fait | `docs/analyse_fonctions_a_etendre.md`, squelette `src/jeux.py` |
| Gantt prévisionnel déposé | Meryem | fait | `docs/gantt_previsionnel.png` + source `docs/gantt_source.mmd` |
| Ollama installé, `ollama pull llama3.1` | Zineb | fait | captures dans l'annexe de `docs/fiche_lecture.pdf` |
| Cas de test listés, pytest installé | Imane | fait | `tests/test_jeux.py` : 8 tests, 8 passent |

Travail complémentaire :

- Format d'arbre JSON commun fixé (feuille, nœud de décision, sous-jeu simultané) et `backward_induction` du cours reprise dans `src/jeux.py`.
- Conventions du solveur de Nash validées avec le Groupe 1 (A = gains de J1 en lignes, B = gains de J2 en colonnes, indices à partir de 0).

## 2. Écarts prévu / réalisé

Aucun retard sur S1 : tous les jalons de la semaine sont tenus. Une tâche a été avancée : Zineb a déjà écrit un premier outil `@tool stackelberg` et l'amorce de la chaîne ultimatum (prévus en S2-S3).

## 3. Difficultés et blocages

- Affichage des formules LaTeX et du diagramme Mermaid sur GitHub : résolu.
- `agent_tj_sma.py` a été écrit à partir de zéro : il faut repartir de l'agent du cours (10 outils) et y ajouter nos outils (règle n°2). Correction prévue en S2.
- Gains hors EPS du jeu d'entrée et gains du mille-pattes à recopier exactement depuis le cours.

## 4. Plan de la semaine 2 (Prototype Python)

| Membre | Tâche S2 |
|---|---|
| Meryem | Rédiger et expliquer les formules ; discuter la sensibilité de l'ultimatum discret (offre 0 ou 1) |
| Yasmine | `backward_induction_tous`, `stackelberg(a, b, c)`, `ultimatum(total=10)`, `sous_jeu_simultane(A, B)` |
| Zineb | Repartir de l'agent du cours ; squelette des outils `@tool` et format JSON des arbres ; prototype de la chaîne pour le jeu d'entrée |
| Imane | Notebook qui vérifie les résultats du cours (EPS Entrer/Accepter, mille-pattes, Stackelberg) |

Prochain point d'avancement : **Yasmine**.

## 5. État du dépôt Git

- Chaque membre a au moins un commit à son prénom en S1 (Meryem, Yasmine, Zineb, Imane).
- `pytest` : 8 tests passent.

## Livrable montré en séance

Fiche de lecture (PDF), Gantt prévisionnel et exécution de `pytest` (8 tests verts).
