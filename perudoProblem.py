import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from IA_Players import MCPlayer, QLPlayer, RandomPlayer
from perudoSimulation import run_montecarlo, run_qlearning, simulate_perudo


# Lancement de l'apprentissage de la méthode Monte-Carlo
mc = run_montecarlo()

# =================================================================
# On check si les recommandations de cette méthode sont cohérentes
#
# Notre jeu : 2 dés de valeur 4
# L'adverse a également 2 dés et a misé 4 dés de valeur 1
# En théorie, on devrait dire dudo puisqu'on a 2 dés de valeur 4
# donc impossible qu'il y ait 4 dés de valeur 1 dans le jeu
print("======================= Méthode MC =========================")
print("On check si les recommandations sont cohérentes")
print("Notre jeu : Deux 6")
print("L'adverse a 2 dés et a misé quatre 1")
print("En théorie, on devrait dire dudo")
print("Avec l'algo MC, on recommande cette action :")
reco = mc.loc[mc['state'] == '0 0 0 2 2 4 1', 'best_action']
print(reco)
#
# Notre jeu : 1 dés de valeur 1
# L'adverse a également 1 dé et a misé 1 dé de valeur 4
# En théorie, on plus de chance en disant dudo
print("======================= Méthode MC =========================")
print("On check si les recommandations sont cohérentes")
print("Notre jeu : Un 1")
print("L'adverse a 1 dé et a misé un 4")
print("Avec l'algo MC, on recommande cette action :")
reco = mc.loc[mc['state'] == '1 0 0 0 1 1 4', 'best_action']
print(reco)


# Lancement de l'apprentissage de la méthode Q-Learning
ql = run_qlearning()

# =================================================================
# On check si les recommandations de cette méthode sont cohérentes
#
# Notre jeu : 2 dés de valeur 4
# L'adverse a également 2 dés et a misé 4 dés de valeur 1
# En théorie, on devrait dire dudo puisqu'on a 2 dés de valeur 4
# donc impossible qu'il y ait 4 dés de valeur 1 dans le jeu
print("======================= Méthode QLearning =========================")
print("On check si les recommandations sont cohérentes")
print("Notre jeu : Deux 6")
print("L'adverse a 2 dés et a misé quatre 1")
print("En théorie, on devrait dire dudo")
print("Avec l'algo de Q-Learning, on recommande cette action :")
reco = ql.columns[np.argmax(ql.loc['0 0 0 2 2 4 1', :])]
print(reco)
#
# Notre jeu : 1 dés de valeur 1
# L'adverse a également 1 dé et a misé 1 dé de valeur 4
# En théorie, on plus de chance en disant dudo
print("======================= Méthode QLearning =========================")
print("On check si les recommandations sont cohérentes")
print("Notre jeu : Un 4")
print("L'adverse a 1 dé et a misé un 4")
print("Avec l'algo de Q-Learning, on recommande cette action :")
reco = ql.columns[np.argmax(ql.loc['1 0 0 0 1 1 4', :])]
print(reco)

# =================================================================
# Comparaison des diférentes policy
# =================================================================
gameSimulations = []
N = 200

# Jeu Aléatoire vs Aléatoire
for i in range(0, N):
    o = pd.DataFrame.from_dict(simulate_perudo(RandomPlayer, RandomPlayer, n_de_max=3, n_valeur_max=4))
    o['simu'] = i
    o['reward_of_simu'] = o['reward'].iloc[-1]

    gameSimulations.append(o)

df_random = pd.concat(gameSimulations)

# Jeu Q-learning vs Aléatoire
for i in range(0, N):
    o = pd.DataFrame.from_dict(simulate_perudo(QLPlayer, RandomPlayer, params_policy_agent=ql, n_de_max=3, n_valeur_max=4))
    o['simu'] = i
    o['reward_of_simu'] = o['reward'].iloc[-1]

    gameSimulations.append(o)

df_ql_random = pd.concat(gameSimulations)

# Jeu Q-learning vs Q-learning
for i in range(0, N):
    o = pd.DataFrame.from_dict(simulate_perudo(QLPlayer, QLPlayer, params_policy_agent=ql, params_policy_robot=ql, n_de_max=3, n_valeur_max=4))
    o['simu'] = i
    o['reward_of_simu'] = o['reward'].iloc[-1]

    gameSimulations.append(o)

df_ql_ql = pd.concat(gameSimulations)

# Jeu MC vs Aléatoire
for i in range(0, N):
    o = pd.DataFrame.from_dict(simulate_perudo(MCPlayer, RandomPlayer, params_policy_agent=mc, n_de_max=3, n_valeur_max=4))
    o['simu'] = i
    o['reward_of_simu'] = o['reward'].iloc[-1]

    gameSimulations.append(o)

df_mc_random = pd.concat(gameSimulations)

# Jeu MC vs Q-Learning
for i in range(0, N):
    o = pd.DataFrame.from_dict(simulate_perudo(MCPlayer, QLPlayer, params_policy_agent=mc, params_policy_robot=ql, n_de_max=3, n_valeur_max=4))
    o['simu'] = i
    o['reward_of_simu'] = o['reward'].iloc[-1]

    gameSimulations.append(o)

df_mc_ql = pd.concat(gameSimulations)

# Plot comparaison des policy
x = range(1, N+1)
y1 = df_random.groupby('simu').tail(1)['reward_of_simu'].cumsum()
y2 = df_ql_random.groupby('simu').tail(1)['reward_of_simu'].cumsum()
y3 = df_ql_ql.groupby('simu').tail(1)['reward_of_simu'].cumsum()
y4 = df_mc_random.groupby('simu').tail(1)['reward_of_simu'].cumsum()
y5 = df_mc_ql.groupby('simu').tail(1)['reward_of_simu'].cumsum()
plt.plot(x, y1, label='Aléatoire vs Aléatoire')
plt.plot(x, y2, label='Q-Learning vs Aléatoire')
plt.plot(x, y3, label='Q-Learning vs Q-Learning')
plt.plot(x, y4, label='MC vs Aléatoire')
plt.plot(x, y5, label='MC vs Q-Learning')
plt.title('Comparaison des gains selon les politiques utilisées')
plt.xlabel('Nombre de parties jouées')
plt.ylabel('Nombre de parties gagnées - nombre de parties perdues')
plt.legend()
plt.grid(True)
plt.show()