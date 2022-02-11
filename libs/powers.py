import sqlite3


# --- Constructor --- #

class Power:
    def __init__(self, name, description, enemy, power_id):
        self.name = name
        self.description = description
        self.enemy = enemy
        self.power_id = power_id

    def export(self):
        return self.name, self.description, self.enemy, self.power_id


# --- Database gestion --- #

def get_species_id(species_name):
    table = sqlite3.connect("BDD/odyssee_powers.db")
    c = table.cursor()

    database = c.execute("SELECT * FROM especes").fetchall()
    table.close()

    species_name = species_name.lower()
    for index, species in enumerate(database):
        if species_name in species[1].split(" ; "):
            return species[0]

    return -1


def get_species(species_name):
    species_id = get_species_id(species_name)

    if species_id == -1:
        return -1, species_name.capitalize(), 1.0, 1.0, 1.0, 1.0

    table = sqlite3.connect("BDD/odyssee_powers.db")
    c = table.cursor()
    database = c.execute(f"SELECT * FROM especes WHERE especes.id = {species_id}").fetchall()
    table.close()

    return database[0]


def get_default_power(species_name):
    species_id = get_species_id(species_name)

    if species_id == -1:
        return None

    table = sqlite3.connect("BDD/odyssee_powers.db")
    c = table.cursor()

    database = c.execute(f"""
        SELECT pouvoirs.nom, description, adversaire, pouvoirs.id FROM pouvoirs
        JOIN especes ON especes.id = pouvoirs.espece
        WHERE especes.id = {species_id}
    """).fetchall()
    table.close()

    if database:
        return Power(*database[0])
    else:
        return None


def get_power_by_id(power_id):
    table = sqlite3.connect("BDD/odyssee_powers.db")
    c = table.cursor()

    database = c.execute(f"SELECT nom, description, adversaire, id FROM pouvoirs WHERE id = {power_id}").fetchall()
    table.close()

    if database:
        return Power(*database[0])
    else:
        return None


def get_power_by_name(power_name):
    table = sqlite3.connect("BDD/odyssee_powers.db")
    c = table.cursor()

    database = c.execute(f"SELECT nom, description, adversaire, id FROM pouvoirs WHERE nom = \"{power_name}\"").fetchall()
    table.close()
    
    if database:
        return Power(*database[0])
    else:
        return None


# --- Powers --- #

def power_use(power_id):
    return (
        nyctalopie,
        vol,
        effroi,
        guerison,
        chant,
        invocation,
        poison,
        regeneration,
        charme,
        boule_de_feu,
        corne_abondance,
        eclair,
        protection,
        fatigue,
        vitesse,
        pourfendre,
        charge,
        antidote,
        chant_de_guerre,
    )[power_id]


def nyctalopie(user, players, target=None):
    pts = 5 * user.get_level()
    user.stat[2] += pts    
    return f"__{user.name}__ a une vision améliorée."


def vol(user, players, target=None):
    if user.capacity_roll(2) >= 2:
        amount = target.stat[8]
        user.stat[8] += amount
        target.stat[8] = 0
        return f"__{user.name}__ vole {amount} Drachmes à __{target.name}__."
    else:
        return f"__{user.name}__ n'a pas réussi à voler __{target.name}__."


def effroi(user, players, target=None):
    pts = 10 * user.get_level()
    target.capacity_modify(3, -pts)
    return f"__{target.name}__ est effrayé(e)."


def guerison(user, players, target=None):
    msg = ""
    pts = user.get_level() * 10

    for player_id in players:
        player = players[player_id]
        if player.place == user.place and player.stat[6] < 100:
            player.stat[6] += pts
            msg += f" - __{player.name}__ a retrouvé {pts} points de Vie.\n"

    return msg


def chant(user, players, target=None):
    msg = ""
    pts = 5 * user.get_level()

    for player_id in players:
        player = players[player_id]
        if player.place == user.place:
            player.stat[2] += pts
            player.stat[3] += pts
            msg += f" - __{player.name}__ gagne en habileté et en rapidité.\n"
    return msg


