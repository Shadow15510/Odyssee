# ----- Code numérique pour le stockage des objets
# 0 : à porter
# 1 : peut-être consommé plus tard
# 2 : doit être consommé au moment de l'achat
# 3 : arme de mêlée
# 4 : arme à distance
# 5 : projectiles
# -----

def data_shop_name():
    return {
        "auberge": ["auberge", "taverne", "gargote", "hôtel"],
        "forge": ["forge", "armurerie"],
        "officine": ["pharmacie", "herboristerie", "officine", "apothicairerie"],
        "tannerie": ["maroquinerie", "tannerie"],
        "écurie": ["écurie", "haras"],
        "port": ["port"]
        }


def data_shop():
    return {
    "auberge":
        {
            "chambre": ({"Courage":10, "Force":10, "Habileté":10, "Rapidité":10, "Défense":0, "Vie":25, "Mana":5, "Argent":-40}, 2),
            "repas chaud": ({"Courage":10, "Force":10, "Habileté":0, "Rapidité":10, "Défense":0, "Vie":10, "Mana":0, "Argent":-20}, 2),
            "repas frois": ({"Courage":5, "Force":5, "Habileté":0, "Rapidité":5, "Défense":0, "Vie":5, "Mana":0, "Argent":-15}, 2),
            "bière": ({"Courage":2, "Force":2, "Habileté":2, "Rapidité":2, "Défense":0, "Vie":0, "Mana":0, "Argent":-10}, 2),
            "lait de chèvre": ({"Courage":5, "Force":5, "Habileté":5, "Rapidité":5, "Défense":0, "Vie":5, "Mana":0, "Argent":-10}, 2),
            "vin": ({"Courage":5, "Force":5, "Habileté":-2, "Rapidité":-1, "Défense":0, "Vie":1, "Mana":0, "Argent":-10}, 1),
            "viande séchée": ({"Courage":2, "Force":2, "Habileté":2, "Rapidité":2, "Défense":0, "Vie":2, "Mana":0, "Argent":-10}, 1),
            "pain": ({"Courage":5, "Force":0, "Habileté":5, "Rapidité":0, "Défense":0, "Vie":5, "Mana":0, "Argent":-5}, 1),
            "fromage": ({"Courage":0, "Force":10, "Habileté":0, "Rapidité":5, "Défense":0, "Vie":5, "Mana":0, "Argent":-10}, 1),
            "vinaigre": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-15}, 1),
            "huile": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-15}, 1),
            "miel": ({"Courage":10, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":5, "Mana":0, "Argent":-15}, 1),
            "sel": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-15}, 1),
            "gousse d'ail": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-15}, 1),
        },

    "forge":
        {
            "épée": ({"Courage":5, "Force":0, "Habileté":-5, "Rapidité":10, "Défense":5, "Vie":0, "Mana":0, "Argent":-20}, 3),
            "arc": ({"Courage":25, "Force":0, "Habileté":15, "Rapidité":15, "Défense":0, "Vie":0, "Mana":0, "Argent":-70}, 4),
            "hache": ({"Courage":10, "Force":10, "Habileté":15, "Rapidité":20, "Défense":0, "Vie":0, "Mana":0, "Argent":-50}, 3),
            "arbalète": ({"Courage":5, "Force":0, "Habileté":15, "Rapidité":25, "Défense":0, "Vie":0, "Mana":0, "Argent":-40}, 4),
            "côte de maille": ({"Courage":5, "Force":0, "Habileté":-5, "Rapidité":-5, "Défense":15, "Vie":0, "Mana":0, "Argent":-20}, 0),
            "armure": ({"Courage":15, "Force":0, "Habileté":-10, "Rapidité":-10, "Défense":100, "Vie":0, "Mana":0, "Argent":-100}, 0),
            "bouclier": ({"Courage":10, "Force":0, "Habileté":-10, "Rapidité":-5, "Défense":25, "Vie":0, "Mana":0, "Argent":-30}, 0),
            "armure souple": ({"Courage":10, "Force":0, "Habileté":-5, "Rapidité":-10, "Défense":25, "Vie":0, "Mana":0, "Argent":-25}, 0),
            "dague": ({"Courage":-5, "Force":-5, "Habileté":10, "Rapidité":10, "Défense":0, "Vie":0, "Mana":0, "Argent":-15}, 3),
            "katana": ({"Courage":10, "Force":15, "Habileté":5, "Rapidité":5, "Défense":5, "Vie":0, "Mana":0, "Argent":-30}, 3),
            "épée batarde": ({"Courage":10, "Force":15, "Habileté":5, "Rapidité":-10, "Défense":10, "Vie":0, "Mana":0, "Argent":-30}, 3),
            "grand arc": ({"Courage":20, "Force":0, "Habileté":15, "Rapidité":10, "Défense":0, "Vie":0, "Mana":0, "Argent":-40}, 4),
            "arc long": ({"Courage":10, "Force":20, "Habileté":10, "Rapidité":5, "Défense":0, "Vie":0, "Mana":0, "Argent":-50}, 4),
            "hallebarde": ({"Courage":5, "Force":10, "Habileté":-5, "Rapidité":-5, "Défense":0, "Vie":0, "Mana":0, "Argent":-20}, 3),
            "flèche": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-2}, 5),
            "carreau": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-2}, 5),
        },

    "officine":
        {
            "potion de courage": ({"Courage":10, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-30}, 1),
            "potion de force": ({"Courage":0, "Force":10, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-30}, 1),
            "potion d'habileté": ({"Courage":0, "Force":0, "Habileté":10, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-30}, 1),
            "potion de rapidité": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":10, "Défense":0, "Vie":0, "Mana":0, "Argent":-30}, 1),
            "potion de vie": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":10, "Mana":0, "Argent":-30}, 1),
            "potion de mana": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":10, "Argent":-30}, 1),
            "potion de puissance": ({"Courage":20, "Force":20, "Habileté":20, "Rapidité":20, "Défense":20, "Vie":20, "Mana":20, "Argent":-100}, 1),
            "poison": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-30}, 0),
            "fiole vide": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-15}, 1),
            "cire d'abeille": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-15}, 1),
            "écorce de saule 5g": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-15}, 1),
            "fleurs d'oranger 5g": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-15}, 1),
            "feuilles de sauge 5g": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-15}, 1),
            "baies de genévrier 5g": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-15}, 1),
            "fruits de tilleul 5g": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-15}, 1),
            "racines de muguet 5g": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-15}, 1),
            "baies de belladone 5g": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-15}, 1),
            "antidote": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-15}, 1),
        },

    "tannerie":
        {
            "bottes": ({"Courage":10, "Force":0, "Habileté":0, "Rapidité":5, "Défense":5, "Vie":0, "Mana":0, "Argent":-30}, 0),
            "cape": ({"Courage":0, "Force":5, "Habileté":0, "Rapidité":10, "Défense":10, "Vie":0, "Mana":0, "Argent":-60}, 0),
            "bottes enchantées": ({"Courage":10, "Force":0, "Habileté":0, "Rapidité":0, "Défense":5, "Vie":0, "Mana":5, "Argent":-60}, 0),
            "cape enchantée": ({"Courage":0, "Force":5, "Habileté":0, "Rapidité":0, "Défense":10, "Vie":0, "Mana":5, "Argent":-120}, 0),
            "manteau": ({"Courage":5, "Force":0, "Habileté":10, "Rapidité":10, "Défense":5, "Vie":0, "Mana":0, "Argent":-50}, 0),
            "gants": ({"Courage":0, "Force":10, "Habileté":5, "Rapidité":0, "Défense":5, "Vie":0, "Mana":0, "Argent":-30}, 0),
        },

    "écurie":
        {
            "cheval": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":10, "Défense":0, "Vie":0, "Mana":0, "Argent":-100}, 0),
        },

    "port":
        {
            "barque": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-100}, 0),
            "voilier": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-300}, 0),
            "goélette franche": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-10000}, 0),
        },
    }
