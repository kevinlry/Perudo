import numpy as np
import pandas as pd
from IA_Players import RandomPlayer
from perudoGame import Perudo

def simulate_perudo(agentPolicy, robotPolicy):

    gameHistory = {'state': [], 
                   'action': [], 
                   'reward': [], 
                   'nextState': []}

    n_players = 2
    start_player = np.random.randint(1, n_players + 1)

    game = Perudo(n_players = n_players, start_player = start_player)

    i = -1
    while game.check_game_end() == -1:
        alternatives = game.get_alternatives()

        # Jeu de l'agent
        if game.actual_player == 1:
            gameHistory['state'].append(None)
            gameHistory['action'].append(None)
            gameHistory['reward'].append(None)
            gameHistory['nextState'].append(None)

            i = i + 1

            policy = agentPolicy().get_policy(alternatives)
            
            # only collect information here
            gameHistory['state'][i] = ' '.join(str(x) for x in game.count_des_in_game(player = 1)) + ' ' + str(sum(game.count_des_in_game(player = 2))) + ' ' + str(game.mise['n']) + ' ' + str(game.mise['de'])

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
            policy = robotPolicy().get_policy(alternatives)

            # play the policy
            de_perdu = game.play(policy)

            if (i > -1):
                gameHistory['nextState'][i] = ' '.join(str(x) for x in game.count_des_in_game(player = 1)) + ' ' + str(sum(game.count_des_in_game(player = 2))) + ' ' + str(game.mise['n']) + ' ' + str(game.mise['de'])

            if (de_perdu == 1):
                gameHistory['reward'][i] = -1

    ls = len(gameHistory['state']) 
    lns = len(gameHistory['nextState']) 

    assert lns == ls

    gameHistory['nextState'][ls - 1] = gameHistory['state'][ls - 1]
    
    return(gameHistory)

def run_qlearning(df):
    stateEnums = set(df['state'] + df['nextState'])
    actionEnums = set(df['action'])

    myvec = [-20 for i in range(len(stateEnums) * len(actionEnums))]
    qmatrix = pd.DataFrame(myvec.reshape(len(stateEnums), len(actionEnums)))

    notConverged = True
    qGamma = 0.9
    qAlpha = 0.8
    eps = 0.0

    while(notConverged):
        oldQmatrix = qmatrix
        for index in range(1, len(df.index)):
            index_s = stateEnums == df['state'][index]
            index_sp = stateEnums == df['nextState'][index]
            index_a = actionEnums == df['action'][index]
            oldValue = qmatrix[index_s, index_a]

            if (np.random.uniform(low=0, high=1, size=1) < eps):
                newValue = df['reward'][index] + qGamma * np.random.choice(qmatrix[index_sp,])[0]     
            else:
                newValue = df['reward'][index] + qGamma * qmatrix[index_sp, our_which_max_(qmatrix[index_sp,])]
            
            qmatrix[index_s, index_a] = oldValue + qAlpha * (newValue - oldValue)

        maxDiffQmatrix = max(abs(qmatrix - oldQmatrix))
        print(maxDiffQmatrix)
        notConverged = (maxDiffQmatrix > 1e-3)

    return({'stateEnums': stateEnums, 'actionEnums': actionEnums, 'qsa': qmatrix})

def our_which_max_(x, return_all = False):
    ind = np.where(x == max(x))
    if (len(ind) == 1 | return_all):
        return(ind)
    else:
        return(np.random.choice(ind)[0])

#print(pd.DataFrame.from_dict(simulate_perudo(RandomPlayer, RandomPlayer)))