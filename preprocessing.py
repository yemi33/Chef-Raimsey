from nltk.tag import UnigramTagger
from nltk.corpus import treebank
import os
import re
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import numpy as np

'''
pip install numpy
pip install gensim
pip install python-Levenshtein
'''

class Recipe: #moved here because circular import error
  '''
  Class that represents a Recipe object.
  '''
  def __init__(self, name, summary, ingredients, recipe_type=None):
    '''
    Constructor
    Args:
      name: name of the recipe
      summary: summary of the recipe
      ingredients: list of lists (each sublist looks like: [CD] [UNIT] [PREP] [ING])
      recipe_type: type of the recipe (cookies, cakes, etc)
    '''
    self.name = name
    self.summary = summary
    self.ingredients = ingredients
    self.recipe_type = recipe_type
  
  def __repr__(self):
    return f'''
    Name: {self.name}
    Type: {self.recipe_type}
    Summary: {self.summary}
    Ingredients: {self.ingredients}
    '''

# Yemi  
def create_tag_dict():
    tag_dict = dict()

    f = open("tagger_dicts/cardinalities.txt", "r").read().strip().split("\n")
    for line in f:
        tag_dict[line.strip()] = "CD"
    
    f = open("tagger_dicts/ingredients.txt", "r").read().strip().split("\n")
    for line in f:
      try:
        split_string = line.split(",") # line looks like: chocolate syrup,chocolate_syrup
        tag_dict[split_string[1].strip()] = "ING"
      except:
        continue
    
    f = open("tagger_dicts/preparation.txt", "r").read().strip().split("\n")
    for line in f:
      try:
        split_string = line.split(",") # line looks like: chocolate syrup,chocolate_syrup
        tag_dict[split_string[1].strip()] = "PREP"
      except:
        continue
    
    f = open("tagger_dicts/unit.txt", "r").read().strip().split("\n")
    for line in f:
      try:
        split_string = line.split(",") # line looks like: chocolate syrup,chocolate_syrup
        tag_dict[split_string[1].strip()] = "UNIT"
      except:
        continue
    
    return tag_dict

# Yemi
def preprocess(test=False):
  # 1) we pos tag using nltk's Unigram tagger (customizable) 
  # train Unigram tagger with our tag_dictionary 
  tag_dict = create_tag_dict()
  tagger = UnigramTagger(model = tag_dict)
  dictionary_of_frequently_seen_together_ingredients = dict()
  dictionary_of_frequently_used_amount = dict()
  dictionary_of_frequently_prepared_method = dict()
  dictionary_of_frequently_used_unit = dict()
  list_of_recipes = list()
  
  corpus_folder_name = "corpus"

  if test:
    corpus_folder_name = "test_corpus"

  for foldername in os.listdir(corpus_folder_name):
    for filename in os.listdir(f"{corpus_folder_name}/{foldername}"):
      f = open(f"{corpus_folder_name}/{foldername}/{filename}").read().lower()
      f = f.replace(",","").strip() #butter, != butter
      # correct instances where it's like: brown sugar --> brown_sugar, so when tagging, this becomes a single word
      ingredient_list = open(f"tagger_dicts/ingredients.txt").read().split("\n")
      for ingr in ingredient_list:
        ingr_sublist = ingr.split(",") # line structure: brown sugar,brown_sugar
        # try replacing 
        try:
          f = f.replace(ingr_sublist[0].strip(),ingr_sublist[1].strip())
        # if error, just move onto the next potential replaceable ingredient
        except:
          continue
      
      # correct instances where it's like: room temperature --> room_temperature, so when tagging, this becomes a single word
      preparation_list = open(f"tagger_dicts/preparation.txt").read().split("\n")
      for prep in preparation_list:
        prep_sublist = prep.strip().split(",") # line structure: brown sugar,brown_sugar
        # try replacing 
        try:
          f = f.replace(prep_sublist[0].strip(),prep_sublist[1].strip())
        # if error, just move onto the next potential replaceable ingredient
        except:
          continue
      
      # after removing punctuations and replacing multi-words into single words
      # pos tag ingredient list and create a Recipe object
      f = f.split("\n")
      name = f[0]
      dessert_type = foldername
      summary = f[2]
      ingredients = f[4:]
      new_ingredients = []
      for ingr in ingredients:
        ingr = ingr.split(" ") # for some reason nltk punkt tokenizer doesn't work
        tagged_ingredient = tagger.tag(ingr)
        fixed_ingredient = resolve_ambiguity(tagged_ingredient)
        # print(fixed_ingredient)
        update_frequently_seen_used_amount(fixed_ingredient,dictionary_of_frequently_used_amount) 
        update_frequently_seen_used_unit(fixed_ingredient,dictionary_of_frequently_used_unit)
        update_frequently_prepared_method(fixed_ingredient, dictionary_of_frequently_prepared_method)
        new_ingredients.append(fixed_ingredient)
        update_frequently_seen_together_ingredients(new_ingredients, dictionary_of_frequently_seen_together_ingredients)
        recipe = Recipe(name=name, summary=summary, ingredients=new_ingredients, recipe_type=dessert_type)
        list_of_recipes.append(recipe)

  model = train_doc2vec(list_of_recipes)

  return list_of_recipes, dictionary_of_frequently_seen_together_ingredients, dictionary_of_frequently_used_amount, dictionary_of_frequently_used_unit, dictionary_of_frequently_prepared_method, model
    
