# Gantt prévisionnel – Projet 2 : Jeux séquentiels (Groupe 2)

Version : prévisionnelle (déposée en S1). La version « réalisée » sera ajoutée en S4 puis en S7, avec l'explication des écarts.

```mermaid
gantt
    title Projet 2 - Jeux séquentiels - Gantt prévisionnel
    dateFormat YYYY-MM-DD
    axisFormat %d/%m

    section S1 Cadrage et théorie
    Dépôt GitHub et Gantt prévisionnel (Meryem)        :done, s1a, 2026-11-09, 7d
    Fiche de lecture (Meryem)                          :active, s1b, 2026-11-09, 7d
    Relecture backward_induction et src/jeux.py (Yasmine) :s1c, 2026-11-09, 7d
    Installation Ollama et test agent (Zineb)          :s1d, 2026-11-09, 7d
    Installation pytest et cas de test (Imane)         :s1e, 2026-11-09, 7d
    Point S1 et fiche de lecture (Meryem)              :milestone, m1, 2026-11-15, 0d

    section S2 Prototype Python
    Formules et hypothèses (Meryem)                    :s2a, 2026-11-16, 7d
    backward_induction_tous, stackelberg, ultimatum, sous_jeu_simultane (Yasmine) :s2b, 2026-11-16, 7d
    Squelette des outils et prototype chaîne (Zineb)   :s2c, 2026-11-16, 7d
    Vérification notebook des résultats du cours (Imane) :s2d, 2026-11-16, 7d
    Point S2 (Yasmine)                                 :milestone, m2, 2026-11-22, 0d

    section S3 Outils LangChain
    Mise à jour Gantt et théorie mille-pattes (Meryem) :s3a, 2026-11-23, 7d
    Mille-pattes à n étapes (Yasmine)                  :s3b, 2026-11-23, 7d
    Outils resoudre_arbre et stackelberg (Zineb)       :s3c, 2026-11-23, 7d
    Premiers tests pytest et invoke (Imane)            :s3d, 2026-11-23, 7d
    Point S3 (Zineb)                                   :milestone, m3, 2026-11-29, 0d

    section S4 Agent et mi-parcours
    Gantt prévu vs réalisé (Meryem)                    :s4a, 2026-11-30, 7d
    Finalisation des fonctions pures (Yasmine)         :s4b, 2026-11-30, 7d
    Agent avec faux modèle puis Ollama (Zineb)         :s4c, 2026-11-30, 7d
    Tests hors ligne et premières expériences (Imane)  :s4d, 2026-11-30, 7d
    Point S4 (Imane)                                   :milestone, m4, 2026-12-06, 0d
    ROTATION DES RÔLES                                 :crit, milestone, rot, 2026-12-06, 0d

    section S5 Expériences
    experiences.py et graphiques (Meryem - Quant)      :s5a, 2026-12-07, 7d
    Chaîne ultimatum LLM (Yasmine - Dév agent)         :s5b, 2026-12-07, 7d
    10 parties par configuration (Zineb - Testeuse)    :s5c, 2026-12-07, 7d
    Début du rapport (Imane - Chef de projet)          :s5d, 2026-12-07, 7d
    Point S5 (Meryem)                                  :milestone, m5, 2026-12-13, 0d

    section S6 Tests et rédaction
    Finalisation code et tableaux (Meryem)             :s6a, 2026-12-14, 7d
    Finalisation agent et README (Yasmine)             :s6b, 2026-12-14, 7d
    Tests et analyse des écarts à l'EPS (Zineb)        :s6c, 2026-12-14, 7d
    Rapport à 80 pourcent avec Gantt (Imane)           :crit, s6d, 2026-12-14, 7d
    Point S6 et rapport 80 pourcent (Yasmine)          :milestone, m6, 2026-12-20, 0d

    section S7 Rapport final et bilan
    Relecture finale du code et du dépôt (Meryem)      :s7a, 2026-12-21, 7d
    Vérification du code zippé (Yasmine)               :s7b, 2026-12-21, 7d
    Relecture croisée et derniers tests (Zineb)        :s7c, 2026-12-21, 7d
    Rapport final et Gantt réalisé (Imane)             :crit, s7d, 2026-12-21, 7d
    Remise rapport et code zippé - bilan (Imane)       :milestone, m7, 2026-12-27, 0d
```

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
| Dépôt GitHub + Gantt prévisionnel | S1 | 15/11 | Meryem | en cours |
| Fiche de lecture | S1 | 15/11 | Meryem | en cours |
| Point d'avancement S1 | S1 | 15/11 | Meryem | à faire |
| Point d'avancement S2 | S2 | 22/11 | Yasmine | à faire |
| Point d'avancement S3 | S3 | 29/11 | Zineb | à faire |
| Point d'avancement S4 + rotation des rôles | S4 | 06/12 | Imane | à faire |
| Point d'avancement S5 | S5 | 13/12 | Meryem | à faire |
| Rapport à 80 % + point S6 | S6 | 20/12 | Imane / Yasmine | à faire |
| Remise rapport + code zippé + bilan S7 | S7 | 27/12 | Imane | à faire |

Légende des statuts : fait / en cours / retard / à faire.
