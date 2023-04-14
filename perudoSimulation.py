import numpy as np
import pandas as pd

from IA_Players import MCPlayer, RandomPlayer
from perudoGame import Perudo

def simulate_perudo(agentPolicy, robotPolicy, params_policy_agent=None, params_policy_robot=None, n_de_max=5, n_valeur_max=6):
    ''' 
    simulate_perudo
    Simulation d'une partie de Perudo

    Inputs: 
        agentPolicy - Object - Politique que va jouer l'agent
        robotPolicy - Object - Politique que va jouer le robot
        params_policy_agent - Object - Paramètre a donner à la politique de l'agent (Exemple : QMatrix)
        params_policy_robot - Object - Paramètre a donner à la politique du robot (Exemple : QMatrix)
        n_de_max - Int - Nombre de dés dans la main de chaque joueur au début de la partie
        n_valeur_max - Int - Valeur maximale des dés (Par être réaliste : 4 ou 6)
    Return: Dict - Historique des tours pendant la partie (états, actions et rewards)
    '''
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
    ''' 
    run_qlearning
    Lance un apprentissage par la méthode Q-Learning

    Inputs: None
    Return: DataFrame - Q-Matrix
    '''
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


def run_montecarlo():
    ''' 
    run_montecarlo
    Lance un apprentissage par la méthode Monte-Carlo

    Inputs: None
    Return: DataFrame - V_estimate
    '''
    try:
        running_V_estimate = pd.read_pickle('V_estimate')

    except:
        iter = 0
        while (iter < 20):
            
            iter = iter + 1
            print('Step\t', iter)
            
            # run a few simulations
            gameSimulations = list()
            N = 5000
            for i in range(0, N):
                if (iter == 1):
                    o = pd.DataFrame.from_dict(simulate_perudo(RandomPlayer, RandomPlayer, n_de_max=3, n_valeur_max=4))
                else:
                    o = pd.DataFrame.from_dict(simulate_perudo(MCPlayer, RandomPlayer, params_policy_agent=running_V_estimate, n_de_max=3, n_valeur_max=4))

                o['simu'] = i
                o['reward_of_simu'] = o['reward'].iloc[-1]

                gameSimulations.append(o)

            gameSimulations = pd.concat(gameSimulations)
            
            # estimate V(s) by averaging returns
            running_V_estimate = gameSimulations \
                .assign(action = lambda DF: DF.action.astype(str)) \
                .groupby(['state', 'action']) \
                .agg({'reward_of_simu': 'mean'})
            
            idx = running_V_estimate \
                .groupby(['state'])['reward_of_simu'] \
                .transform(max) == running_V_estimate['reward_of_simu']

            running_V_estimate = running_V_estimate[idx]

            running_V_estimate.reset_index(inplace=True)
            
            running_V_estimate.rename(columns={"action": "best_action"}, inplace=True)

            running_V_estimate = running_V_estimate.groupby('state').first()

            running_V_estimate.reset_index(inplace=True)

        running_V_estimate.to_pickle('V_estimate')
        
    return running_V_estimate