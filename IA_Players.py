import numpy as np
import json

class RandomPlayer:
    ''' 
    RandomPlayer
    
    Permet de jouer une politique aléatoire parmi les alternatives possibles
    '''
    def __init__(self, args=None):
        pass

    def get_policy(self, game):

        alternatives = game.get_alternatives()

        return_policy = {'type': 'mise', 'n': None, 'de': None}
        
        #Si il y a déjà une mise, on peut dire dudo
        if (game.get_state()[-3:] != "0 0"):
            alternatives.append("dudo")

        action = np.random.choice(alternatives, 1)[0]

        if (action == "dudo"):
            return_policy['type'] = "dudo"
        else:
            return_policy['n'] = action['n']
            return_policy['de'] = action['de']

        return return_policy
    

class QLPlayer:
    ''' 
    QLPlayer
    
    Permet de jouer la politique recommandée par la méthode Q-Learning parmi les alternatives possibles
    '''
    def __init__(self, args=None):
        self.qmatrix = args

    def get_policy(self, game):
        try :
            res = self.qmatrix.columns[np.argmax(self.qmatrix.loc[game.get_state(),:])]
            res = res.replace("\'", "\"").replace("None", "null")

            return json.loads(res)
        
        except:
            return RandomPlayer().get_policy(game)
        

class MCPlayer:
    ''' 
    MCPlayer
    
    Permet de jouer la politique recommandée par la méthode de Monte-Carlo parmi les alternatives possibles
    '''
    def __init__(self, args=None):
        self.running_V_estimate = args

    def get_policy(self, game):
        eps = 0.1
        if (np.random.uniform(low=0, high=1, size=1) < eps):
            return RandomPlayer().get_policy(game)
        else:
            a = self.running_V_estimate[self.running_V_estimate['state'] == game.get_state()].loc[:, 'best_action']

            if (len(a) == 0):
                return RandomPlayer().get_policy(game)
            else:
                res = a.to_list()[0].replace("\'", "\"").replace("None", "null")

                return json.loads(res)