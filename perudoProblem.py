import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from IA_Players import QLPlayer, RandomPlayer
from perudoSimulation import run_qlearning, simulate_perudo

ql = run_qlearning()

# On check si les recommandations sont cohérentes
# Notre jeu : Deux 6
# L'adverse a 2 dés et a misé quatre 1
# En théorie, on devrait dire dudo
print("================================================")
print("On check si les recommandations sont cohérentes")
print("Notre jeu : Deux 6")
print("L'adverse a 2 dés et a misé quatre 1")
print("En théorie, on devrait dire dudo")
print("Avec l'algo de Q-Learning, on recommande cette action :")
reco = ql.columns[np.argmax(ql.loc['0 1 0 1 3 3 4', :])]
print(reco)

# Comparaison du Q-learning avec un jeu aléatoire
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

# Plot comparaison des policy
x = range(1, N+1)
y1 = df_random.groupby('simu').tail(1)['reward_of_simu'].cumsum()
y2 = df_ql_random.groupby('simu').tail(1)['reward_of_simu'].cumsum()
y3 = df_ql_ql.groupby('simu').tail(1)['reward_of_simu'].cumsum()
plt.plot(x, y1, label='Aléatoire vs Aléatoire')
plt.plot(x, y2, label='Q-Learning vs Aléatoire')
plt.plot(x, y3, label='Q-Learning vs Q-Learning')
plt.title('Comparaison des gains selon les politiques utilisées')
plt.xlabel('Nombre de parties jouées')
plt.ylabel('Nombre de parties gagnées - nombre de parties perdues')
plt.legend()
plt.grid(True)
plt.show()