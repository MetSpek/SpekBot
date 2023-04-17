import csv

all_pokemon = []
all_cases = {}

cases_to_fill = [["standard", ""],["gen", 1]]

with open("data\data.csv", 'r') as file:
  csvreader = csv.reader(file)
  for row in csvreader:
    all_pokemon.append(row)

def fill(case):
    case_name = case[0]
    case_type = case[1]
    pokemon_list = []

    match case_name:
        case "standard":
            all_cases[case_name] = all_pokemon
        case "gen":
            print("ewa")
            for pokemon in all_pokemon:
                if pokemon[2] == str(case_type):
                    pokemon_list.append(pokemon)
            all_cases[case_name + str(case_type)] = pokemon_list

def fill_cases():
    for case in cases_to_fill:
        fill(case)

def main():
    fill_cases()

main()