def invocation(user, players, target=None):
    pts = 10 * user.get_level()
    for capacity_index in (1, 2):
        target.capacity_modify(capacity_index, -pts)

    return f"Le démon que vous avez invoqué provoque une terreur infinie chez __{target.name}__."


def poison(user, players, target=None):
    pts = 10 * user.get_level()
    if target.stat[6] > pts:
        target.state = 1
        target.capacity_modify(6, -pts)
        return f"__{target.name}__ perd {pts} points de Vie."
    else:
        target.state = 2
        target.stat[6] = 1
        return f"__{target.name}__ tombe au sol, incapable de bouger."


def regeneration(user, players, target=None):
    pts = 3 * user.get_level()
    for capacity_index in range(5):  # From Courage to Intelligence
        user.capacity_modify(capacity_index, pts)
    return f"__{user.name}__ se régénère."


def charme(user, players, target=None):
    pts = 3 * user.get_level()
    for capacity_index in range(4):
        target.capacity_modify(capacity_index, -pts)
    return f"__{target.name}__ tombe sous le charme de __{user.name}__"


def boule_de_feu(user, players, target=None):
    pts = 10 * user.get_level()
    if target.stat[6] > pts:
        for capacity_index in (0, 1, 6):
            target.capacity_modify(capacity_index, -pts)
        return f"__{target.name}__ est atteint par la boule de feu !"
    else:
        target.state = 2
        target.stat[6] = 1
        return f"__{target.name}__ s'effondre au sol."


def corne_abondance(user, players, target=None):
    pts = 5 * user.get_level()
    if user.stat[8] < 20 * user.get_level():
        user.capacity_modify(7, pts)
        return f"__{user.name}__ gagne {pts} Drachmes."
    else:
        return "La corne d'abondance est tarie…"


def eclair(user, players, target=None):
    pts = 5 * user.get_level()
    for capacity in (1, 4):
        target.capacity_modify(capacity, -pts)
    return f"__{target.name}__ s'est fait foudroyer."


def protection(user, players, target=None):
    pts = 10 * user.get_level()
    user.capacity_modify(4, pts)
    return f"__{user.name}__ gagne en défense."


def fatigue(user, players, target=None):
    pts = 15 * user.get_level()
    target.capacity_modify(3, -pts)
    target.state = 4
    return f"__{target.name}__ est pris d'un soudain besoin de sommeil."


def vitesse(user, players, target=None):
    pts = 15 * user.get_level()
    user.capacity_modify(3, pts)
    return f"__{user.name}__ devient plus rapide."


def charge(user, players, target=None):
    pts = user.stat[1] * 2
    user.stat[7] += 1

    if target.stat[6] > pts:
        target.capacity_modify(6, -pts)
        return f"__{user.name}__ se jette sur __{target.name}__."
    else:
        target.state = 2
        target.stat[6] = 1
        return f"__{target.name}__ tombe au sol."


def pourfendre(user, players, target=None):
    pts = int(user.stat[2] * 1.5)

    if target.stat[6] > pts:
        target.capacity_modify(6, -pts)
        return f"__{target.name}__ se fait transpercer."
    else:
        target.state = 2
        target.stat[6] = 1
        return f"Choqué par la douleur, __{target.name}__ s'évanouit"


def antidote(user, players, target=None):
    if target.state == 1:
        target.state = 0
        return f"__{target.name}__ n'est plus empoisonné."
    else:
        return f"__{target.name}__ n'était pas empoisonné."


def chant_de_guerre(user, players, target=None):
    msg = ""
    pts = user.get_level() * 5

    for player_id in players:
        player = players[player_id]
        if player.place == user.place:
            player.capacity_modify(0, pts)
            player.capacity_modify(1, pts)
            msg += f" - __{player.name}__ gagne en force et en courage.\n"
    return msg