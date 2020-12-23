# --- Species --- #

def data_species():
    return [
        ["Elfe", "Elfe sylvestre", "Druide"],
        ["Humain", "Mage", "Magicienne", "Magicien", "Cavalière", "Cavalier"],
        ["Troll", "Orque", "Ogre", "Cyclope"],
        ["Naine", "Nain"],
        ["Gnome", "Gobelin"],
        ["Nazgul", "Cavalière noire", "Cavalier noir"],
        ["Succube", "Incube"],
        ["Vampire"],
        ["Hobbit"],
        ["Satyre"],
        ["Nymphe"],
        ["Guivre"],
        ["Centaure"],
        ["Dragon", "Dragonne"],
        ["Minotaure"],
        ["Efrit", "Démon"],
        ["Follasse"],
        ["Dieu", "Déesse"]]


# --- Special powers --- #

def data_power_by_species():
    return {
        0: [0, 3, 7],      # Elfe
        1: [3, 6],         # Humain
        2: [2, 7],         # Troll
        3: [3, 4],         # Nain 
        4: [1, 3, 5],      # Gnome
        5: [1, 2, 6],      # Nazgul
        6: [3, 4, 8],      # Succube
        7: [0, 2, 7],      # Vampire 
        8: [4],            # Hobbit
        9: [1, 4],         # Satyre
        10: [4, 7, 8],     # Nymphe
        11: [6],           # Guivre
        12: [0, 4, 8],     # Centaure
        13: [2, 9],        # Dragon
        14: [2, 6],        # Minotaure
        15: [3, 5, 6],     # Démon
        16: [0, 3],        # Follasse
        17: [3, 10, 11],   # Dieu
        }


def data_powers():
    return {
        0: ["Nyctalopie",
                "augmente votre Habilité et votre Rapidité.",
                False],
        
        1: ["Vol",
                "vous permet de voler votre adversaire sans le tuer.",
                True],
        
        2: ["Effroi",
                "fait chuter la Rapidité de votre adversaire.",
                True],
        
        3: ["Guérison",
                "soigne tous les joueurs à votre proximité, vous compris.",
                False],

        4: ["Chant",
                "augmente le Courage et la Force des joueurs qui écoutent.",
                False],

        5: ["Invocation",
                "fait chuter la Force et l'Habileté de votre adversaire.",
                True],

        6: ["Poison",
                "empoisonne votre adversaire.",
                True],

        7: ["Régénération",
                "fait monter toutes vos capacités.",
                False],

        8: ["Charme",
                "fait chuter toutes les capacités de votre adversaire.",
                True],

        9: ["Boule de feu",
                "fait brûler votre adversaire.",
                True],

        10: ["Corne d'abondance",
                "créer des Drachmes.",
                False],

        11: ["Éclair",
                "foudroye votre adversaire.",
                True],

        12: ["Protection",
                "augmente votre capacité à vous défendre.",
                False],

        13: ["Fatigue",
                "ralentit votre adversaire.",
                True]}


def data_power_index(power_name):
    powers = data_powers()
    for i in powers:
        if powers[i][0] == power_name: return i


class SpecialPower:

    def __init__(self, power_name, user, others, target):
        self.others = others
        self.user = user
        self.target = target

        self.index = data_power_index(power_name)

    def launch(self):
        msg = ""

        if self.index == 0: msg = self.__nyctalopie()
        elif self.index == 1: msg = self.__vol()
        elif self.index == 2: msg = self.__effroi()
        elif self.index == 3: msg = self.__guerison()
        elif self.index == 4: msg = self.__chant()
        elif self.index == 5: msg = self.__invocation()
        elif self.index == 6: msg = self.__poison()
        elif self.index == 7: msg = self.__regenération()
        elif self.index == 8: msg = self.__charme()
        elif self.index == 9: msg = self.__boule_de_feu()      
        elif self.index == 10: msg = self.__corne_abondance()
        elif self.index == 11: msg = self.__eclair()
        elif self.index == 12: msg = self.__protection()
        elif self.index == 13: msg = self.__fatigue()

        return msg
            

    def __nyctalopie(self):
        pts = 5 * user.get_level()
        self.user.stat[2] += pts
        self.user.stat[3] += pts
        return f"{self.user.name} devient plus habile et rapide."

    def __vol (self):
        if self.user.capacity_roll(2):
            amount = self.target.stat[7]
            self.user.stat[7] += amount
            self.target.stat[7] = 0
            return f"{self.user.name} vole {amount} Drachmes à {self.target.name}."
        else:
            return f"{self.user.name} n'a pas réussi à voler {self.target.name}."

    def _effroi(self):
        pts = 10 * user.get_level()
        self.target.capacity_modify(3, -pts)
        return f"{self.target.name} perd {pts} points de Courage."

    def __guerison(self):
        msg = ""

        for player_id in self.others:
            if player_id < 0: next

            player = self.others[player_id]
            if player.place == self.user.place and player.stat[5] < 100:
                player.stat[5] = 100
                msg += f" - {player.name} a retrouvé 100 points de Vie.\n"
        return msg

    def __chant(self):
        msg = ""
        pts = 5 * self.user.get_level()

        for player_id in self.others:
            if player_id < 0: next

            player = self.others[player_id]
            if player.place == self.user.place:
                player.stat[0] += pts
                player.stat[1] += pts
                msg += f" - {player.name} gagne {pts} points de Courage et de Force.\n"
        return msg

    def __invocation(self):
        pts = 5 * self.user.get_level()
        for capacity_index in (1, 2):
            self.target.capacity_modify(capacity_index, -pts)
        return f"{self.target.name} perd {pts} points de Force et d'Habileté."

    def __poison(self):
        pts = 10 * self.user.get_level()
        if self.target.stat[5] > pts:
            self.target.capacity_modify(5, -pts)
            return f"{self.target.name} perd {pts} points de Vie."
        else:
            return f"{self.target.name} est immunisé."

    def __regeneration(self):
        pts = 3 * self.user.get_level()
        for capacity_index in range(4):  # From Courage to Rapidity
            self.user.capacity_modify(capacity_index, pts)
        return f"{self.user.name} se régénère."

    def __charme(self):
        pts = 3 * self.user.get_level()
        for capacity_index in range(4):
            self.target.capacity_modify(capacity_index, -pts)
        return f"{self.target.name} tombe sous le charme de {self.user.name}"

    def __boule_de_feu(self):
        pts = 10 * self.user.get_level()
        if self.target.stat[5] > pts:
            for capacity_index in (0, 1, 5):
                self.target.capacity_modify(capacity_index, -pts)
            return f"{self.target.name} est atteint par la boule de feu !"
        else:
            return f"{self.target.name} parvient à échapper à la boule de feu."

    def __corne_abondance(self):
        pts = 10 * self.user.get_level()
        if self.user.stat[7] < 20 * self.user.get_level():
            self.user.capacity_modify(7, pts)
            return f"{self.user.name} gagne {pts} Drachmes."
        else:
            return "Le sort a échoué, la Corne d'abondance ne donne qu'aux nécessiteux…"

    def __eclair(self):
        pts = 5 * self.user.get_level()
        for capacity in (1, 4):
            self.target.capacity_modify(capacity, -pts)
        return f"{self.target.name} s'est fait foudroyer."

    def __protection(self):
        pts = 10 * self.user.get_level()
        user.capacity_modify(4, pts)
        return f"{self.user.name} gagne en défense."

    def __fatigue(self):
        pts = 15 * user.get_level()
        target.capacity_modify(3, -pts)
        return f"{target.name} perd en rapidité."
       
