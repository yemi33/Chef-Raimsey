import os
def process():
    ingredients_list = []
    ingredients_for_file = []
    preparation_list = []
    preparation_for_file = []
    for foldername in os.listdir("corpus"):
        for filename in os.listdir(f"corpus/{foldername}"):
            recipe = open(f"corpus/{foldername}/{filename}").read().split("\n")
            for line in recipe[4:]:
                set = line.split(",")
                if set[0] not in ingredients_list and len(set[0]) != 0:
                    ingredients_list.append(set[0])
                    string = set[0].strip() + ", " + set[0].strip().replace(" ", "_") + "\n"
                    ingredients_for_file.append(string)
                try:
                    if set[1] not in preparation_list and len(set[1]) != 0:
                        preparation_list.append(set[1])
                        string = set[1].strip() + ", " + set[1].strip().replace(" ", "_") + "\n"
                        preparation_for_file.append(string)
                except:
                    continue
    ingredients_file = open("tagger_dicts/ingredients_full.txt", "a")
    preparation_file = open("tagger_dicts/preparation_full.txt", "a")
    ingredients_for_file.sort()
    preparation_for_file.sort()
    for item in ingredients_for_file:
        ingredients_file.write(item)
    for item in preparation_for_file:
        preparation_file.write(item)
    ingredients_file.close()
    preparation_file.close()


def main():
    process()
main()
