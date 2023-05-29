import csv

all_pokemon = []
all_cases = {}


cases_to_fill = [["standard", ""],["gen", 1]]

with open("Pokemon\data.csv", encoding='utf-8-sig') as file:
  csvreader = csv.reader(file)
  for row in csvreader:
    pokemon = {
        "id" : row[0],
        "name" : row[1],
        "gen" : row[2],
        "rarity" : row[3],
        "primary_type" : row[4],
        "secondary_type" : row[5]
    }
    all_pokemon.append(pokemon)

def fill(case):
    case_name = case[0]
    case_type = case[1]
    pokemon_list = {
        'common' : [],
        'uncommon' : [],
        'rare' : [],
        'legendary' : []
    }

    match case_name:
        case "standard":
            for pokemon in all_pokemon:
                pokemon_list[pokemon["rarity"]].append(pokemon)
            all_cases[case_name] = pokemon_list
        case "gen":
            for pokemon in all_pokemon:
                if pokemon["gen"] == str(case_type):
                    pokemon_list[pokemon["rarity"]].append(pokemon)
            all_cases[case_name + " " + str(case_type)] = pokemon_list

def fill_cases():
    for case in cases_to_fill:
        fill(case)


def main():
    fill_cases()

main()