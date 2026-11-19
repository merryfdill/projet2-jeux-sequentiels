# Théorie S2 – Formules expliquées, hypothèses et sensibilité de l'ultimatum

**Groupe 2 – Projet 2 : Jeux séquentiels** · Rédigé par : Meryem (chef de projet / théorie) · Semaine 2

Ce document explique les formules utilisées dans `src/jeux.py` et les relie aux résultats obtenus par le code (commit S2 de Yasmine).

---

## 1. Induction à rebours

### 1.1 Formule

```math
V(n) =
\begin{cases}
u(n) & \text{si } n \text{ est une feuille} \\
V(c^*) \text{ avec } c^* \in \arg\max_{c \in \text{enfants}(n)} V_{i(n)}(c) & \text{sinon}
\end{cases}
```

### 1.2 Explication

- $u(n)$ est le **vecteur des gains** d'une feuille, par exemple $(2, 2)$.
- $i(n)$ est le joueur qui décide au nœud $n$.
- On part des feuilles et on remonte vers la racine : à chaque nœud, le joueur qui joue garde l'enfant qui lui rapporte le plus, et le nœud « hérite » du vecteur de gains de cet enfant.
- Le résultat est un **plan complet** : une action à **chaque** nœud de décision, y compris les nœuds qui ne sont pas atteints. C'est ce plan qui définit l'**équilibre parfait en sous-jeux (EPS)**. Le **chemin joué** n'est qu'une partie du plan.

### 1.3 Égalités

Quand plusieurs enfants donnent le même gain maximal (à `TOL` près) :
- `backward_induction` (version du cours) garde **la première** action ;
- `backward_induction_tous` garde **toutes** les actions optimales et renvoie **tous** les plans, avec un plafond `max_plans` contre l'explosion combinatoire ;
- le paramètre `prefere` permet d'imposer une règle de départage (par exemple `["Accepter"]`).

### 1.4 Sous-jeux simultanés

Un nœud `{"sous_jeu": {"A": ..., "B": ...}}` est un jeu où les deux joueurs choisissent **en même temps**. On ne peut pas le résoudre par induction à rebours, donc :
1. `sous_jeu_simultane(A, B)` élimine d'abord les stratégies strictement dominées, puis cherche les équilibres de Nash par énumération des supports ;
2. le nœud est **remplacé** par le vecteur de gains de l'équilibre trouvé ;
3. l'induction à rebours continue au-dessus.

Conventions validées avec le Groupe 1 : A = gains de J1 (lignes), B = gains de J2 (colonnes), indices à partir de 0.

**Vérification par le code** : sous-jeu de prix → équilibre pur (Bas, Bas), gains $(1, 1)$.

---

## 2. Stackelberg

### 2.1 Modèle

Demande inverse $P = a - bQ$ avec $Q = q_1 + q_2$, coût marginal constant $c$. Le meneur (firme 1) choisit $q_1$, puis le suiveur (firme 2) observe $q_1$ et choisit $q_2$. Profit de la firme $i$ :

```math
\pi_i = (P - c)\,q_i = \big(a - b(q_1 + q_2) - c\big)\,q_i
```

### 2.2 Étape 1 : le suiveur (on résout la fin du jeu en premier)

Le suiveur maximise $\pi_2$ en prenant $q_1$ comme donné. Condition du premier ordre :

```math
\frac{\partial \pi_2}{\partial q_2} = a - c - b\,q_1 - 2b\,q_2 = 0
\quad\Longrightarrow\quad
q_2(q_1) = \frac{a - c - b\,q_1}{2b}
```

C'est la **fonction de meilleure réponse** du suiveur : plus le meneur produit, moins le suiveur produit.

### 2.3 Étape 2 : le meneur (il anticipe la réaction du suiveur)

On remplace $q_2$ par $q_2(q_1)$ dans le profit du meneur :

```math
\pi_1(q_1) = \big(a - c - b\,q_1 - b\,q_2(q_1)\big)\,q_1 = \frac{(a - c - b\,q_1)\,q_1}{2}
```

Condition du premier ordre :

```math
\frac{d\pi_1}{dq_1} = \frac{a - c - 2b\,q_1}{2} = 0
\quad\Longrightarrow\quad
q_1^* = \frac{a - c}{2b}, \qquad q_2^* = q_2(q_1^*) = \frac{a - c}{4b}
```

### 2.4 Prix et profits

```math
P^* = a - b\,(q_1^* + q_2^*) = \frac{a + 3c}{4},
\qquad
\pi_1^* = \frac{(a-c)^2}{8b},
\qquad
\pi_2^* = \frac{(a-c)^2}{16b}
```

**Interprétation** : le meneur produit deux fois plus que le suiveur et gagne deux fois plus. Son avantage vient de **l'engagement** : une fois $q_1$ choisi, il ne peut plus être modifié, et le suiveur n'a plus qu'à s'adapter. Par comparaison, Cournot (choix simultanés) donne $q = (a-c)/(3b)$ par firme.

### 2.5 Application numérique et vérification par le code

Avec $a = 100$, $b = 1$, $c = 10$ :

| Grandeur | Formule | Valeur | `stackelberg(100, 1, 10)` |
|---|---|---|---|
| $q_1^*$ | $(a-c)/(2b)$ | 45 | 45.0 ✅ |
| $q_2^*$ | $(a-c)/(4b)$ | 22,5 | 22.5 ✅ |
| $P^*$ | $(a+3c)/4$ | 32,5 | 32.5 ✅ |
| $\pi_1^*$ | $(a-c)^2/(8b)$ | 1012,5 | 1012.5 ✅ |
| $\pi_2^*$ | $(a-c)^2/(16b)$ | 506,25 | 506.25 ✅ |
| Cournot | $(a-c)/(3b)$ par firme | 30 (profit 900) | — |

