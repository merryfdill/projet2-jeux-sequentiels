# Fiche de lecture – Projet 2 : Jeux séquentiels

**Groupe 2** : Meryem (chef de projet / théorie), Yasmine, Zineb, Imane
**Module** : Théorie des Jeux et Systèmes Multi-Agents – IDIA3, ENSA Safi – 2026-2027

---

## 1. Formules clés

### 1.1 Induction à rebours (jeux à information parfaite)

On part des feuilles et on remonte vers la racine. À chaque nœud $n$ où joue le joueur $i(n)$ :

```math
V(n) =
\begin{cases}
u(n) & \text{si } n \text{ est une feuille (vecteur des gains)} \\
V(c^*) \text{ avec } c^* \in \arg\max_{c \in \text{enfants}(n)} V_{i(n)}(c) & \text{sinon}
\end{cases}
```

**Avec nos mots** : à chaque nœud, le joueur qui joue choisit le sous-arbre qui lui donne le plus grand gain, et le nœud prend le vecteur de gains de ce sous-arbre. La **stratégie** d'un joueur est un plan complet : une action à **chaque** nœud où il joue, y compris les nœuds qui ne sont pas atteints sur le chemin joué. Le résultat est l'**équilibre parfait en sous-jeux (EPS)**.

**Égalités** : si plusieurs enfants donnent le même gain maximal, le code du cours garde la première action. Notre version renvoie **tous** les plans optimaux.

**Sous-jeu simultané** : on le résout par un équilibre de Nash, puis on le remplace dans l'arbre par le vecteur de gains de cet équilibre.

### 1.2 Stackelberg (même demande que Cournot)

Demande inverse $P = a - bQ$ avec $Q = q_1 + q_2$, coût marginal constant $c$. Le meneur (firme 1) choisit $q_1$ en premier, le suiveur (firme 2) observe $q_1$ puis choisit $q_2$.

- Suiveur (on maximise $\pi_2$ à $q_1$ donné) :
```math
q_2(q_1) = \frac{a - c - b\,q_1}{2b}
```
- Meneur (il anticipe $q_2(q_1)$) :
```math
q_1^* = \frac{a - c}{2b}, \qquad q_2^* = \frac{a - c}{4b}
```
- Profits :
```math
\pi_1^* = \frac{(a-c)^2}{8b}, \qquad \pi_2^* = \frac{(a-c)^2}{16b}
```

**Avec nos mots** : le meneur produit plus et gagne plus que le suiveur. Son avantage vient de **l'engagement** : une fois $q_1$ choisi, le suiveur ne peut que s'y adapter.

**Valeurs de test** ($a = 100$, $b = 1$, $c = 10$) : $q_1 = 45$, $q_2 = 22{,}5$, $P = 32{,}5$, $\pi_1 = 1012{,}5$, $\pi_2 = 506{,}25$. Pour comparaison, Cournot donne $30$ par firme et un profit de $900$.

### 1.3 Jeu de l'ultimatum (partage de 10 unités)

Le proposant offre $`x \in \{0, 1, \dots, 10\}`$ au répondant :

```math
\text{gains} =
\begin{cases}
(10 - x,\ x) & \text{si le répondant accepte} \\
(0,\ 0) & \text{s'il refuse}
\end{cases}
```

**Sensibilité (cas discret)** : pour $x \geq 1$, le répondant accepte, car $x \gt 0$. Pour $x = 0$, il est **indifférent**.
- S'il accepte en cas d'indifférence, l'EPS est l'offre $x = 0$, avec les gains $(10, 0)$.
- S'il refuse en cas d'indifférence, l'EPS est l'offre $x = 1$, avec les gains $(9, 1)$.

La prédiction dépend donc de la règle choisie pour les égalités. C'est exactement le cas que `backward_induction_tous` doit gérer.

---

## 2. Lien avec le code du cours

| Code du cours | Ce que nous ajoutons |
|---|---|
| `backward_induction` (garde la 1re action en cas d'égalité) | `backward_induction_tous(noeud)` : tous les plans optimaux |
| Solveur de Nash (Groupe 1) | `sous_jeu_simultane(A, B)` : équilibre du sous-jeu, puis remplacement par ses gains |
| — | `stackelberg(a, b, c)` : formules fermées + vérification par induction à rebours sur une grille |
| — | `ultimatum(total=10)` : construit l'arbre JSON puis le résout |
| Outil `resoudre_arbre` | option `tous_les_plans` |
| — | nouvel outil `@tool stackelberg(a, b, c)` |
| Chaîne `prompt \| modèle \| parser` du TP6 (jeu d'entrée) | extension à l'ultimatum : proposant et répondant LLM, format « CHOIX : » |

**Conventions communes** : avec le Groupe 1, A = gains de J1 en lignes, B = gains de J2 en colonnes, indices à partir de 0. Avec le Groupe 6, on partage la chaîne `prompt | modèle | parser`.

---

## 3. Algorithme et hypothèses

### 3.1 Démarche de calcul en Python
1. Représenter le jeu par un arbre JSON : chaque nœud est soit une feuille (avec ses gains), soit un nœud de décision (avec le joueur et ses enfants), soit un sous-jeu simultané (avec les matrices A et B).
2. Parcourir l'arbre récursivement en profondeur, des feuilles vers la racine.
3. Pour une feuille, renvoyer ses gains.
4. Pour un sous-jeu simultané, calculer l'équilibre de Nash et renvoyer ses gains.
5. Pour un nœud de décision, calculer la valeur de chaque enfant, garder **tous** les enfants qui maximisent le gain du joueur, et enregistrer l'action à ce nœud.
6. Renvoyer les gains de l'EPS et le ou les plans complets (une action par nœud).

### 3.2 Hypothèses du modèle
- Jeu fini, **information parfaite** (chaque joueur voit les coups précédents), sauf dans les sous-jeux simultanés.
- **Rationalité commune** : chaque joueur maximise son gain et sait que les autres font de même.
- Stackelberg : demande linéaire, coût marginal constant, $a \gt c$, le meneur s'engage et le suiveur observe $q_1$.
- Ultimatum : offres entières entre 0 et 10, et une règle explicite pour l'indifférence.

### 3.3 Limites
- Les humains, et les LLM, s'écartent souvent de l'EPS. À l'ultimatum, les offres basses sont souvent refusées. Au mille-pattes, les joueurs continuent au lieu de s'arrêter.
- Un écart à l'EPS peut venir d'une erreur ou de préférences différentes (équité, réciprocité). Il faudra le discuter dans les expériences.

### 3.4 Résultats de référence pour les tests
- Jeu d'entrée : EPS = (Entrer, Accepter), gains $(2, 2)$.
- Mille-pattes à 3 étapes : Stop dès la 1re étape, gains $(1, 0)$. On vérifie que c'est toujours le cas à $n$ étapes.
- Sous-jeu de prix : (Bas, Bas), gains $(1, 1)$.
- Stackelberg : $q_1 = 45$, $q_2 = 22{,}5$.
