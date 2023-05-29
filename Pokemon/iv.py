import random

def get_iv():
    iv = {
        "iv_list" : [],
        "iv_total" : 0.0
    }

    for x in range(0,6):
        iv["iv_list"].append(random.randrange(0, 32))


    total_iv = 0
    for x in iv["iv_list"]:
       total_iv += x

    iv_percentage = (total_iv / 186) * 100
    iv["iv_total"] = round(iv_percentage, 2)

    return iv