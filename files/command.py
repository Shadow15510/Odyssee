from files.player import *

# --------------------------------------------------
# Get informations from the message
# --------------------------------------------------

# --- Command and argument --- #

def int_converter(data):
    try:
        return int(data)
    except:
        return data

def analyse(message, SEP):
    def get_arg(arguments, SEP):
        args = [i.strip() for i in arguments.split(SEP)]
        return [int_converter(i) for i in args]

    arguments = message.content.split(" ", 1)

    if len(arguments) == 1: return None
    else: return get_arg(arguments[1], SEP)

# --- Author's information --- #

def get_user(message):
    if message.author.nick:
        return message.author.nick, int(message.author.id)
    else:
        return message.author.name, int(message.author.id)

class Command:
    def __init__(self, players, kick, server_id, PREFIX, SEP):
        self.players = players
        self.kick = kick
        self.server_id = server_id
        self.PREFIX = PREFIX
        self.SEP = SEP

    def set_server_id(self, message):
        self.server_id = message.channel.guild.id
        self.save()

# --- Information about the targeted player --- #

    def nick_to_id(self, player_nick):
        for player_id in self.players:
            if self.players[player_id].name == player_nick: return player_id
        return False

    def id_to_nick(self, player_id):
        if player_id in self.players:
            return self.players[player_id].name
        return False

    def id_to_object(self, player_id):
        if player_id in self.players:
            return self.players[player_id]
        else:
            return False

# --------------------------------------------------
# Commands
# --------------------------------------------------

# --- Settings --- #

    def color_change(self, message):
        user = self.id_to_object(get_user(message)[1])
        if not user:
            return "*Erreur : {get_user(message)[0]} n'est pas un joueur enregistré.*"
        color_name = analyse(message, self.SEP)
        color_available = data_color()

        if color_name:
            color_name = color_name[0]
            if color_name.startswith("0x"): color_name = int(color_name, 16)
        else:
            return self.color_list()

        if type(color_name) == str and color_name in color_available.keys():
            color_id = color_available[color_name]
        elif type(color_name) == int:
            color_id = color_name
        else:
            return self.color_list()
    
        
        user.stat[8] = color_id
        
        return f"La couleur de __{user.name}__ et devenue {color_name}"
    
    def color_list(self):
        return f"Entrez le code hexadécimal `{self.PREFIX}couleur 0xRRVVBB`, ou le nom de la couleur souhaitée.\n**Liste des couleurs disponibles**\n - " + "\n - ".join(data_color())
    
    def species_change(self, message):
        user = self.id_to_object(get_user(message)[1])
        if not user:
            return self.species_list()
        
        new_species = analyse(message, self.SEP)
        
        if not new_species:
            return self.species_list()

        new_species = new_species[0].capitalize()
        
        user.species = new_species
        return f"__{user.name}__ devient un(e) {new_species}"

    def species_list(self):
        species_category = data_species()
        msg = f"Pour changer d'espèce, la syntaxe est : `{self.PREFIX}espèce < nom_de_la_nouvelle_espèce >`\n**Liste des espèces gérées**"
        for species in species_category:
            msg += "\n - " + ", ".join(species)
            
        return msg

    def player_list(self, message):
        if get_user(message)[1] not in self.players:
            return f"*Erreur : {get_user(message)[0]} n'existe pas.*", -1
        return [[self.players[player_id].name, self.players[player_id].species, self.players[player_id].place, self.players[player_id].get_level()] for player_id in self.players], self.players[get_user(message)[1]].stat[8]

    def player_new(self, message):
        user = get_user(message)
        species = analyse(message, self.SEP)

        if user[1] in self.kick:
            return f"*Erreur : {user[0]} a été kické.*"
        
        if species:
            species = species[0].capitalize()
        else:
            return f"*Erreur : syntaxe invalide : `{self.PREFIX}nouveau < nom_de_l'espèce >`.*"
        
        if not user[1] in self.players:
            self.players.update({user[1] : Player(user[1], user[0], species)})
            return f"{user[0]}, un(e) {species}, est apparu(e)."
        else:
            return f"*Erreur : {user[0]} est déjà enregistré(e).*"

    def change_pseudo(self, message):
        user = self.id_to_object(get_user(message)[1])
        if not user:
            return f"*Erreur : {get_user(message)[0]} n'est pas un joueur enregistré.*"

        pseudo = analyse(message, self.SEP)[0]
        if pseudo:
            user.name, pseudo = pseudo, user.name
            return f"Le pseudo de {pseudo} est devenu {user.name}."
        else:
            return f"*Erreur : syntaxe invalide : `{self.PREFIX}pseudo < nouveau_pseudo >`.*"

    def modify_note(self, message):
        user = self.id_to_object(get_user(message)[1])
        if not user:
            return f"*Erreur : {get_user(message)[0]} n'est pas un joueur enregistré.*"

        args = analyse(message, self.SEP)

        if len(args) > 1:
            if args[-1] == "+":
                content = f"{self.SEP} ".join(args[:-1])
                user.add_note(content)
                return f"__{user.name}__ a ajouté la note :\n> {content}"
            elif args[1] == "-":
                content = user.del_note(args[0])
                if content:
                    return f"__{user.name}__ a supprimé la note :\n> {content}"
                else:
                    return f"*Erreur : la note n°{note_index} n'existe pas.*"
            else:
                return f"*Erreur : syntaxe invalide : `{self.PREFIX}note < contenu > {self.SEP} < + | - >`.*"
        else:
            return f"*Erreur : syntaxe invalide : `{self.PREFIX}note < contenu > {self.SEP} < + | - >`.*"