# Yemi
def resolve_ambiguity(tagged_ingredient):
  #refer to Medium article
  ingr = ""
  cardinal = []
  unit = []
  prep = []

  for i in range(0,len(tagged_ingredient)):
    if tagged_ingredient[i][1] == "CD" or "\u2009" in tagged_ingredient[i][0]:
      cardinal.append(tagged_ingredient[i][0])
    elif tagged_ingredient[i][1] == "UNIT":
      unit.append(tagged_ingredient[i][0])
    elif tagged_ingredient[i][1] == "PREP":
      prep.append(tagged_ingredient[i][0])
    elif tagged_ingredient[i][1] == "ING" :
      ingr = tagged_ingredient[i][0]
  
  # key: unit->unit_to_translate_into / value: constant to multiply
  translate_unit = {
    "teaspoon-tablespoon" : 0.33,
    "teaspoon-ounce" : 0.16666672,
    "teaspoon-cup" : 0.0208,
    "teaspoon-pint" : 0.01041667,
    "teaspoon-quart" : 0.0052,
    "tablespoon-ounce" : 0.5,
    "tablespoon-cup" : 0.0625,
    "tablespoon-pint" : 0.03125,
    "tablespoon-quart" : 0.03125001125,
    "ounce-cup" : 0.1232227,
    "ounce-pint" : 0.0625000225,
    "ounce-quart" : 0.03125001125,
    "cup-pint" : 0.50000018,
    "cup-quart" : 0.25000009,
    "pint-quart" : 0.50000018
  }
  # do something with the lists 
  if len(unit) == 2:
    # retrieve the unit_translating key
    key = unit[0] + "-" + unit[1]
    # retrieve the constant 
    constant = translate_unit[key]
    # new cardinal is the first cardinal + second cardinal times the constant
    cardinal = cardinal[0] + cardinal[1] * constant
    # update the unit to just be the first one (which we are assuming is the larger one)
    unit = unit[0]
  elif len(unit) == 1:
    unit = unit[0]
    # if there's a single unit and multiple cardinals, average the cardinals
    if len(cardinal) > 1:
      cardinal = list(map(int, cardinal))
      sum_cardinal = sum(cardinal)
      avg = sum_cardinal / len(cardinal)
      # set the new cardinal to be the average of all the cardinals
      cardinal = avg
      # choose the unit as the first thing in the unit list
    elif len(cardinal) == 1:
      cardinal = cardinal[0]
    else:
      cardinal = ""
  else:
    unit = ""
    try:
      cardinal = cardinal[0]
    except:
      cardinal = ""
  if len(prep) > 0:
    prep = ", ".join(prep)
  else:
    prep = "" 

  refined_ingredient = [cardinal,unit,prep,ingr] # if no values for slot, it will be None
  # print(refined_ingredient)
  return refined_ingredient
      
