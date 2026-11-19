# Gantt prévisionnel – Projet 2 : Jeux séquentiels (Groupe 2)

Version : prévisionnelle (déposée en S1), statuts mis à jour en S2 (19/11/2026). Légende des barres : gris = fait, bleu clair = en cours, bleu = à faire, rouge = jalon critique. La version « réalisée » sera ajoutée en S4 puis en S7, avec l'explication des écarts.

```mermaid
gantt
    title Projet 2 - Jeux séquentiels - Planning prévisionnel
    dateFormat YYYY-MM-DD
    axisFormat %d/%m
    todayMarker off

    section S1 Cadrage et théorie
    Dépôt GitHub et planning prévisionnel (Meryem)     :done, s1a, 2026-11-09, 7d
    Fiche de lecture (Meryem)                          :done, s1b, 2026-11-09, 7d
    Relecture backward_induction et src/jeux.py (Yasmine) :done, s1c, 2026-11-09, 7d
    Installation Ollama et test agent (Zineb)          :done, s1d, 2026-11-09, 7d
    Installation pytest et cas de test (Imane)         :done, s1e, 2026-11-09, 7d
    Point S1 et fiche de lecture (Meryem)              :done, milestone, m1, 2026-11-15, 0d

    section S2 Prototype Python
    Formules et hypothèses (Meryem)                    :done, s2a, 2026-11-16, 7d
    Fonctions induction, stackelberg, ultimatum (Yasmine) :done, s2b, 2026-11-16, 7d
    Squelette des outils et prototype chaîne (Zineb)   :done, s2c, 2026-11-16, 7d
    Vérification notebook des résultats du cours (Imane) :done, s2d, 2026-11-16, 7d
    Point S2 (Yasmine)                                 :milestone, m2, 2026-11-22, 0d

    section S3 Outils LangChain
    Mise à jour planning et théorie mille-pattes (Meryem) :s3a, 2026-11-23, 7d
    Mille-pattes à n étapes (Yasmine)                  :s3b, 2026-11-23, 7d
    Outils resoudre_arbre et stackelberg (Zineb)       :s3c, 2026-11-23, 7d
    Premiers tests pytest et invoke (Imane)            :s3d, 2026-11-23, 7d
    Point S3 (Zineb)                                   :milestone, m3, 2026-11-29, 0d

    section S4 Agent et mi-parcours
    Planning prévu contre réalisé (Meryem)             :s4a, 2026-11-30, 7d
    Finalisation des fonctions pures (Yasmine)         :s4b, 2026-11-30, 7d
    Agent avec faux modèle puis Ollama (Zineb)         :s4c, 2026-11-30, 7d
    Tests hors ligne et premières expériences (Imane)  :s4d, 2026-11-30, 7d
    Point S4 (Imane)                                   :milestone, m4, 2026-12-06, 0d
    ROTATION DES RÔLES                                 :crit, milestone, rot, 2026-12-06, 0d

    section S5 Expériences
    Script experiences et graphiques (Meryem Quant)    :s5a, 2026-12-07, 7d
    Chaîne ultimatum LLM (Yasmine Dév agent)           :s5b, 2026-12-07, 7d
    10 parties par configuration (Zineb Testeuse)      :s5c, 2026-12-07, 7d
    Début du rapport (Imane Chef de projet)            :s5d, 2026-12-07, 7d
    Point S5 (Meryem)                                  :milestone, m5, 2026-12-13, 0d

    section S6 Tests et rédaction
    Finalisation code et tableaux (Meryem)             :s6a, 2026-12-14, 7d
    Finalisation agent et README (Yasmine)             :s6b, 2026-12-14, 7d
    Tests et analyse des écarts à l EPS (Zineb)        :s6c, 2026-12-14, 7d
    Rapport à 80 pourcent avec planning (Imane)        :crit, s6d, 2026-12-14, 7d
    Point S6 et rapport 80 pourcent (Yasmine)          :milestone, m6, 2026-12-20, 0d

    section S7 Rapport final et bilan
    Relecture finale du code et du dépôt (Meryem)      :s7a, 2026-12-21, 7d
    Vérification du code zippé (Yasmine)               :s7b, 2026-12-21, 7d
    Relecture croisée et derniers tests (Zineb)        :s7c, 2026-12-21, 7d
    Rapport final et planning réalisé (Imane)          :crit, s7d, 2026-12-21, 7d
    Remise rapport et code zippé et bilan (Imane)      :milestone, m7, 2026-12-27, 0d
```

Source éditable : `docs/gantt_source.mmd` · Image : `docs/gantt_previsionnel.png`

## Tâches (responsable, début, fin, durée, statut)

