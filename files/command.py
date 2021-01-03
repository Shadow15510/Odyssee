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
        return [[self.players[player_id].name, self.players[player_id].species, self.players[player_id].place, self.players[player_id].get_level(), player_id] for player_id in self.players], self.players[get_user(message)[1]].stat[8]

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
        
        return self.fight_new(user, message)
        
    def fight_new(self, user, message):
        enemy_id = -len(self.players)
        args = analyse(message, self.SEP)

        if len(args) == 1:
            enemy_name, weapon_name = args[0], None
        elif len(args) == 2:
            enemy_name, weapon_name = args
        else:
            return f"*Erreur : syntaxe invalide `{self.PREFIX}combat < nom_de_l'ennemi > [ {self.SEP} < nom_de_l'arme >]`.*"
        
        if self.nick_to_id(enemy_name):
            return self.fight_continue(user, enemy_name, weapon_name)
        elif self.nick_to_id(enemy_name.capitalize()):
            return self.fight_continue(user, enemy_name.capitalize(), weapon_name)
        
        enemy_name = enemy_name.capitalize()
        level = user.get_level()
        self.players.update({enemy_id : Player(enemy_id, enemy_name, "Ennemi", stat_gen(randint(level - 1, level + 1), user.stat[8], True), user.place)})

        return f"__{user.name}__ se prépare pour combattre {enemy_name}.\nEntrez `{self.PREFIX}combat {enemy_name} [ {self.SEP} < nom_de_l'arme >]` pour attaquer."

    def fight_continue(self, user, enemy_name, weapon_name):

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
            result = ""
            if phase_2(player):
                result += f"Le coup porte !\n"
                result += comment_on_damage(player, target, phase_3(player, target))
    
                if not target.isalive():
                    inventory = target.inventory[:]
                    result += f"\n**Butin**\n__{player.name}__ fouille le cadavre et récupère :\n - {target.stat[7]} Drachmes."
                    if inventory:
                        result += f"\n - " + "\n - ".join([item[0] + ('', f' ({item[1]})')[item[1] != -1] for item in inventory])
                        for item in inventory:
                            if item[1] != -1:
                                for _ in range(item[1]): player.object_add(item[0])
                            else: player.object_add(item[0])

                    player.stat[7] += target.stat[7]
                    self.players.pop(target.id)
                    return result, True

            else:
                result = f"Mais __{target.name}__ esquive le coup…\n"

            return result, False
        
        def enemy_weapon(enemy, wpn_type):
            enemy_wpn = enemy.find_by_type(wpn_type)

            if enemy_wpn[0]:
                if wpn_type == 4:
                    enemy_bullet = enemy.find_by_type(5)[0]
                    if not enemy_bullet:
                        return enemy_wpn[0], [0 for _ in range(8)], "", False
                    else:
                        return enemy_wpn[0], enemy_wpn[1], enemy_bullet, True
                else:
                    return enemy_wpn[0], enemy_wpn[1], "", True
            else:
                return "mains nues", [0 for _ in range(8)], "", wpn_type == 3

        def melee_fight(user, enemy):
            if phase_1(user, enemy):
                fighters = (user, enemy)
            else:
                fighters = (enemy, user)
                        
            result = f"__{fighters[0].name}__ engage le combat.\n"
            fight = turn(fighters[0], fighters[1])
            result += fight[0]
                
            if fight[1]: return result, True

            result +=f"__{fighters[1].name}__ riposte…\n"
            fight = turn(fighters[1], fighters[0])
            result += fight[0]

            return result, fight[1]

        def ranged_fight(user, enemy, bullet, ripost):
            if ripost:
                if phase_1(user, enemy):
                    fighters = (user, enemy)
                else:
                    fighters = (enemy, user)
                    bullet = bullet[1], bullet[0]

                result = f"__{fighters[0].name}__ vise {fighters[1].name}…\n"
                fighters[0].object_use(bullet[0])
                fight = turn(fighters[0], fighters[1])
                result += fight[0]

                if fight[1]: return result, True

                result += f"\n__{fighters[1].name}__ ajuste un tir.\n"
                fighters[1].object_use(bullet[1])
                fight = turn(fighters[1], fighters[0])
                result += fight[0]

            else:
                result = f"__{user.name}__ vise __{enemy.name}__\n"
                user.object_use(bullet[0])
                fight = turn(user, enemy)
                result += fight[0]

            return result, fight[1]

        enemy = self.id_to_object(self.nick_to_id(enemy_name))

        if weapon_name: user_weapon = user.have(weapon_name)
        else: weapon_name, user_weapon = "mains nues", (-1, [0 for _ in range(8)], -1)

        user_arrow = user.find_by_type(5)[0]

        if user_weapon == (-1, -1, -1):
            return f"*Erreur : {user.name} n'a pas cette arme : '{weapon_name}'*"
        elif user_weapon[2] == 4 and not user_arrow:
            return f"*Erreur : {user.name} n'a rien pour tirer sur {enemy_name}.*"

        if user_weapon[2] != 4 and user.place != enemy.place:
            return f"*Erreur : {user.name} et {enemy.name} ne sont pas au même endroit.*"

        enemy_weapon_name, enemy_weapon_stat, enemy_arrow, ripost = enemy_weapon(enemy, (3, 4)[user_weapon[2] == 4])
        
        result = f"__{user.name}__ se bat avec l'arme : '{weapon_name}'.\n"
        if ripost: result += f"__{enemy.name}__ se bat avec l'arme : '{enemy_weapon_name}'.\n"
        else: result += f"__{enemy.name}__ ne peut pas riposter.\n"

        user.stat_add(user_weapon[1])
        enemy.stat_add(enemy_weapon_stat)
        
        result += f"Les capacités temporaires sont :\n({user.name} | {enemy.name})\n"

        capacity_line = [f"`{name}.: {user.stat[index]}" for index, name in enumerate(("Courage .", "Force ...", "Habileté ", "Rapidité ", "Défense ."))]
        len_max = max([len(i) for i in capacity_line]) + 1
        capacity_line = [i + " " * (len_max - len(i)) + f"| {enemy.stat[index]}`" for index, i in enumerate(capacity_line)]

        result += "\n".join(capacity_line)
        result += "\n\n"

        if user_weapon[2] == 4:
            fight = ranged_fight(user, enemy, enemy_arrow, ripost)
        else:
            fight = melee_fight(user, enemy)

        result += fight[0]

        if not fight[1]: result += f"\n**Points de vie restant**\n - __{user.name}__ : {user.stat[5]} Pv restant\n - __{enemy.name}__ : {enemy.stat[5]} Pv restant"
        
        user.stat_sub(user_weapon[1])
        enemy.stat_sub(enemy_weapon_stat)

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
            return f"*Erreur : {get_user(message)[0]} n'est pas un joueur enregistré.*", -1, 2

        shop_name = user.inshop()
        item_name = analyse(message, self.SEP)

        if not shop_name:
            return f"*Erreur : {user.name} n'est pas dans un magasin.*", -1, 2
        
        if item_name:
            item_name = item_name[0]
            _, stat, check = object_stat(item_name, shop_name)
            if check != -1:
                return (item_name, (stat, check)), user.stat[8], 1
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
        
        args = analyse(message, self.SEP)

        if len(args) == 1:
            item_name, nb = args[0].lower(), 1
        elif len(args) == 2:
            item_name, nb = args[0].lower(), args[1]
        else:
            return f"*Erreur : syntaxe invalide `{self.PREFIX}achat < nom_de_l'objet > [ {self.SEP} < nombre >]`."

        _, stat, check = object_stat(item_name, shop_name)
        if nb <= 0: nb = 1

        if check == -1:
            return f"*Erreur : cet objet n'est pas vendu ici. Consultez les objets disponibles via : `{self.PREFIX}article`.*"
        elif user.stat[7] < nb * abs(stat[7]):
            return f"*Erreur : {user.name} n'a pas assez de Drachmes.*"
        else:
            if check in (1, 5):
                for _ in range(nb): user.object_add(item_name)
            else:
                if nb > 1: return f"*Erreur : {user.name} ne peut pas acheter plusieurs fois cet objet : '{item_name}'.*"
                if user.have(item_name)[0] == -1:
                    user.object_add(item_name)
                else:
                    return f"*Erreur : {user.name} a déjà cet objet.*"

            user.capacity_modify(7, nb * stat[7])
            return f"__{user.name}__ a acheté {item_name}{('', f' ({nb})')[nb > 1]} pour {nb * abs(stat[7])} Drachmes."

    def object_take(self, message):
        user = self.id_to_object(get_user(message)[1])
        if not user:
            return f"*Erreur : {get_user(message)[0]} n'est pas un joueur enregistré.*"

        args = analyse(message, self.SEP)
   
        if len(args) == 1:
            object_name, nb = args[0], 1
        elif len(args) == 2:
            object_name, nb = args
        else:
            return f"*Erreur : syntaxe invalide `{self.PREFIX}prend < nom_de_l'objet > [ {self.SEP} < nombre >]`.*"

        index, _, stockable = user.have(object_name)
        if nb <= 0: nb = 1

        if index != -1 and stockable not in (1, 5):
            return f"*Erreur : {user.name} a déjà cet objet.*"
        else:
            if stockable not in (1, 5): nb = 1
            for _ in range(nb): user.object_add(object_name)
            return f"__{user.name}__ prend {object_name}{('', f' ({nb})')[stockable in (1, 5)]}."
            
    def object_give(self, message):
        user = self.id_to_object(get_user(message)[1])
        if not user:
            return f"*Erreur : {get_user(message)[0]} n'est pas un joueur enregistré.*"
        args = analyse(message, self.SEP)

        if len(args) == 2:
            player, object_name = args
            amount = 1
        elif len(args) == 3:
            player, object_name, amount = args
            amount = abs(amount)
        else:
            return f"*Erreur : syntaxe invalide `{self.PREFIX}donne < nom_du_receveur > {self.SEP} < nom_de_l'objet > [ {self.SEP} < nombre >]`.*"
        
        player = self.id_to_object(self.nick_to_id(player))
        
        if not player:
            return f"*Erreur : {args[0]} n'existe pas.*"
        elif user.place.lower() != player.place.lower():
            return f"*Erreur : {user.name} et {player.name} ne sont pas au même endroit.*"
        
        if object_name.lower() == "argent":
            
            if amount > user.stat[7]:
                return f"*Erreur : {user.name} ne peut pas donner de Drachmes.*"

            user.stat[7] -= amount
            player.stat[7] += amount

            return f"__{user.name}__ donne {amount} Drachmes à __{player.name}__."
            
        else:
            index, _, check = user.have(object_name)
            if index == -1:
                return f"*Erreur : {user.name} ne possède pas cet objet : '{object_name}'.*"
            elif check in (1, 5) and amount > user.inventory[index][1]:
                return f"*Erreur : {user.name} ne possède pas en assez grande quantité l'objet : '{object_name}'.*"
            elif check not in (1, 5) and player.have(object_name)[0] != -1:
                return f"*Erreur : {player.name} a déjà cet objet.*"
            else:
                if check != 1: amount = 1
                object_name = user.inventory[index][0]
                for _ in range(amount):
                    user.object_del(object_name)
                    player.object_add(object_name)
                
            return f"__{user.name}__ donne {object_name}{('', f' ({amount})')[check in (1, 5)]} à __{player.name}__."

    def object_throw(self, message, use):
        user = self.id_to_object(get_user(message)[1])
        if not user:
            return f"*Erreur : {get_user(message)[0]} n'est pas un joueur enregistré.*"
        
        args = analyse(message, self.SEP)

        if len(args) == 1:
            object_name, nb = args[0], 1
        elif len(args) == 2:
            object_name, nb = args[0], args[1]
        else:
            return f"*Erreur : syntaxe invalide `{self.PREFIX}{('jette', 'utilise', 'vend')[use]} < nom_de_l'objet > [ {self.SEP} < nombre >]`.*"

        
        index, _, check = user.have(object_name)
    
        if check not in (1, 5): nb = 1

        if index == -1:
            return f"*Erreur : {user.name} ne possède pas cet objet : '{object_name}'.*"
        elif nb > user.inventory[index][1] and check in (1, 5):
            return f"*Erreur : {user.name} ne possède pas en assez grande quantité l'objet : '{object_name}'.*"

        object_name = user.inventory[index][0]


        if use == 0:
            if check in (1, 5) and nb > user.inventory[index][1]: nb = user.inventory[index][1]
            for _ in range(nb): user.object_del(object_name)

        elif use == 1:
            if check != 1:
                return f"*Erreur : cet objet ne peut pas être utilisé.*"
            else:
                for _ in range(nb): user.object_use(object_name)
               
        else:
            shop = user.inshop()
            if not shop:
                return f"*Erreur : {user.name} n'est pas dans un magasin.*"

            all_item = data_shop()[shop]

            item_name, stat, check = object_stat(object_name)
            price = int(0.75 * abs(stat[7]))

            if item_name in all_item:
                for _ in range(nb):
                    user.stat[7] += price
                    user.object_del(object_name)
                return f"__{user.name}__ vend l'objet : '{object_name}{('', f' ({nb})')[nb > 1]}' pour {price * nb} Drachmes."
            else:
                return f"*Erreur : {user.name} n'est pas dans le bon magasin, ou cet objet n'est pas vendable.*"


            

        return f"__{user.name}__ {('jette', 'utilise')[use]} {object_name} {('', f'({nb})')[check in (1, 5)]}."


    def speed_travel(self, message):
        args = analyse(message, self.SEP)
        
        if len(args) == 2:
            mean, weather = args
            land_type = False
        elif len(args) == 3:
            mean, weather, land_type = args
        else:
            return f"*Erreur : syntaxe invalide `{self.PREFIX}vitesse < moyen_de_transport > {self.SEP} < météo > [ {self.SEP} < type_de_terrain >]`.*", 0, 0, 0, False

        return get_speed(mean, weather, land_type)

        

    def time_travel(self, message):
        args = analyse(message, self.SEP)

        if len(args) == 3:
            distance, mean, weather = args
            land_type = False
        elif len(args) == 4:
            distance, mean, weather, land_type = args
        else:
            return f"*Erreur : syntaxe invalide `{self.PREFIX}temps < distance > {self.SEP} < moyen_de_transport > {self.SEP} < météo > [ {self.SEP} < type_de_terrain >]`.*", 0, 0, 0, False

        per_hour, per_day, hour_per_day, sea, success = get_speed(mean, weather, land_type)

        if not success: return per_hour, 0, 0, 0, False

        return [int((distance // i) % hour_per_day) for i in per_hour], [int(distance // i) for i in per_day], distance, sea, True

# --- Administration --- #

    def save(self):
        player_file = [object_to_save(player) for player in self.players.values()]
        save_file = [player_file, self.kick, self.server_id]
        save_send(str(save_file))
        print("Partie sauvegardée.")

    def load(self, message):
        save_send(message.content[9:])
        return "Partie chargée."

    def player_modify(self, message):
        user = self.id_to_object(get_user(message)[1])

        try:
            player_name, capacity_name, *new_value = analyse(message, self.SEP)
            if len(new_value) == 1:
                new_value, nb = new_value[0], 1
            else:
                new_value, nb = new_value
                nb = abs(nb)
        except:
            return f"*Erreur : syntaxe invalide `{self.PREFIX}modifier < nom_joueur > {self.SEP} < nom_capacité > {self.SEP} < valeur > [ {self.SEP} < nombre >]`*"
        player = self.id_to_object(self.nick_to_id(player_name))

        if not player:
            return f"*Erreur : {player_name} n'existe pas.*"


        capacity_name = capacity_name.lower()
        capacity_list = ("courage", "force", "habileté", "rapidité", "défense", "vie", "mana", "argent")
        
        if capacity_name in capacity_list:
            player.capacity_modify(capacity_list.index(capacity_name), new_value)
            result = f"__{player.name}__ {('perd', 'gagne')[new_value > 0]} {abs(new_value)} "
            
            if capacity_name == "habileté":
                result += f"point{('', 's')[new_value > 1]} d'Habileté."
                
            elif capacity_name == "argent":
                result += "Drachmes."
                
            else:
                result += f"point{('', 's')[new_value > 1]} de {capacity_name}."

        elif capacity_name == "toutes":
            result = f"__{player.name}__ {('perd', 'gagne')[new_value > 0]} {abs(new_value)} point{('', 's')[abs(new_value) > 1]} de Courage, de Force, d'Habileté et de Rapidité."
            for i in range(4): player.capacity_modify(i, new_value)

        elif capacity_name == "lieu":
            player.place = new_value
            result = f"__{player.name}__ se dirige vers {new_value}."

        elif capacity_name == "objet+":
            index, _, stockable = player.have(new_value)
            if stockable not in (1, 5): nb = 1

            if index == -1 or stockable in (1, 5):
                for _ in range(nb): player.object_add(new_value)
                result = f"__{player.name}__ reçoit {new_value}{('', f' ({nb})')[stockable in (1, 5)]}."
            else:
                result = f"__{player.name}__ a déjà cet objet : '{new_value}'."

        elif capacity_name == "objet-":
            index, _, stockable = player.have(new_value)
            if stockable not in (1, 5): nb = 1
            elif nb > player.inventory[index][1]: nb = player.inventory[index][1]

            if index != -1:
                for _ in range(nb): player.object_del(new_value)
                result = f"__{player.name}__ a perdu {new_value}{('', f' ({nb})')[stockable in (1, 5)]}."
            else:
                result = f"__{player.name}__ ne possède pas cet objet : '{new_value}'."  

        elif capacity_name == "nom":
            old_name = player.name
            player.name = new_value
            result = f"Le pseudo de {old_name} est devenu : {new_value}."

        elif capacity_name == "espèce":
            new_value = new_value.capitalize()
            player.species = new_value
            result = f"__{player.name}__ est devenu(e) un(e) {new_value}."

        elif capacity_name == "pouvoir+":
            power_check = player.power_add(new_value)
            result = ("*Erreur : '{new_value}' n'est pas un pouvoir connu.*", f"*Erreur : {player.name} connaît déjà le sort '{new_value}'.*", f"__{player.name}__ apprend le sort : '{new_value}'.")[power_check]

        elif capacity_name == "pouvoir-":
            power_check = player.power_sub(new_value)
            result = (f"*Erreur : '{new_value}' n'est pas un pouvoir connu.*", f"Erreur : {player.name} ne connaît pas le sort : '{new_value}'", f"__{player.name}__ oublie le sort : '{new_value}'")[power_check]

        else:
            result = "*Erreur : la capacité saisie ne correspond à aucune capacité connue.*"

        if not player.isalive():
            result += f"\n__{player.name}__ a succombé a ses blessures."
            self.players.pop(player.id)
        
        return result

    def player_create(self, message):
        try:
            name, species = analyse(message, self.SEP)
        except:
            return f"*Erreur : syntaxe invalide `{self.PREFIX}joueur_plus < nom > {self.SEP} < espèce >`.*"

        if name in self.players:
            return f"*Erreur : {name} existe déjà.*"
        else:
            name = name.capitalize()
            new_id = -len(self.players)
            self.players.update({new_id: Player(new_id, name, species.capitalize())})
            self.players[new_id].stat[7] = 0
            self.players[new_id].stat[6] = 0
            return f"{name}, un(e) {species}, est apparu(e)."

    def player_delete(self, message):
        player_name = analyse(message, self.SEP)

        if not player_name:
            return f"*Erreur : syntaxe invalide `{self.PREFIX}joueur_moins < nom >`.*"
        
        player_name = player_name[0]
        player_id = self.nick_to_id(player_name)

        if not player_id:
            return f"*Erreur : {player_name} n'est pas un joueur enregistré.*"
        self.players.pop(player_id)

        return f"__{player_name}__ a été supprimé."


    def player_kick(self, message):
        player_name = analyse(message, self.SEP)[0]
        player_id = self.nick_to_id(player_name)
        
        if not player_id:
            return f"*Erreur : {player_name} n'existe pas.*"
            
        self.kick.append(int(player_id))
        self.players.pop(player_id)
        return f"{player_name} a été kické."

    def player_unkick(self, message):
        player_id = int(analyse(message, self.SEP)[0])
        for i in self.kick:
            if i == player_id:
                self.kick.remove(player_id)
                return f"Le joueur n°{player_id} a été unkick."

        return f"*Erreur : le joueur ciblé n'est pas kické.*"

    def clear_kick(self, message):
        self.kick = []
        
        return "Tous les joueurs kickés ont été unkick."

    def clear_player(self, message):
        self.players = {}
        
        return "Tous les joueurs ont été supprimés."

    def clear_all(self, message):
        self.server_id = 0
        save_delete()
        
        return "Sauvegarde effacée."