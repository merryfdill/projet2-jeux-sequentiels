# Gantt prévisionnel – Projet 2 : Jeux séquentiels (Groupe 2)

Version : prévisionnelle (déposée en S1). La version « réalisée » sera ajoutée en S4 puis en S7, avec l'explication des écarts.

```mermaid
gantt
    title Projet 2 - Jeux séquentiels - Planning prévisionnel
    dateFormat YYYY-MM-DD
    axisFormat %d/%m

    section S1 Cadrage et théorie
    Dépôt GitHub et planning prévisionnel (Meryem)     :done, s1a, 2026-11-09, 7d
    Fiche de lecture (Meryem)                          :active, s1b, 2026-11-09, 7d
    Relecture backward_induction et src/jeux.py (Yasmine) :s1c, 2026-11-09, 7d
    Installation Ollama et test agent (Zineb)          :s1d, 2026-11-09, 7d
    Installation pytest et cas de test (Imane)         :s1e, 2026-11-09, 7d
    Point S1 et fiche de lecture (Meryem)              :milestone, m1, 2026-11-15, 0d

    section S2 Prototype Python
    Formules et hypothèses (Meryem)                    :s2a, 2026-11-16, 7d
    Fonctions induction, stackelberg, ultimatum (Yasmine) :s2b, 2026-11-16, 7d
    Squelette des outils et prototype chaîne (Zineb)   :s2c, 2026-11-16, 7d
    Vérification notebook des résultats du cours (Imane) :s2d, 2026-11-16, 7d
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
