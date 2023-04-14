# Perudo

## Contexte

Le Perudo est un jeu de harsard et de stratégie qui se joue à partir de 2 joueurs. Chaque joueur détient 6 dés au début de la partie. Le but est de finir la partie en étant le seul joueur à avoir conservé au moins 1 dé. Dans notre cas, nous utiliserons la version simplifiée du jeu suivante :

1. Il y a deux joueurs au début de la partie, chacun détient 3 dés à 4 faces ;
2. Les joueurs mélangent leurs dés ;
3. Le premier joueur réalise une mise sur le nombre de dés présents dans le jeu (exemple : 2 dés de valeur 3) ;
4. Chacun leur tour, les joueurs réalisent une des actions suivantes :
   - Augmenter le nombre de dés misés (passer de 2 - 3 à 3 - 3) ;
   - Augmenter la valeur du dé misé (passer de 2 - 3 à 2 - 4) ;
   - Dire "dudo", on compte alors le nombre de dés dans le jeu, si la mise annoncée est présente dans le jeu le joueur ayant dit "dudo" perd un dé, sinon le joueur ayant réalisé la mise perd un dé ;
3. Si les deux joueurs ont au moins 1 dé, on retourne à l'étape 2, sinon le joueur qui n'a plus aucun dé à perdu la partie.

Dans ce projet, nous implémenterons deux méthodes d'apprentissage par renforcement : Q-Learning et Monte-Carlo. Ces méthodes nous permettrons de choisir une action à réaliser selon l'état actuel du jeu en se basant sur un historique de parties. 

## Installation

Pour récuper le projet :
```
git clone https://github.com/kevinlry/Perudo.git
cd /Perudo
```

Pour lancer l'apprentissage par renforcement et visualiser les résultats :
```
py perudoProblem.py
```

_Note : Pour limiter le temps d'execution, les résultats de l'apprentissage par renforcement sont sauvegardés dans les fichiers "qmatrix" et "V_estimate". Ainsi, l'apprentissage n'est pas lancée à chaque execution, le script récupère ces fichiers s'ils existent. Si ces fichiers n'existent pas, le script lance de nouvelles simulations et relance l'apprentissage._

## Résultats

Pour vérifier la cohérence des recommandations effectuées par les deux méthodes de renforcement, on simule l'état de jeu suivant : nous avons 2 dés de valeur 6, le joueur adverse a 2 dés et a misé 4 dés de valeur 1. En théorie, on devrait dire "dudo" puisque notre main contient 2 dés de valeur 6, il n'est donc pas possible d'avoir 4 dés de valeur 1 dans le jeu.

Les deux politiques recommandent bien de dire "dudo" :
```
====================== Méthode MC =========================
Notre jeu : Deux 6
L'adverse a 2 dés et a misé quatre 1
Avec l'algo MC, on recommande cette action :
{'type': 'dudo', 'n': None, 'de': None}

=================== Méthode QLearning =====================
Notre jeu : Deux 6
L'adverse a 2 dés et a misé quatre 1
Avec l'algo de Q-Learning, on recommande cette action :
{'type': 'dudo', 'n': None, 'de': None}
```

Pour comparer les deux méthodes de renforcement, on simule maintenant 200 parties pendant lesquelles on fait jouer les différentes politiques (aléatoire, Q-Learning et Monte-Carlo) l'une contre l'autre. La métrique d'évaluation des performances utilisée est le nombre de parties gagnées - le nombre de parties perdues. On voit alors clairement que les deux méthodes par renforcement sont plus performantes qu'une méthode de jeu aléatoire. Cependant, la méthode Q-Learning est meilleure que la méthode Monte-Carlo.