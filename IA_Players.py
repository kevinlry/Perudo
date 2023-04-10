import numpy as np
import json

class RandomPlayer:
    def __init__(self, args=None):
        pass

    def get_policy(self, game):

        alternatives = game.get_alternatives()

        return_policy = {'type': 'mise', 'n': None, 'de': None}
        
        alternatives.append("dudo")

        action = np.random.choice(alternatives, 1)[0]

        if (action == "dudo"):
            return_policy['type'] = "dudo"
        else:
            return_policy['n'] = action['n']
            return_policy['de'] = action['de']

        return return_policy
    
class QLPlayer:
    def __init__(self, args=None):
        self.qmatrix = args

    def get_policy(self, game):
        try :
            res = self.qmatrix.columns[np.argmax(self.qmatrix.loc[game.get_state(),:])]
            res = res.replace("\'", "\"").replace("None", "null")

            return json.loads(res)
        
        except:
            return RandomPlayer().get_policy(game)