| Sem. | Tâche | Responsable | Début | Fin | Durée | Statut |
|---|---|---|---|---|---|---|
| S1 | Dépôt GitHub et planning prévisionnel | Meryem | 09/11 | 15/11 | 7 j | fait |
| S1 | Fiche de lecture | Meryem | 09/11 | 15/11 | 7 j | fait |
| S1 | Relecture backward_induction et src/jeux.py | Yasmine | 09/11 | 15/11 | 7 j | fait |
| S1 | Installation Ollama et test agent | Zineb | 09/11 | 15/11 | 7 j | fait |
| S1 | Installation pytest et cas de test | Imane | 09/11 | 15/11 | 7 j | fait |
| S2 | Formules et hypothèses | Meryem | 16/11 | 22/11 | 7 j | fait |
| S2 | Fonctions induction, stackelberg, ultimatum | Yasmine | 16/11 | 22/11 | 7 j | fait |
| S2 | Squelette des outils et prototype chaîne | Zineb | 16/11 | 22/11 | 7 j | fait |
| S2 | Vérification notebook des résultats du cours | Imane | 16/11 | 22/11 | 7 j | fait |
| S3 | Mise à jour planning et théorie mille-pattes | Meryem | 23/11 | 29/11 | 7 j | à faire |
| S3 | Mille-pattes à n étapes | Yasmine | 23/11 | 29/11 | 7 j | à faire |
| S3 | Outils resoudre_arbre et stackelberg | Zineb | 23/11 | 29/11 | 7 j | à faire |
| S3 | Premiers tests pytest et invoke | Imane | 23/11 | 29/11 | 7 j | à faire |
| S4 | Planning prévu contre réalisé | Meryem | 30/11 | 06/12 | 7 j | à faire |
| S4 | Finalisation des fonctions pures | Yasmine | 30/11 | 06/12 | 7 j | à faire |
| S4 | Agent avec faux modèle puis Ollama | Zineb | 30/11 | 06/12 | 7 j | à faire |
| S4 | Tests hors ligne et premières expériences | Imane | 30/11 | 06/12 | 7 j | à faire |
| S5 | Script experiences et graphiques | Meryem Quant | 07/12 | 13/12 | 7 j | à faire |
| S5 | Chaîne ultimatum LLM | Yasmine Dév agent | 07/12 | 13/12 | 7 j | à faire |
| S5 | 10 parties par configuration | Zineb Testeuse | 07/12 | 13/12 | 7 j | à faire |
| S5 | Début du rapport | Imane Chef de projet | 07/12 | 13/12 | 7 j | à faire |
| S6 | Finalisation code et tableaux | Meryem | 14/12 | 20/12 | 7 j | à faire |
| S6 | Finalisation agent et README | Yasmine | 14/12 | 20/12 | 7 j | à faire |
| S6 | Tests et analyse des écarts à l EPS | Zineb | 14/12 | 20/12 | 7 j | à faire |
| S6 | Rapport à 80 pourcent avec planning | Imane | 14/12 | 20/12 | 7 j | à faire |
| S7 | Relecture finale du code et du dépôt | Meryem | 21/12 | 27/12 | 7 j | à faire |
| S7 | Vérification du code zippé | Yasmine | 21/12 | 27/12 | 7 j | à faire |
| S7 | Relecture croisée et derniers tests | Zineb | 21/12 | 27/12 | 7 j | à faire |
| S7 | Rapport final et planning réalisé | Imane | 21/12 | 27/12 | 7 j | à faire |

## Rôles et rotation

| Personne | S1 à S4 | S5 à S7 (après rotation) |
|---|---|---|
| Meryem | Chef de projet / Théorie | Quant / Python |
| Yasmine | Quant / Python | Développeur agent |
| Zineb | Développeur agent | Testeur / Expérimentateur |
| Imane | Testeur / Expérimentateur | Chef de projet / Théorie |

## Jalons

| Jalon | Semaine | Date prévue | Responsable | Statut |
|---|---|---|---|---|
| Dépôt GitHub + Gantt prévisionnel | S1 | 15/11 | Meryem | fait |
| Fiche de lecture | S1 | 15/11 | Meryem | fait |
| Point d'avancement S1 | S1 | 15/11 | Meryem | fait |
| Point d'avancement S2 | S2 | 22/11 | Yasmine | en cours |
| Point d'avancement S3 | S3 | 29/11 | Zineb | à faire |
| Point d'avancement S4 + rotation des rôles | S4 | 06/12 | Imane | à faire |
| Point d'avancement S5 | S5 | 13/12 | Meryem | à faire |
| Rapport à 80 % + point S6 | S6 | 20/12 | Imane / Yasmine | à faire |
| Remise rapport + code zippé + bilan S7 | S7 | 27/12 | Imane | à faire |

Légende des statuts : fait / en cours / retard / à faire.
