# ----- Code numérique pour le stockage des objets
# 0 : peut-être stocké
# 1 : peut-être consommé plus tard
# 2 : doit être consommé au moment de l'achat
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
            "une chambre": ({"Courage":10, "Force":10, "Habileté":10, "Rapidité":10, "Défense":0, "Vie":25, "Mana":5, "Argent":-10}, 2),
            "un repas chaud": ({"Courage":10, "Force":10, "Habileté":0, "Rapidité":10, "Défense":0, "Vie":10, "Mana":0, "Argent":-7}, 2),
            "un repas frois": ({"Courage":5, "Force":5, "Habileté":0, "Rapidité":5, "Défense":0, "Vie":5, "Mana":0, "Argent":-5}, 2),
            "une bière": ({"Courage":2, "Force":2, "Habileté":2, "Rapidité":2, "Défense":0, "Vie":0, "Mana":0, "Argent":-2}, 2),
            "un lait de chèvre": ({"Courage":5, "Force":5, "Habileté":5, "Rapidité":5, "Défense":0, "Vie":5, "Mana":0, "Argent":-5}, 2),
            "du vin": ({"Courage":5, "Force":5, "Habileté":-2, "Rapidité":-1, "Défense":0, "Vie":1, "Mana":0, "Argent":-5}, 1),
            "de la viande séchée": ({"Courage":2, "Force":2, "Habileté":2, "Rapidité":2, "Défense":0, "Vie":2, "Mana":0, "Argent":-5}, 1),
            "du pain": ({"Courage":5, "Force":0, "Habileté":5, "Rapidité":0, "Défense":0, "Vie":5, "Mana":0, "Argent":-2}, 1),
            "du fromage": ({"Courage":0, "Force":10, "Habileté":0, "Rapidité":5, "Défense":0, "Vie":5, "Mana":0, "Argent":-5}, 1),
        },

    "forge":
        {
            "une épée": ({"Courage":0, "Force":0, "Habileté":15, "Rapidité":15, "Défense":10, "Vie":0, "Mana":0, "Argent":-20}, 0),
            "un arc": ({"Courage":25, "Force":0, "Habileté":15, "Rapidité":15, "Défense":0, "Vie":0, "Mana":0, "Argent":-70}, 0),
            "une hache": ({"Courage":10, "Force":10, "Habileté":15, "Rapidité":20, "Défense":0, "Vie":0, "Mana":0, "Argent":-50}, 0),
            "une arbalète": ({"Courage":5, "Force":0, "Habileté":15, "Rapidité":25, "Défense":0, "Vie":0, "Mana":0, "Argent":-40}, 0),
            "une côte de maille": ({"Courage":5, "Force":0, "Habileté":-5, "Rapidité":-5, "Défense":15, "Vie":0, "Mana":0, "Argent":-20}, 0),
            "une armure": ({"Courage":15, "Force":0, "Habileté":-10, "Rapidité":-10, "Défense":100, "Vie":0, "Mana":0, "Argent":-100}, 0),
            "un bouclier": ({"Courage":10, "Force":0, "Habileté":-10, "Rapidité":-5, "Défense":25, "Vie":0, "Mana":0, "Argent":-30}, 0),
            "une armure souple": ({"Courage":10, "Force":0, "Habileté":-5, "Rapidité":-10, "Défense":25, "Vie":0, "Mana":0, "Argent":-15}, 0),
            "une dague": ({"Courage":-5, "Force":-5, "Habileté":10, "Rapidité":10, "Défense":0, "Vie":0, "Mana":0, "Argent":-10}, 0),
            "un katana": ({"Courage":10, "Force":15, "Habileté":5, "Rapidité":5, "Défense":5, "Vie":0, "Mana":0, "Argent":-30}, 0),
            "une épée batarde": ({"Courage":10, "Force":15, "Habileté":-5, "Rapidité":-10, "Défense":10, "Vie":0, "Mana":0, "Argent":-30}, 0),
            "un grand arc": ({"Courage":20, "Force":0, "Habileté":15, "Rapidité":10, "Défense":0, "Vie":0, "Mana":0, "Argent":-40}, 0),
            "un arc long": ({"Courage":10, "Force":20, "Habileté":10, "Rapidité":5, "Défense":0, "Vie":0, "Mana":0, "Argent":-50}, 0),
            "une hallebarde": ({"Courage":5, "Force":10, "Habileté":-5, "Rapidité":-5, "Défense":0, "Vie":0, "Mana":0, "Argent":-15}, 0),
        },

    "officine":
        {
            "une potion de courage": ({"Courage":10, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-15}, 1),
            "une potion de force": ({"Courage":0, "Force":10, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-15}, 1),
            "une potion d'habileté": ({"Courage":0, "Force":0, "Habileté":10, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-15}, 1),
            "une potion de rapidité": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":10, "Défense":0, "Vie":0, "Mana":0, "Argent":-15}, 1),
            "une potion de vie": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":10, "Mana":0, "Argent":-15}, 1),
            "une potion de mana": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":10, "Argent":-15}, 1),
            "une potion de puissance": ({"Courage":20, "Force":20, "Habileté":20, "Rapidité":20, "Défense":20, "Vie":20, "Mana":20, "Argent":-100}, 1),
            "du poison": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":10, "Défense":0, "Vie":0, "Mana":0, "Argent":-15}, 0),
            "une fiole vide": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":10, "Défense":0, "Vie":0, "Mana":0, "Argent":-30}, 0),
        },

    "tannerie":
        {
            "des bottes": ({"Courage":10, "Force":0, "Habileté":0, "Rapidité":0, "Défense":5, "Vie":0, "Mana":0, "Argent":-15}, 0),
            "une cape": ({"Courage":0, "Force":5, "Habileté":0, "Rapidité":0, "Défense":10, "Vie":0, "Mana":0, "Argent":-15}, 0),
            "des bottes enchantées": ({"Courage":10, "Force":0, "Habileté":0, "Rapidité":0, "Défense":5, "Vie":0, "Mana":5, "Argent":-30}, 0),
            "une cape enchantée": ({"Courage":0, "Force":5, "Habileté":0, "Rapidité":0, "Défense":10, "Vie":0, "Mana":5, "Argent":-30}, 0),
        },

    "écurie":
        {
            "un cheval": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":10, "Défense":0, "Vie":0, "Mana":0, "Argent":-30}, 0),
        },

    "port":
        {
            "une barque": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-40}, 0),
            "un voilier": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-100}, 0),
            "une goélette franche": ({"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-200}, 0),
        },
    }
