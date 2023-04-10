import numpy as np
import pandas as pd
from IA_Players import RandomPlayer
from perudoGame import Perudo

def simulate_perudo(agentPolicy, robotPolicy, params_policy_agent=None, params_policy_robot=None, n_de_max=5, n_valeur_max=6):

    gameHistory = {'state': [], 
                   'action': [], 
                   'reward': [], 
                   'nextState': []}

    n_players = 2
    start_player = np.random.randint(1, n_players + 1)

    game = Perudo(n_players = n_players, n_de_max = n_de_max, n_valeur_max = n_valeur_max, start_player = start_player)

    i = -1
    while game.check_game_end() == -1:
        # Jeu de l'agent
        if game.actual_player == 1:
            gameHistory['state'].append(None)
            gameHistory['action'].append(None)
            gameHistory['reward'].append(None)
            gameHistory['nextState'].append(None)

            i = i + 1

            policy = agentPolicy(params_policy_agent).get_policy(game)
            
            # only collect information here
            gameHistory['state'][i] = game.get_state()

            gameHistory['action'][i] = policy
            gameHistory['reward'][i] = 0

            # play the policy
            de_perdu = game.play(policy)

            if (de_perdu == 2):
                gameHistory['reward'][i] = +1
            else:
                gameHistory['reward'][i] = 0
        
        # Jeu du robot
        else:
            policy = robotPolicy(params_policy_robot).get_policy(game)

            # play the policy
            de_perdu = game.play(policy)

            if (i > -1):
                gameHistory['nextState'][i] = game.get_state()

            if (de_perdu == 1):
                gameHistory['reward'][i] = -1

    ls = len(gameHistory['state']) 
    lns = len(gameHistory['nextState']) 

    assert lns == ls

    gameHistory['nextState'][ls - 1] = gameHistory['state'][ls - 1]
    
    return(gameHistory)

def run_qlearning():
    try:
        qmatrix = pd.read_pickle('qmatrix')
    except:
        # run bunch of simulations
        gameSimulations = []
        N = 7000

        for i in range(1, N):
            o = pd.DataFrame.from_dict(simulate_perudo(RandomPlayer, RandomPlayer, n_de_max=3, n_valeur_max=4))
            o['simu'] = i
            o['reward_of_simu'] = o['reward'].iloc[-1]
            
            gameSimulations.append(o)

        df = pd.concat(gameSimulations)

        stateEnums = np.array(list(set(df['state'].to_list() + df['nextState'].to_list())))
        actionEnums = np.array(list(set([str(i) for i in df['action']])))

        myvec = np.array([-20 for i in range(len(stateEnums) * len(actionEnums))])
        qmatrix = pd.DataFrame(myvec.reshape(len(stateEnums), len(actionEnums)))

        notConverged = True
        qGamma = 0.9
        qAlpha = 0.8
        eps = 0.0

        while (notConverged):
            oldQmatrix = qmatrix.copy()

            for index in range(0, len(df.index)):
                index_s = np.where(stateEnums == df['state'].iloc[index])[0][0]
                index_sp = np.where(stateEnums == df['nextState'].iloc[index])[0][0]
                index_a = np.where(actionEnums == str(df['action'].iloc[index]))[0][0]

                oldValue = qmatrix.at[index_s, index_a]

                if (np.random.uniform(low=0, high=1, size=1) < eps):
                    newValue = df['reward'].iloc[index] + qGamma * np.random.choice(qmatrix.iloc[index_sp,:])[0]     
                else:
                    newValue = df['reward'].iloc[index] + qGamma * qmatrix.iloc[index_sp, np.argmax(qmatrix.iloc[index_sp,:])]
                
                qmatrix.iloc[index_s, index_a] = float(oldValue) + qAlpha * (float(newValue) - float(oldValue))

            maxDiffQmatrix = abs(qmatrix - oldQmatrix).max().max()        
            print(maxDiffQmatrix)
            notConverged = (maxDiffQmatrix > 1e-2)

        qmatrix.columns = actionEnums
        qmatrix.index = stateEnums

        qmatrix.to_pickle('qmatrix')

    return qmatrix