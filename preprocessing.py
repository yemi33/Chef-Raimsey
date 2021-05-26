# Yemi
def preprocess():
  # 1) we pos tag using nltk's Unigram tagger (customizable) 
  
  # 1-1) resolve ambiguity in ingredient description 

  # 2) create Recipe objects (name,summary, list of ingredients)

  # 3) we also create a dictionary of frequently seen-together ingredients 
  # where key: ingredient, value: list of ingredients that appeared together

  # 4) we also create a dictionary of frequently seen-together measurements and ingredients
  # where key: ingredient, value: a list of measurements for this ingredient

  # 5) 

  # output: 
  # 1) list of Recipe Objects 
  # 2) dictionary of ingredients 
  # 3) dictionary of measurements 
  
def resolve_ambiguity():
  # refer to Medium article

#Maanya Goenka
def allergen():
    allergens_dict = {}
    allergens_file = open("allergies/allergens.txt", "r")
    for line in allergens_file:
        if "->" in line:
            category, ingredients = line. split("->")
            ingredients_list = ingredients.split(",")
            allergens_dict[category] = ingredients_list
    return allergens_dict