# --- Game --- #

    def fight(self, message):
        user = self.id_to_object(get_user(message)[1])
        if not user:
            return f"*Erreur : {get_user(message)[0]} n'existe pas.*"

        elif not analyse(message, self.SEP):
            return f"*Erreur : syntaxe invalide `{self.PREFIX}combat < nom_de_l'ennemi >`.*"
        
        return self.fight_new(user, message)
        
    def fight_new(self, user, message):
        enemy_id = -len(self.players)
        enemy_name = analyse(message, self.SEP)[0]
        
        if self.nick_to_id(enemy_name):
            return self.fight_continue(user, enemy_name)
        elif self.nick_to_id(enemy_name.capitalize()):
            return self.fight_continue(user, enemy_name.capitalize())
        
        enemy_name = enemy_name.capitalize()
        self.players.update({enemy_id : Player(enemy_id, enemy_name, "Ennemi", stat_gen(user.get_level(), user.stat[8], True), user.place)})

        return f"__{user.name}__ se prépare pour combattre {enemy_name}.\nEntrez `{self.PREFIX}combat {enemy_name}` pour attaquer."

    def fight_continue(self, user, enemy_name):
        enemy = self.id_to_object(self.nick_to_id(enemy_name))

        if not enemy:
            return f"*Erreur : {enemy_name} n'existe pas.*"

        if user.place != enemy.place:
            return f"*Erreur : {user.name} et {enemy.name} ne sont pas au même endroit.*"

        def phase_1(player, target):
            pt_player, pt_target = 0, 0
            
            while pt_player == pt_target:
                pt_player = player.stat[0] + player.stat[3] + roll_die()
                pt_target = target.stat[0] + target.stat[3] + roll_die()
            return pt_player > pt_target

        def phase_2(player):
            return player.capacity_roll(2)

        def phase_3(player, target):
            pt_damage = player.stat[1] + roll_die(10, player.get_level())
            if target.stat[4] >= pt_damage:
                return 0
            elif target.stat[5] < pt_damage:
                return -1
            return pt_damage

        def comment_on_damage(player, target, pt_damage):
            if pt_damage == -1:
                target.stat[5] = 0
                return f"__{target.name}__ meurt sur le coup.\n"
            
            elif not pt_damage:
                return f"__{target.name}__ parvient à parer le coup.\n"
            
            else:
                target.stat[5] -= pt_damage
                return f"__{target.name}__ subit {pt_damage} dégâts.\n"

        def turn(player, target):
            result = f"__{player.name}__ s'avance pour attaquer…\n"
            if phase_2(player):
                result += f"Le coup porte !\n"
                result += comment_on_damage(player, target, phase_3(player, target))

                if target.isalive():
                    result += f"__{target.name}__ est toujours vivant.\n"
    
                else:
                    inventory = target.inventory[:]
                    result += f"__{player.name}__ fouille le cadavre et récupère {target.stat[7]} Drachmes."
                    if inventory:
                        result += f"\n__{player.name}__ trouve\n - " + "\n - ".join(inventory)
                        for item in inventory: player.object_add(item)
                    player.stat[7] += target.stat[7]
                    self.players.pop(target.id)
                    return result, True

            else:
                result = f"Mais __{target.name}__ esquive le coup…\n"

            return result, False
                    
        if phase_1(user, enemy):
            fighters = (user, enemy)
        else:
            fighters = (enemy, user)
            
        result = f"__{fighters[0].name}__ engage le combat.\n"

        fight = turn(fighters[0], fighters[1])
        result += fight[0]
            
        if fight[1]: return result

        result +=f"__{fighters[1].name}__ riposte…\n"
            
        fight = turn(fighters[1], fighters[0])
        result += fight[0]

        if not fight[1]: result += f"\n**Points de vie restant**\n - __{user.name}__ : {user.stat[5]} Pv restant\n - __{enemy.name}__ : {enemy.stat[5]} Pv restant"
        return result
            
    def player_information(self, message):
        target = analyse(message, self.SEP)
        
        if target:
            target = self.id_to_object(self.nick_to_id(target[0]))
            if not target: return analyse(message, self.SEP)[0]
        else:
            target = self.id_to_object(get_user(message)[1])
            if not target: return get_user(message)[0]
            
        return target.get_stat()

    def specialpower(self, message):
        user = self.id_to_object(get_user(message)[1])

        if not user:
            return f"*Erreur : {get_user(message[0])} n'existe pas.*"

        args = analyse(message, self.SEP)

        if not args:
            return self.specialpower_list(user)

        args[0] = args[0].capitalize()
        power_available = user.get_special_powers()

        if data_power_index(args[0]) not in power_available:
            return f"*Erreur : {user.name} n'a pas le pouvoir : '{args[0]}'.*"
        
        if len(args) == 1:
            if data_powers()[data_power_index(args[0])][2]:
                return f"*Erreur : syntaxe invalide `{self.PREFIX}pouvoir {args[0]} {self.SEP} < nom_de_l'ennemi >`.*"
            return self.specialpower_use(args[0], user)

        args[1] = args[1].capitalize()
        
        target = self.id_to_object(self.nick_to_id(args[1]))
        
        if not target:
            return f"*Erreur : {args[1]} n'existe pas.*"

        if len(args) == 2:
            if not data_powers()[data_power_index(args[0])][2]:
                return f"*Erreur : syntaxe invalide `{self.PREFIX}pouvoir {args[0]}`.*"
            if target.place != user.place:
                return f"*Erreur : {user.name} et {target.name} ne sont pas au même endroit.*"
            return self.specialpower_use(args[0], user, target)
            
    def specialpower_list(self, user):
        power_available = user.get_special_powers()
        if not power_available:
            return f"__{user.name}__ n'a pas de pouvoir."
        
        all_power = data_powers()
        rslt = f"Pouvoirs spéciaux de __{user.name}__. Pour utiliser un pouvoir :\n`{self.PREFIX}pouvoir < nom_du_pouvoir > [ {self.SEP} < nom_de_l'ennemi >]`"

        for power_index in power_available:
            rslt += f"\n - __{all_power[power_index][0]}__ : {all_power[power_index][1]}"
            if all_power[power_index][2]: rslt += " Nom de l'ennemi à spécifier."

        return rslt

    def specialpower_use(self, power_name, user, target = None):
        user.capacity_modify(6, -1)
        
        if not user.stat[6]:
            return f"__{user.name}__ tente de lancer {power_name}… Mais rate le sort."

        msg = f"__{user.name}__ lance {power_name}.\n"
        s_power = SpecialPower(power_name, user, self.players, target)
        msg += s_power.launch()
    
        return msg

    def roll_dice(self, message):
        user = self.id_to_object(get_user(message)[1])
        
        if not user:
            return f"*Erreur : {get_user(message)[0]} n'existe pas.*"

        args = analyse(message, self.SEP)
        
        if not args:
            faces, nb = 20, 1
            
        elif len(args) == 1:
            faces, nb = args[0], 1
            
        elif len(args) == 2:
            faces, nb = args[0], args[1]
        
        else:
            return f"*Erreur : syntaxe invalide `{self.PREFIX}dé [< nb_de_faces > {self.SEP} [< nb_de_dés >]]`.*"
        
        if faces < 3: faces = 3
        if nb < 1: nb = 1

        return f"__{user.name}__ lance {nb} dé{('', 's')[nb > 1]} à {faces} faces. Résultat obtenu : {roll_die(faces, nb)} / {faces * nb}."

    def roll_capacity(self, message):
        user = self.id_to_object(get_user(message)[1])
        if not user:
            return f"*Erreur : {get_user(message)[0]} n'est pas un joueur enregistré.*"
        
        capacity_name = analyse(message, self.SEP)[0].capitalize()
        
        try:
            capacity_index = ["Courage", "Force", "Habileté", "Rapidité", "Défense", "", "Mana"].index(capacity_name)
        except:
            return f"*Erreur : {capacity_name} n'est pas une capacité.*"
        
        comment = user.capacity_roll(capacity_index)
        result = f"__{user.name}__ a {('fait un échec critique sur', 'raté', 'réussi de justesse', 'réussi')[comment]} son lancer "
        
        if capacity_index == 2:
            result += "d'Habileté."
        else:
            result += f"de {capacity_name}."

        return result

    def place_change(self, message):
        user = self.id_to_object(get_user(message)[1])
        if not user:
            return f"*Erreur : {get_user(message)[0]} n'est pas un joueur enregistré.*"

        new_place = analyse(message, self.SEP)
        if not new_place:
            return f"*Erreur : syntaxe invalide `{self.PREFIX}lieu < nom_du_lieu >`.*"
        
        user.place = new_place[0]
        return f"__{user.name}__ se dirige vers {user.place}."

    def show_articles(self, message):
        user = self.id_to_object(get_user(message)[1])
        if not user:
            return f"*Erreur : {get_user(message)[0]} n'est pas un joueur enregistré.*", -1

        shop_name = user.inshop()
        if not shop_name:
            return f"*Erreur : {user.name} n'est pas dans un magasin.*", -1

        item_name = analyse(message, self.SEP)
        
        if item_name:
            item_name = item_name[0]
            if item_name in data_shop()[shop_name]:
                return (item_name, object_stat(item_name)), user.stat[8], 1
            else:
                return f"*Erreur : cet objet n'est pas vendu ici. Consultez la liste des objets disponibles via : `{self.PREFIX}article`.*", -1, 2

        else:
            return (user.place, data_shop()[shop_name]), user.stat[8], 0

    def buy(self, message):
        user = self.id_to_object(get_user(message)[1])
        if not user:
            return f"*Erreur : {get_user(message)[0]} n'est pas un joueur enregistré.*"

        shop_name = user.inshop()
        if not shop_name:
            return f"*Erreur : {user.name} n'est pas dans un magasin.*"
        
        item_name = analyse(message, self.SEP)
        if not item_name:
            return f"*Erreur : syntaxe invalide `{self.PREFIX}achat < nom_de_l'objet >`."

        item_name = item_name[0]
        
        if item_name not in data_shop()[shop_name]:
            return f"*Erreur : cet objet n'est pas vendu ici. Consultez les objets disponibles via : `{self.PREFIX}article`.*"

        price = object_stat(item_name)[0][7]
        user.object_add(item_name)
        user.stat[7] += price
        return f"__{user.name}__ a acheté {item_name} pour {abs(price)} Drachmes."

    def object_take(self, message):
        user = self.id_to_object(get_user(message)[1])
        if not user:
            return f"*Erreur : {get_user(message)[0]} n'est pas un joueur enregistré.*"

        object_name = analyse(message, self.SEP)

        if not object_name:
            return f"*Erreur : syntaxe invalide `{self.PREFIX}prend < nom_de_l'objet >`.*"

        object_name = object_name[0]
        
        if object_name in user.inventory:
            return f"*Erreur : {user.name} a déjà cet objet.*"
        
        user.object_add(object_name)
        return f"__{user.name}__ prend {object_name}."

    def object_give(self, message):
        user = self.id_to_object(get_user(message)[1])
        if not user:
            return f"*Erreur : {get_user(message)[0]} n'est pas un joueur enregistré.*"
        args = analyse(message, self.SEP)

        if len(args) > 3:
            return f"*Erreur : syntaxe invalide `{self.PREFIX}donne < nom_du_receveur > {self.SEP} < nom_de_l'objet >`.*"
        
        player = self.id_to_object(self.nick_to_id(args[0]))
        
        if not player:
            return f"*Erreur : {args[0]} n'existe pas.*"
        elif user.place.lower() != player.place.lower():
            return f"*Erreur : {user.name} et {player.name} ne sont pas au même endroit.*"
        
        if args[1].lower() == "argent":
            amount = abs(args[2])
            
            if amount > user.stat[7]:
                return f"*Erreur : {user.name} ne peut pas donner de Drachmes.*"

            user.stat[7] -= amount
            player.stat[7] += amount

            return f"__{user.name}__ donne {amount} Drachmes à __{player.name}__."
            
        else:
            object_name = args[1]
            if object_name not in user.inventory:
                return f"*Erreur : {user.name} ne possède pas cet objet : '{object_name}'.*"
            elif object_name in player.inventory:
                return f"*Erreur : {player.name} a déjà cet objet.*"
        
            user.object_del(object_name)
            player.object_add(object_name)
        
            return f"__{user.name}__ donne {object_name} à __{player.name}__."

    def object_throw(self, message, use):
        user = self.id_to_object(get_user(message)[1])
        if not user:
            return f"*Erreur : {get_user(message)[0]} n'est pas un joueur enregistré.*"
        
        object_name = analyse(message, self.SEP)

        if not object_name:
            return f"*Erreur : syntaxe invalide `{self.PREFIX}{('jette', 'utilise')[use]} < nom_de_l'objet >`.*"

        object_name = object_name[0]

        if object_name not in user.inventory:
            return f"*Erreur : {user.name} ne possède pas cet objet : '{object_name}'*."

        if use:
            if object_stat(object_name)[1] != 1: return f"*Erreur : cet objet ne peut pas être utilisé.*"
            user.object_use(object_name)
        else:
            user.object_del(object_name)
        
        return f"__{user.name}__ {('jette', 'utilise')[use]} {object_name}."


