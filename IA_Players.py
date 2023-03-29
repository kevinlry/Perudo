import numpy as np

class RandomPlayer:
    def __init__(self):
        pass

    def get_policy(self, alternatives):
        
        alternatives.append("dudo")

        return np.random.choice(alternatives, 1)[0]
    
