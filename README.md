# Projet 2 – Jeux séquentiels : induction à rebours, Stackelberg, ultimatum et agents LLM

**Groupe 2** · Module Théorie des Jeux et Systèmes Multi-Agents (SMA) · IDIA3, ENSA Safi, 2026-2027

## Sujet

Étendre la fonction `backward_induction` du cours (information parfaite) pour gérer :

- les **égalités** (renvoyer tous les plans optimaux) ;
- les **sous-jeux simultanés** (équilibre de Nash, remplacé par ses gains) ;
- trois applications : **Stackelberg**, **ultimatum** et **mille-pattes** à n étapes.

Ensuite, des **agents LLM** (Ollama + LangChain) jouent ces jeux, et leurs choix sont comparés à l'équilibre parfait en sous-jeux (EPS).

## Équipe

| Membre  | Rôle (S1 à S4)           |
| ------- | -------------------------- |
| Meryem  | Chef de projet / Théorie  |
| Yasmine | Quant / Python             |
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

| Action                       | Commande                   |
| ---------------------------- | -------------------------- |
| Tester l'agent et ses outils | `python agent_tj_sma.py` |
| Lancer les tests             | `pytest`                 |

L'agent a besoin qu'Ollama soit lancé. Les outils `@tool` peuvent se tester seuls avec `.invoke()`


## Tests et validation

Le projet utilise **pytest** pour vérifier le comportement des fonctions développées dans `src/jeux.py`.

### Exécution des tests

Depuis la racine du dépôt, activer l'environnement virtuel puis exécuter :

```bash
python -m pytest -v
```

### Organisation des tests

Les tests automatisés sont regroupés dans le dossier `tests/` :

- **`test_jeux.py`** : tests de la fonction `backward_induction`, couvrant notamment :

  - le jeu d'entrée ;
  - la maximisation des gains des joueurs ;
  - les égalités entre plusieurs actions ;
  - les décisions situées hors du chemin joué ;
  - les feuilles terminales ;
  - les gains négatifs et décimaux ;
  - la tolérance numérique pour les égalités.
- **`test_jeux_s2.py`** : tests complémentaires des fonctionnalités S2 :

  - conservation de tous les plans optimaux ;
  - résolution du modèle de Stackelberg ;
  - résolution du jeu de l'ultimatum ;
  - détection des équilibres de Nash dans les sous-jeux simultanés.

### Vérifications expérimentales

Le notebook `notebooks/experiences_s2.ipynb` regroupe des expériences complémentaires permettant de confronter les résultats des fonctions aux résultats théoriques.

Les expériences portent sur le jeu d'entrée, Stackelberg, l'ultimatum, la conservation des plans optimaux et la résolution des sous-jeux simultanés.

Le jeu du mille-pattes sera vérifié après l'implémentation de sa fonction en S3.

## Convention de commit

Format : `[Prénom] verbe + objet`

Chaque membre fait au moins un commit par semaine.
