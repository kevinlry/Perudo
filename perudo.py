import numpy as np

class Perudo:
    def __init__(self, n_players=2, n_de_max=3):
        self.n_players = n_players
        self.n_de_max = n_de_max
        self.mains = None
        self.actual_player = np.random.randint(1, n_players + 1)
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

    def next_player(self):
        ''' 
        next_player
        Retourne le joueur suivant

        Inputs: None
        Return: int - Numéro du joueur suivant
        '''
        return self.actual_player + 1 if self.actual_player != self.n_players else 1

    def play(self, type, n=None, de=None):
        if (type == "mise"):
            self.set_mise(n, de)
        
        elif (type == "dudo"):
            count_des = self.count_des_in_game()
            if (count_des[self.mise['de']] >= self.mise['n']):
                print(f"Dudo perdu, il y avait {count_des}")
                #new_n_des = [self.n_de_max - sum(de == 0 for de in main) for main in self.mains]
                #new_n_des[self.actual_player] -= 1

            else:
                print(f"Dudo gagne, il y avait {count_des}")
            
            #self.distribution_des(new_n_des)
        
        self.actual_player = self.next_player()

    def count_des_in_game(self):
        count = np.zeros(6, dtype = int)

        for main in self.mains:
            for de in main:
                count[de - 1] += 1
        
        return count

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

game = Perudo()
game.print_state_game()
game.play("mise", 1, 5)
game.print_state_game(player = 2)
game.play(type = "dudo")