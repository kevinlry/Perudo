import numpy as np
from IA_Players import RandomPlayer

class Perudo:
    def __init__(self, n_players, n_de_max=3, start_player=1):
        self.n_players = n_players
        self.n_de_max = n_de_max
        self.mains = None
        self.actual_player = start_player
        self.mise = {'player': 0, 'n': 0, 'de': 0}
        self.distribution_des([n_de_max for i in range(n_players)])

    def distribution_des(self, n_des):
        ''' 
        distribution_des
        Permet de redistribuer les dés de l'ensemble des joueurs

        Inputs: n_des - List[int] - Liste des nombre de dés des différents joueurs
        Return: None
        '''
        tmp_mains = []

        for n in n_des:
            assert n <= self.n_de_max
            tmp_mains.append(
                np.concatenate((np.random.randint(1, 7, size = n), 
                                np.zeros(self.n_de_max - n, dtype = int)), axis=0))
        
        self.mains = tmp_mains

    def set_mise(self, n, de):
        ''' 
        set_mise
        Définie la mise du joueur actuel

        Inputs: 
            n - int - Nombre de dés misé
            de - int - Valeur du dé misé
        Return: None
        '''
        self.mise = {'player': self.actual_player, 'n': n, 'de': de}

    def reset_mise(self):
        ''' 
        reset_mise
        Remet la mise à 0

        Inputs: None
        Return: None
        '''
        self.mise = {'player': 0, 'n': 0, 'de': 0}

    def next_player(self, actual_player):
        ''' 
        next_player
        Retourne le joueur suivant

        Inputs: actual_player - Int - Numéro du joueur actuel
        Return: int - Numéro du joueur suivant
        '''
        next_player = actual_player + 1 if actual_player != self.n_players else 1

        if sum(self.mains[next_player - 1]) == 0:
            next_player = self.next_player(next_player)
        
        return next_player

    def last_player(self, actual_player):
        ''' 
        last_player
        Retourne le joueur précédent

        Inputs: actual_player - Int - Numéro du joueur actuel
        Return: int - Numéro du joueur précédent
        '''
        last_player = actual_player - 1 if actual_player != 1 else self.n_players

        if sum(self.mains[last_player - 1]) == 0:
            last_player = self.last_player(last_player)
        
        return last_player

    def play(self, policy):
        ''' 
        play
        Permet de jouer une mise ou de dire "Dudo"

        Inputs: policy - Dict - Policy joué
        Return: n_player_perte_de - Numéro du joueur qui a perdu un dé le cas échéant
        '''
        n_player_perte_de = None

        if (policy['type'] == "mise"):
            self.set_mise(policy['n'], policy['de'])
            # Le joueur suivant joue
            self.actual_player = self.next_player(self.actual_player)
        
        else:
            count_des = self.count_des_in_game()

            if (count_des[self.mise['de'] - 1] >= self.mise['n']):
                n_player_perte_de = self.actual_player
                #print(f"Dudo perdu, le joueur {self.actual_player - 1} perd un dé, il y avait {count_des[self.mise['de'] - 1]} - {self.mise['de']}")
            else:
                n_player_perte_de = self.last_player(self.actual_player)
                #print(f"Dudo gagne, le joueur {n_player_perte_de} perd un dé, il y avait {count_des[self.mise['de'] - 1]} - {self.mise['de']}")
            
            # On retire un dé au joueur qui a perdu
            new_n_des = [self.n_de_max - sum(de == 0 for de in main) for main in self.mains]    
            new_n_des[n_player_perte_de - 1] -= 1

            # Le joueur qui a perdu joue
            self.actual_player = self.next_player(self.actual_player)
            
            self.reset_mise()
            self.distribution_des(new_n_des)

            return n_player_perte_de

    def get_alternatives(self):
        ''' 
        get_alternatives
        Retourne toutes les alternatives autorisées selon la mise du joueur précédent

        Inputs: None
        Return: List[Dict] - Liste des alternatives autorisées
        '''
        alternatives = []
        mise_actuelle = self.mise
        n_des_total = sum(self.count_des_in_game())

        # Si aucune mise actuelle
        if (mise_actuelle['de'] == 0):
            for i in range(1, 7):
                for j in range(1, n_des_total + 1):
                    alternatives.append({'n': j, 'de': i})

        else:
            # Augmentation du nombre de dé misés sans changement de valeur
            if (mise_actuelle['n'] + 1 <= n_des_total):
                for i in range(mise_actuelle['n'] + 1, n_des_total + 1):
                    alternatives.append({'n': i, 'de': mise_actuelle['de']})

            # Augmentation de la valeur sans changement du nombre de dés misés
            if (mise_actuelle['de'] < 6):
                for i in range(mise_actuelle['de'] + 1, 7):
                    alternatives.append({'n': mise_actuelle['n'], 'de': i})

            # Diminution de la valeur avec changement obligatoire du nombre de dés misés
            if ((mise_actuelle['de'] > 1) & (mise_actuelle['de'] < 6)):
                for i in range(1, mise_actuelle['de']):
                    for j in range(mise_actuelle['n'] + 1, n_des_total + 1):
                        alternatives.append({'n': j, 'de': i})

        return alternatives

    def count_des_in_game(self, player=None):
        count = np.zeros(6, dtype = int)

        if player:
            for de in self.mains[player - 1]:
                if (de != 0):
                    count[de - 1] += 1
        else:
            for main in self.mains:
                for de in main:
                    if (de != 0):
                        count[de - 1] += 1
        
        return count
    
    def check_game_end(self):
        winner = -1

        mains_non_vides = [index for index, main in enumerate(self.mains) if sum(main) != 0]

        if len(mains_non_vides) == 1:
            winner = mains_non_vides[0] + 1

        return winner

    def print_state_game(self, player=None):
        if player:
            print(f"================= PERUDO - VUE DU JOUEUR {player} =================")
            print(f"Vos dés : {[de for de in self.mains[player - 1] if de != 0]}")
        else:
            print("=================== PERUDO - VUE GLOBALE ===================")
            for i, main in enumerate(self.mains):
                print("Dé{} du joueur {} : {}".format('s' if len([de for de in main if de != 0]) > 1 else '', i + 1, [de for de in main if de != 0]))

        if self.mise['player'] > 0:
            print(f"Mise du joueur {self.mise['player']} : {self.mise['n']} - {self.mise['de']}")


if (False):
    n_players = 2
    start_player = np.random.randint(1, n_players + 1)

    pygame.init()
    fenetre = pygame.display.set_mode((640, 480))

    game = Perudo(n_players = n_players, start_player = start_player)
    game.print_state_game()

    while game.check_game_end() == -1:
        game.print_state_game(player = game.actual_player)

        alternatives = game.get_alternatives()

        policy = RandomPlayer().get_policy(alternatives)

        game.play(policy)

    print(game.check_game_end())