# --- Administration --- #

    def save(self):
        player_file = [object_to_save(player) for player in self.players.values()]
        save_file = [player_file, self.kick, self.server_id]
        save_send(str(save_file))
        print("Partie sauvegardée.")

    def load(self, message):
        if get_user(message)[1] not in data_admin():
            return "*< commande non autorisée >*"
        save_send(message.content[9:])
        return "Partie chargée."

    def player_modify(self, message):
        if get_user(message)[1] not in data_admin():
            return "*< commande non autorisée >*"
        
        user = self.id_to_object(get_user(message)[1])

        try:
            player_name, capacity_name, new_value = analyse(message, self.SEP)
        except:
            return f"*Erreur : syntaxe invalide `{self.PREFIX}modifier < nom_joueur > {self.SEP} < nom_capacité > {self.SEP} < valeur >`*"
        player = self.id_to_object(self.nick_to_id(player_name))

        if not player:
            return f"*Erreur : {player_name} n'existe pas.*"


        capacity_name = capacity_name.lower()
        capacity_list = ("courage", "force", "habileté", "rapidité", "défense", "vie", "mana", "argent")
        
        if capacity_name in capacity_list:
            player.capacity_modify(capacity_list.index(capacity_name), new_value)
            result = f"__{player.name}__ {('perd', 'gagne')[new_value > 0]} {new_value} "
            
            if capacity_name == "habileté":
                result += f"point{('', 's')[new_value > 1]} d'Habileté."
                
            elif capacity_name == "argent":
                result += "Drachmes."
                
            else:
                result += f"point{('', 's')[new_value > 1]} de {capacity_name}."

        elif capacity_name == "toutes":
            result = f"__{player.name}__ {('perd', 'gagne')[new_value > 0]} {new_value} point{('', 's')[abs(new_value) > 1]} de Courage, de Force, d'Habileté et de Rapidité."
            for i in range(4): player.capacity_modify(i, new_value)

        elif capacity_name == "lieu":
            player.place = new_value
            result = f"__{player.name}__ se dirige vers {new_value}."

        elif capacity_name == "objet+":
            if new_value not in player.inventory:
                player.object_add(new_value)
                result = f"__{player.name}__ reçoit {new_value}."
            else:
                resutl = f"__{player.name}__ a déjà {new_value}."

        elif capacity_name == "objet-":
            if new_value in player.inventory:
                player.object_del(new_value)
                result = f"__{player.name}__ a perdu {new_value}."
            else:
                result = f"__{player.name}__ ne possède pas cet objet : '{new_value}'."

        elif capacity_name == "nom":
            old_name = player.name
            player.name = new_value
            result = f"Le pseudo de {old_name} est devenu : {new_value}."

        else:
            result = "*Erreur : la capacité saisie ne correspond à aucune capacité connue.*"

        if not player.isalive():
            result += f"\n__{player.name}__ a succombé a ses blessures."
            self.players.pop(player.id)
        
        return result

    def player_kick(self, message):
        if get_user(message)[1] not in data_admin():
            return "*< commande non autorisée >*"

        player_name = analyse(message, self.SEP)[0]
        player_id = self.nick_to_id(player_name)
        
        if not player_id:
            return f"*Erreur : {player_name} n'existe pas.*"
            
        self.kick.append(int(player_id))
        self.players.pop(player_id)
        return f"{player_name} a été kické."

    def player_unkick(self, message):
        if get_user(message)[1] not in data_admin():
            return "*< commande non autorisée >*"

        player_id = int(analyse(message, self.SEP)[0])
        for i in self.kick:
            if i == player_id:
                self.kick.remove(player_id)
                return f"Le joueur n°{player_id} a été unkick."

        return f"*Erreur : le joueur ciblé n'est pas kické.*"

    def clear_kick(self, message):
        if get_user(message)[1] not in data_admin():
            return "*< commande non autorisée >*"

        self.kick = []
        
        return "Tous les joueurs kickés ont été unkick."

    def clear_player(self, message):
        if get_user(message)[1] not in data_admin():
            return "*< commande non autorisée >*"

        self.players = {}
        
        return "Tous les joueurs ont été supprimés."

    def clear_all(self, message):
        if get_user(message)[1] not in data_admin():
            return "*< commande non autorisée >*"

        self.server_id = 0
        save_delete()
        
        return "Sauvegarde effacée."