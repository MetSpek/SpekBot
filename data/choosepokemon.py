import random
import data.pokemondata as pokemondata
import data.iv as iv

def choose_pokemon(case):
    if pokemondata.all_cases[case]:
        chosen_rarity = random.randrange(1, 100)

        if chosen_rarity > 0 and chosen_rarity < 51:
            rarity = "common"
        elif chosen_rarity > 50 and chosen_rarity < 76:
            rarity = "uncommon"
        elif chosen_rarity > 75 and chosen_rarity < 96:
            rarity = "rare"
        else:
            rarity = "legendary"
    
    pokemon = pokemondata.all_cases[case][rarity][random.randint(0, len(pokemondata.all_cases[case][rarity]) - 1)]
    iv_list = iv.get_iv()
    pokemon["iv_list"] = iv_list["iv_list"]
    pokemon["iv_total"] = iv_list["iv_total"]

    pokemon["worth"] = calculate_pbc(pokemon["rarity"], pokemon["iv_total"])
    print(pokemon)
    return pokemon

def calculate_pbc(rarity, iv):
    match rarity:
        case "common":
            pbc = int(12 * iv)
    
    return pbc
