import numpy as np

class RandomPlayer:
    def __init__(self):
        pass

    def get_policy(self, alternatives):

        return_policy = {'type': 'mise', 'n': None, 'de': None}
        
        alternatives.append("dudo")

        action = np.random.choice(alternatives, 1)[0]

        if (action == "dudo"):
            return_policy['type'] = "dudo"
        else:
            return_policy['n'] = action['n']
            return_policy['de'] = action['de']

        return return_policy
    
