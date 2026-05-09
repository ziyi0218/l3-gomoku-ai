# Gomoku AI

Projet realise dans le cadre de l'UE Intelligence Artificielle, Licence 3
Mathematiques et Informatique, Universite Paris Cite.

**Auteurs :** LI Wenxiao, REN Ziyi  
**Responsable de l'UE :** Elise Bonzon  
**Annee universitaire :** 2025-2026

## Description

Ce projet implemente le jeu de Gomoku et plusieurs intelligences artificielles
capables d'y jouer. Le Gomoku est un jeu deterministe a information parfaite :
deux joueurs placent des pions a tour de role sur un plateau, et le premier qui
aligne cinq pions gagne.

Le projet utilise une version simplifiee des regles :

- plateau `15 x 15` ;
- `X` represente le joueur 1, `O` represente le joueur -1 ;
- une ligne de cinq pions ou plus gagne ;
- les regles professionnelles comme le double-trois ne sont pas prises en compte.

## Lancer le jeu

Installer les dependances :

```bash
python -m pip install -r requirements.txt
```

Lancer le menu principal :

```bash
python main.py
```

Le menu propose :

1. `PvP` : deux joueurs humains sur le meme terminal ;
2. `Human vs AI` : un joueur humain contre une IA ;
3. `Quit`.

En mode `Human vs AI`, les difficultes disponibles sont celles validees par
l'Experience 4 :

|Difficulte|Configuration|Evaluation|Profondeur|Recherche|
|---|---|---|---|---|
|Easy|A1|Eval A|1|Alpha-Beta|
|Medium|A3|Eval A|3|Alpha-Beta + ordering|
|Hard|B2|Eval B|2|Alpha-Beta + ordering|

Un mode `Custom` permet aussi de choisir manuellement l'evaluation, la profondeur
et le rayon de generation des coups candidats. La recherche y est fixee a
`Alpha-Beta + ordering`.

## Structure du projet

```text
.
|-- main.py
|-- models.py
|-- requirements.txt
|-- Report.pdf
|-- ai/
|   |-- alphabeta.py
|   |-- evaluation.py
|   |-- minmax.py
|   `-- player.py
|-- cli/
|   |-- input.py
|   |-- menu.py
|   `-- output.py
|-- game/
|   |-- board.py
|   |-- rules.py
|   `-- utils.py
|-- modes/
|   |-- human_vs_ai.py
|   `-- pvp.py
`-- experiments/
    |-- experiment1_search/
    |-- experiment2_evaluations/
    |-- experiment3_candidate_tournament/
    `-- experiment4_difficulty_tournament/
```

## Dossiers principaux

- `ai/` : algorithmes de recherche et fonctions d'evaluation.
- `game/` : moteur de jeu, plateau, regles et detection de victoire.
- `cli/` : menus, entrees utilisateur et affichage terminal.
- `modes/` : modes de jeu jouables depuis `main.py`.
- `experiments/` : scripts, resultats CSV, graphiques et rapports experimentaux.

## Intelligence artificielle

Le projet contient :

- `Minimax` ;
- `Alpha-Beta pruning` ;
- `Alpha-Beta + move ordering` ;
- trois fonctions d'evaluation :
  - Eval A : alignements consecutifs / defense simple ;
  - Eval B : formes ouvertes et bloquees ;
  - Eval C : potentiel des fenetres de cinq cases.

Les coups candidats sont generes autour des pierres deja placees afin de reduire
le facteur de branchement.

## Experiences

Les experiences sont organisees dans `experiments/` :

- `experiment1_search/` : efficacite de l'elagage Alpha-Beta ;
- `experiment2_evaluations/` : comparaison des fonctions d'evaluation ;
- `experiment3_candidate_tournament/` : selection des configurations candidates ;
- `experiment4_difficulty_tournament/` : validation finale Easy / Medium / Hard.

Chaque dossier contient ses scripts, ses resultats et son rapport.
