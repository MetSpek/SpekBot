import random
import Pokemon.pokemondata as pokemondata
import Pokemon.iv as iv

def choose_pokemon(case):
    if pokemondata.all_cases[case]:
        chosen_rarity = random.random()

        if chosen_rarity > 0 and chosen_rarity < .51:
            rarity = "common"
        elif chosen_rarity > .50 and chosen_rarity < .86:
            rarity = "uncommon"
        elif chosen_rarity > .85 and chosen_rarity < .99:
            rarity = "rare"
        elif chosen_rarity > .98 and chosen_rarity < .995:
            rarity = "legendary"
        else:
            rarity = "mythical"

        if rarity == "mythical":
            pokemon = pokemondata.all_cases[case][random.randint(0, len(pokemondata.all_cases[case]) - 1)]
        else:
            pokemon = pokemondata.all_cases[case][rarity][random.randint(0, len(pokemondata.all_cases[case][rarity]) - 1)]

        iv_list = iv.get_iv()
        pokemon["iv_list"] = iv_list["iv_list"]
        pokemon["iv_total"] = iv_list["iv_total"]

        pokemon["worth"] = calculate_pbc(pokemon["rarity"], pokemon["iv_total"])
        return pokemon

def calculate_pbc(rarity, iv):
    match rarity:
        case "common":
            pbc = int(.12 * iv)
        case "uncommon":
            pbc = int(1.2 * iv)
        case "rare":
            pbc = int(12.3 * iv)
        case "legendary":
            pbc = int(123.4 * iv)
        case "mythical":
            pbc = int(1234.5 * iv)
    return pbc
