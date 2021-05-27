from nltk.tag import UnigramTagger
from nltk.corpus import treebank
import os
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
      ingredients: list of tuples (ingredient, amount)
      recipe_type: type of the recipe (cookies, cakes, etc)
    '''
    self.name = name
    self.summary = summary
    self.ingredients = ingredients
    self.recipe_type = recipe_type
  
  def __repr__(self):
    return f'''
    {self.name}
    {self.recipe_type}
    {self.summary}
    {self.ingredients}
    '''

# Yemi  
def create_tag_dict():
    tag_dict = dict()

    f = open("tagger_dicts/cardinalities.txt", "r")
    for line in f:
        tag_dict[line.strip()] = "CD"
    
    f = open("tagger_dicts/ingredients.txt", "r")
    for line in f:
        split_string = line.split(",") # line looks like: chocolate syrup,chocolate_syrup
        tag_dict[split_string[1].strip()] = "ING"
    
    f = open("tagger_dicts/preparation.txt", "r")
    for line in f:
        tag_dict[line.strip()] = "PREP"
    
    f = open("tagger_dicts/unit.txt", "r")
    for line in f:
        split_string = line.split(",") # line looks like: chocolate syrup,chocolate_syrup
        tag_dict[split_string[1].strip()] = "UNIT"
    
    return tag_dict

# Yemi
def preprocess():
    # 1) we pos tag using nltk's Unigram tagger (customizable) 
    # train Unigram tagger with our tag_dictionary 
    tag_dict = create_tag_dict()
    tagger = UnigramTagger(model = tag_dict)
    dictionary_of_frequently_seen_together_ingredients = dict()
    dictionary_of_frequently_used_amount = dict()
    list_of_recipes = list()
    
    for foldername in os.listdir("corpus"):
      for filename in os.listdir(f"corpus/{foldername}"):
        f = open(f"corpus/{foldername}/{filename}").read().split("\n")
        name = f[0]
        dessert_type = foldername
        summary = f[2]
        ingredients = "\n".join(f[4:])
        tagged_name = tagger.tag(name)
        tagged_summary = tagger.tag(summary)
        tagged_ingredients = tagger.tag(ingredients)
        print(tagged_ingredients)
        # 1-1) resolve ambiguity in ingredient description 
    #     fixed_ingredients = resolve_ambiguity(tagged_ingredients)

    #     # 3) we also create a dictionary of frequently seen-together ingredients 
    #     # where key: ingredient, value: list of ingredients that appeared together
    #     find_frequently_seen_together_ingredients(fixed_ingredients, dictionary_of_frequently_seen_together_ingredients)
    #     # 4) we also create a dictionary of frequently seen-together measurements and ingredients
    #     # where key: ingredient, value: a list of measurements for this ingredient
    #     find_frequently_seen_used_amount(fixed_ingredients,dictionary_of_frequently_used_amount)

    #     # 2) create Recipe objects and a list of recipe summaries (name,summary, list of ingredients)
    #     recipe = Recipe(name=name, summary=summary, ingredients=fixed_ingredients, recipe_type=dessert_type)
    #     list_of_recipes.append(recipe)

    # # output: 
    # # 1) list of Recipe Objects 
    # # 2) dictionary of ingredients 
    # # 3) dictionary of measurements
    # return list_of_recipes, dictionary_of_frequently_seen_together_ingredients,dictionary_of_frequently_used_amount
    

# Yemi
def resolve_ambiguity(tagged_ingredients):
    #refer to Medium article
    '''
    [cardinal] [unit] [potentially preparation] [ingredient]. 

    Some examples of nonstandard lines were:
      2 cups plus 2 tablespoons sugar. This is of the form [cardinal] [unit] [none] [cardinal] [unit] [ingredient], and was resolved by converting the second cardinal and unit into the first unit, and adding: 2.125 cups sugar.

      1 cup butterscotch or peanut butter chips. This is of the form [cardinal] [unit] [ingredient] [none] [ingredient]. One difficulty here is that the second ingredient is actually describing both ingredients: they mean butterscotch chips or peanut butter chips. This was resolved by choosing the second ingredient, rather than the first.

      1 to 2 tablespoons oil. This is of the form [cardinal] [none] [cardinal] [unit] [ingredient], and was resolved by averaging the two cardinals.
    
    find a cardinal
    see if the next thing is a unit
    if yes, 
      check if the next thing is a ingredient
        if yes,
          cut off the list here 
        else if the next thing is a none,
          check if the next thing is a cardinal,
            if yes, 
              use a dictionary to add the first cardinal to the second cardinal,
              and replace original list to [added_cardinal] [unit] [ingredient]
      else if the next thing is prep,
        check if the next thing is an ingredient, 
          if yes, 
            cut off the list here 
    else if the next thing is none,
      check if the next thing is cardinal,
        if yes, 
          average the first cardinal to the second cardinal 
          and replace original list to [averaged_cardinal] [unit] [ingredient]

    '''
    
    pass

# Yemi
def find_frequently_seen_together_ingredients(fixed_ingredients,dictionary_of_frequently_seen_together_ingredients):
  pass

# Yemi
def find_frequently_seen_used_amount(fixed_ingredients,dictionary_of_frequently_used_amount):
  pass


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
def process_ingredients():
    pass

# Sue
def train_doc2vec(list_of_Recipes):
    # Up to change - choose one of BOW/LSA/Doc2Vec
    # I'll go with doc2vec for now, since it's more accurate than BOW and takes a shorter time to train
    '''
    Recipe Obejct:
    name: name of the recipe
    type: type of the recipe (cookies, cakes, etc)
    summary: summary of the recipe
    ingredients: list of tuples (ingredient, amount)
    '''
    documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(list_of_Recipes).ingredients]
    model = Doc2Vec(documents, vector_size=100, window=5, min_count=1, workers=4)
    document_vectors = [model.dv[i] for i in range(len(documents))]
    model_export_data = []
    for i, document in enumerate(list_of_Recipes):
        document_vector = document_vectors[i]
        document_topic = list_of_Recipes[i].recipe_type
        document_entry = (document_topic, document_vector)
        model_export_data.append(document_entry)
        # Convert to numpy array and save to file
    export_data = np.array(model_export_data)
    outfile = open("doc2vec_model.txt", "wb")
    np.save(outfile, export_data)
    outfile.close()

if __name__ == "__main__":  
  preprocess()