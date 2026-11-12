# Projet 2 – Jeux séquentiels : induction à rebours, Stackelberg, ultimatum et agents LLM

**Groupe 2** · Module Théorie des Jeux et Systèmes Multi-Agents (SMA) · IDIA3, ENSA Safi, 2026-2027

## Sujet

Étendre la fonction `backward_induction` du cours (information parfaite) pour gérer :

- les **égalités** (renvoyer tous les plans optimaux) ;
- les **sous-jeux simultanés** (équilibre de Nash, remplacé par ses gains) ;
- trois applications : **Stackelberg**, **ultimatum** et **mille-pattes** à n étapes.

Ensuite, des **agents LLM** (Ollama + LangChain) jouent ces jeux, et leurs choix sont comparés à l'équilibre parfait en sous-jeux (EPS).

## Équipe

| Membre  | Rôle (S1 à S4)            |
|---------|---------------------------|
| Meryem  | Chef de projet / Théorie  |
| Yasmine | Quant / Python            |
| Zineb   | Développeur agent         |
| Imane   | Testeur / Expérimentateur |

Les rôles permutent à la fin de la S4.

## Structure du dépôt

```
projet2-jeux-sequentiels/
├── README.md
├── requirements.txt       # dépendances Python
├── agent_tj_sma.py        # agent du cours étendu (outils @tool, chaîne LLM)
├── docs/                  # fiche de lecture, Gantt, points d'avancement, rapport
├── notebooks/             # notebooks de théorie, d'outils agent et d'expériences
├── src/                   # fonctions pures (jeux.py) et protocoles (experiences.py)
└── tests/                 # tests pytest
```

## Installation

1. Installer [Ollama](https://ollama.com), puis télécharger le modèle :

   ```bash
   ollama pull llama3.1
   ```

2. Cloner le dépôt et installer les dépendances :

   ```bash
   git clone https://github.com/merryfdill/projet2-jeux-sequentiels.git
   cd projet2-jeux-sequentiels
   pip install -r requirements.txt
   ```

## Lancer

| Action                        | Commande                  |
|-------------------------------|---------------------------|
| Tester l'agent et ses outils  | `python agent_tj_sma.py`  |
| Lancer les tests              | `pytest`                  |

L'agent a besoin qu'Ollama soit lancé. Les outils `@tool` peuvent se tester seuls avec `.invoke()`.

## Convention de commit

Format : `[Prénom] verbe + objet`

Chaque membre fait au moins un commit par semaine.