# Yemi
def update_frequently_seen_together_ingredients(list_of_ingredients,dictionary_of_frequently_seen_together_ingredients):
  for ingr in list_of_ingredients:
    for ingr2 in list_of_ingredients:
      if ingr[3] == ingr2[3]:
        continue
      if ingr[3] == '' or ingr2[3] == '':
        continue
      try: # if there is already a key
        dictionary_of_frequently_seen_together_ingredients[ingr[3]].add(ingr2[3])
      except KeyError: # if there is no key, create one
        dictionary_of_frequently_seen_together_ingredients[ingr[3]] = set()
        dictionary_of_frequently_seen_together_ingredients[ingr[3]].add(ingr2[3])

# Yemi
def update_frequently_seen_used_amount(fixed_ingredients,dictionary_of_frequently_used_amount):
  ingr = fixed_ingredients[3]
  cardinal = fixed_ingredients[0]
  if cardinal != "":
    try:
      dictionary_of_frequently_used_amount[ingr].add(cardinal)
    except KeyError:
      dictionary_of_frequently_used_amount[ingr] = set()
      dictionary_of_frequently_used_amount[ingr].add(cardinal)

# Yemi
def update_frequently_seen_used_unit(fixed_ingredients,dictionary_of_frequently_used_unit):
  ingr = fixed_ingredients[3]
  unit = fixed_ingredients[1]
  if unit != "":
    try:
      dictionary_of_frequently_used_unit[ingr].add(unit)
    except KeyError:
      dictionary_of_frequently_used_unit[ingr] = set()
      dictionary_of_frequently_used_unit[ingr].add(unit)

# Yemi
def update_frequently_prepared_method(fixed_ingredients, dictionary_of_frequently_prepared_method):
  ingr = fixed_ingredients[3]
  prep = fixed_ingredients[2]
  if prep != "":
    try:
      dictionary_of_frequently_prepared_method[ingr].add(prep)
    except KeyError:
      dictionary_of_frequently_prepared_method[ingr] = set()
      dictionary_of_frequently_prepared_method[ingr].add(prep)

# Maanya
def allergen():
    allergens_dict = {}
    allergens_file = open("allergies/allergens.txt", "r")
    for line in allergens_file:
        if "->" in line:
            category, ingredients = line. split("->")
            ingredients_list = ingredients.split(",")
            allergens_dict[category] = ingredients_list
        else:
            continue
    return allergens_dict

# Sue
def create_ingredients_corpus(list_of_Recipes):
    '''
    ingredients: list of lists (each sublist looks like: [CD] [UNIT] [PREP] [ING])
    '''
    recipe_corpus = []
    recipe_type_list = []
    for recipe in list_of_Recipes:
        for sublist in recipe.ingredients:
            string = " ".join(sublist)
            recipe_corpus.append(string)
            recipe_type_list.append(recipe.recipe_type)
    return recipe_corpus, recipe_type_list

# Sue
def train_doc2vec(list_of_Recipes):
    # Up to change - choose one of BOW/LSA/Doc2Vec
    # I'll go with doc2vec for now, since it's more accurate than BOW and takes a shorter time to train
    '''
    Recipe Obejct:
    name: name of the recipe
    type: type of the recipe (cookies, cakes, etc)
    summary: summary of the recipe
    ingredients: list of lists (each sublist looks like: [CD] [UNIT] [PREP] [ING])
    '''
    recipe_corpus, recipe_type_list = create_ingredients_corpus(list_of_Recipes)
    documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(recipe_corpus)]
    model = Doc2Vec(documents, vector_size=100, window=5, min_count=1, workers=4)
    document_vectors = [model.dv[i] for i in range(len(documents))]
    model_export_data = []
    for i, document in enumerate(recipe_corpus):
        document_vector = document_vectors[i]
        document_topic = recipe_type_list[i]
        document_entry = (document_topic, document_vector)
        model_export_data.append(document_entry)
        # Convert to numpy array and save to file
    export_data = np.array(model_export_data, dtype=object)
    outfile = open("doc2vec_model.txt", "wb")
    np.save(outfile, export_data)
    outfile.close()
    return model

if __name__ == "__main__":  
  preprocess(test=True)