**Vérification par induction à rebours sur grille** : le code construit un arbre discret (`stackelberg_arbre`) où le meneur choisit $q_1$ sur une grille de pas 5 et le suiveur $q_2$ sur une grille de pas 2,5, puis le résout avec `backward_induction`. Il retrouve $q_1 = 45$ et $q_2 = 22{,}5$ (`coincide: True`).

Pourquoi deux pas différents (pas du meneur = 2 × pas du suiveur) ? La meilleure réponse $q_2(q_1)$ tombe alors toujours exactement sur la grille du suiveur. Avec deux grilles identiques, le suiveur devrait arrondir sa meilleure réponse, ce qui crée des égalités artificielles dont le meneur profiterait : le résultat sur grille s'écarterait des formules.

---

## 3. Ultimatum

### 3.1 Modèle

Le proposant (J1) offre $`x \in \{0, 1, \dots, 10\}`$ au répondant (J2), qui accepte ou refuse :

```math
\text{gains} =
\begin{cases}
(10 - x,\ x) & \text{si J2 accepte} \\
(0,\ 0) & \text{si J2 refuse}
\end{cases}
```

### 3.2 Induction à rebours

1. **Répondant** (fin du jeu) : accepter rapporte $x$, refuser rapporte $0$.
   - Pour $x \geq 1$ : $x \gt 0$, donc il **accepte**.
   - Pour $x = 0$ : $0 = 0$, il est **indifférent**.
2. **Proposant** : il anticipe la réaction du répondant et choisit l'offre qui lui laisse le plus.

---

## 4. Hypothèses

| Hypothèse | Rôle dans le modèle | Ce qui change si elle tombe |
|---|---|---|
| Jeu fini à **information parfaite** (hors sous-jeux simultanés) | Chaque joueur voit les coups précédents : l'induction à rebours est possible | Il faut des croyances (information imparfaite, projet 3) |
| **Rationalité commune** | Chaque joueur maximise son gain et sait que les autres le font | Les joueurs peuvent s'écarter de l'EPS (cas des LLM et des humains) |
| Gains = **seul objectif** | Le répondant ne compare que $x$ et $0$ | Avec un souci d'équité, il peut refuser les offres basses |
| Règle explicite pour les **égalités** | Le résultat est unique une fois la règle fixée | Sans règle, plusieurs EPS coexistent (voir partie 5) |
| Sous-jeu simultané **non dégénéré** | `sous_jeu_simultane` trouve tous les équilibres | Des équilibres peuvent manquer |
| Stackelberg : demande linéaire, coût constant, $a \gt c$, $b \gt 0$ | Formules fermées valides | Le code lève une erreur si $a \leq c$ ou $b \leq 0$ |
| Stackelberg : **engagement** du meneur, $q_1$ observé | Le jeu est bien séquentiel | Sans observation de $q_1$, on retombe sur Cournot |
| Ultimatum : offres **entières** de 0 à 10 | Le jeu est discret et fini | En continu, la sensibilité disparaît (partie 5.3) |

---

## 5. Sensibilité de l'ultimatum discret

### 5.1 Deux EPS selon la règle d'indifférence

Le seul nœud où le répondant est indifférent est $x = 0$. Le résultat dépend donc de ce qu'il fait à ce nœud :

| Règle à $x = 0$ | Meilleure offre du proposant | Gains EPS | Code |
|---|---|---|---|
| Le répondant **accepte** | $x = 0$ (il garde 10) | $(10, 0)$ | `ultimatum(10, accepte_indifference=True)` → offre 0 ✅ |
| Le répondant **refuse** | $x = 1$ (offrir 0 rapporterait 0) | $(9, 1)$ | `ultimatum(10, accepte_indifference=False)` → offre 1 ✅ |
| Aucune règle imposée | les deux | $(10, 0)$ et $(9, 1)$ | `backward_induction_tous` → **2 plans** ✅ |

Dans les deux cas, le plan du répondant contient une action pour **chacune** des 11 offres : il accepte toute offre $x \geq 1$, même celles qui ne sont jamais faites.

### 5.2 Ce que montre la sensibilité

- La prédiction théorique n'est pas « le proposant offre 0 », mais « le proposant offre **le minimum que le répondant accepte** ».
- Une seule égalité, à un seul nœud, suffit à changer l'issue. C'est pourquoi le code du cours (qui garde la première action) ne suffit pas : selon l'ordre des actions dans l'arbre, il donnerait l'un ou l'autre résultat, sans le signaler.

### 5.3 Effet de la taille de l'unité

Si la plus petite offre possible vaut $\varepsilon$ (1 unité ici), les deux EPS donnent au répondant $0$ ou $\varepsilon$. Plus l'unité est petite, plus les deux EPS se rapprochent : en continu, il ne reste qu'une seule prédiction, le proposant garde (presque) tout. La sensibilité est donc un **effet de la discrétisation**, et elle est maximale quand l'unité est grande par rapport au total.

### 5.4 Lien avec les expériences (S5)

- Les humains, et sans doute les LLM, s'écartent nettement de l'EPS : ils proposent souvent des partages proches de l'égalité, et les offres basses sont souvent refusées.
- Un refus de $x = 1$ n'est pas prévu par l'EPS (car $1 \gt 0$). Si on l'observe, ce n'est pas une affaire d'égalité : c'est soit une erreur du LLM, soit un objectif différent (équité, réciprocité). C'est la question à discuter dans les expériences.
