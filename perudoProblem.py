import pandas as pd

from IA_Players import RandomPlayer
from perudoSimulation import simulate_perudo, run_qlearning

# run bunch of simulations
gameSimulations = []
N = 500

for i in range(1, N):
    o = pd.DataFrame.from_dict(simulate_perudo(RandomPlayer, RandomPlayer))
    o['simu'] = i
    o['reward_of_simu'] = o['reward'].iloc[-1]
    
    gameSimulations.append(o)

gameSimulations = pd.concat(gameSimulations)
print(gameSimulations)

# run qlearning
ql = run_qlearning(df = gameSimulations)

#print(ql)