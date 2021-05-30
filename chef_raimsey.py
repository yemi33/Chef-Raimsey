import random
import preprocessing
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import numpy as np
from scipy import spatial
import sys
from InferKit.InferMain import InferKit
from nltk.tag import UnigramTagger
import nltk
from chef_raimsey_graphic import *
# nltk.download('punkt')

'''
pip install numpy
pip install scipy
pip install gensim
pip install python-Levenshtein
'''

class Chef_Raimsey:
  '''
  Class that represents a Chef Raimsey simulation.
  '''
  #Nicole
  def __init__(self,test=False, gui=True):
    self.recipe_list, self.ingredients, self.amount, self.unit, self.prep, self.model = preprocessing.preprocess(test=test)
    if gui:
      self.user_name, self.favorite_ingredient, self.list_of_allergies, self.main_allergen = conversation_starter_graphic()
    else:
      self.user_name, self.favorite_ingredient, self.list_of_allergies, self.main_allergen = self.conversation_starter()

  #Nicole
  def find_frequently_paired_ingredient(self, ingredient):
    '''
    Method to find a frequently paired ingredient with the one given.

    Args:
      ingredient: ingredient 
    Returns:
      a frequently paired ingredient 
    '''
    try:
      paired_ingredients = self.ingredients[ingredient]
      return random.choice(list(paired_ingredients))
    except:
      for key in self.ingredients.keys():
        if ingredient in key or key in ingredient:
          try:
            paired_ingredients = self.ingredients[key]
            return random.choice(list(paired_ingredients))
          except KeyError:
            return ""
      return ""

  #Nicole
  def find_frequently_used_amount(self, ingredient):
    '''
    Method to find a frequently used amount of the ingredient.

    Args:
      ingredient: ingredient
    Returns:
      amount that the ingredient is frequently used for.
    '''
    try:
      paired_amount = self.amount[ingredient]
      return random.choice(list(paired_amount))
    except:
      for key in self.ingredients.keys():
        if ingredient in key or key in ingredient:
          try:
            paired_amount = self.amount[key]
            return random.choice(list(paired_amount))
          except KeyError:
            return ""
      return ""
  
  #Yemi
  def find_frequently_used_unit(self, ingredient):
    '''
    Method to find a frequently used unit of the ingredient.

    Args:
      ingredient: ingredient
    Returns:
      unit that the ingredient frequently uses.
    '''
    try:
      paired_unit = self.unit[ingredient]
      return random.choice(list(paired_unit))
    except:
      for key in self.ingredients.keys():
        if ingredient in key or key in ingredient:
          try:
            paired_unit = self.unit[key]
            return random.choice(list(paired_unit))
          except KeyError:
            return ""
      return ""
  
  #Yemi
  def find_frequently_used_prep(self, ingredient):
    '''
    Method to find a frequently used prep of the ingredient.

    Args:
      ingredient: ingredient
    Returns:
      frequent prep methods of ingredient.
    '''
    try:
      paired_prep = self.prep[ingredient]
      return random.choice(list(paired_prep))
    except:
      for key in self.ingredients.keys():
        if ingredient in key or key in ingredient:
          try:
            paired_prep = self.prep[key]
            return random.choice(list(paired_prep))
          except KeyError:
            return ""
      return ""

  #Maanya
  def num_of_ingredients(self):
    '''
    Method to get the number of ingredients
    '''
    number_of_ingredients = random.randint(6, 12)
    return number_of_ingredients

  #Nicole - recipe ingredient list generation complete
  def generate(self):
    '''
    Uses user's favorite ingredient or food to initiate the recipe generation process.

    Args:
      user_favorite_food: user-specied favorite food/ingredient
    Returns:
      A recipe object
    '''
    user_favorite_food = self.favorite_ingredient
    # start generation process off of the user's favorite food
    new_recipe = preprocessing.Recipe(name="",summary="",ingredients=[],recipe_type="")
    #get user favorite ingredient amount, then append to ingredient list
    fav_ingredient_amount = self.find_frequently_used_amount(user_favorite_food)
    fav_ingredient_unit = self.find_frequently_used_unit(user_favorite_food)
    fav_ingredient_prep = self.find_frequently_used_prep(user_favorite_food)
    new_recipe.ingredients.append([fav_ingredient_amount,fav_ingredient_unit,fav_ingredient_prep,user_favorite_food]) # this should be a len 4 list
    added_ingredients = [] #list to keep track of already added ingredients, so we can avoid repeats
    #start a for loop to add all the other ingredient
    last_ingredient = user_favorite_food
    for i in range(self.num_of_ingredients()):
      next_ingredient = self.find_frequently_paired_ingredient(last_ingredient)
      next_amount = self.find_frequently_used_amount(next_ingredient)
      next_ingredient_unit = self.find_frequently_used_unit(next_ingredient)
      next_ingredient_prep = self.find_frequently_used_prep(next_ingredient)
      while next_ingredient in self.list_of_allergies or next_ingredient in added_ingredients: #don't want allergens to be included in the recipe object
        next_ingredient = self.find_frequently_paired_ingredient(last_ingredient)
        next_amount = self.find_frequently_used_amount(next_ingredient)
        next_ingredient_unit = self.find_frequently_used_unit(next_ingredient)
        next_ingredient_prep = self.find_frequently_used_prep(next_ingredient)
      added_ingredients.append(next_ingredient)
      new_recipe.ingredients.append([next_amount,next_ingredient_unit,next_ingredient_prep,next_ingredient])
      last_ingredient = next_ingredient
    # print(new_recipe.ingredients)

    new_recipe.recipe_type = self.categorize(new_recipe).strip()
    new_recipe.name = self.name_recipe(new_recipe).strip()
    new_recipe.summary = self.create_summary(new_recipe).strip()
    print(self.format_recipe(new_recipe))
    self.add_new_recipe(new_recipe)
    return new_recipe
  
  def add_new_recipe(self,recipe):
      save_file = open(f"newly_generated_recipe/{recipe.recipe_type}/{recipe.name}.txt", "a")
      save_file.write(self.format_recipe(recipe))
      save_file.close()

#Maanya
  def format_recipe(self,recipe):
    '''
    Output: 
    
    Strawberry Cobbler I

    Serve with cream or ice cream. 

    ½ cup white sugar 
    1 tablespoon cornstarch 
    1 cup water 
    3 cups strawberries, hulled 
    2 tablespoons butter, diced 
    1 cup all-purpose flour 
    1 tablespoon white sugar 
    1 ½ teaspoons baking powder 
    ½ teaspoon salt 
    3 tablespoons butter 
    ½ cup heavy whipping cream 
    '''
    final_ingredients = []
    for i in recipe.ingredients:
      ingredient_string = ""
      if i[0] == "" and i[1] == "" and i[3] != "":
          i[0] = "1"
          i[1] = "cup"
      if "\u2009" in i[0]:
          i[0] = i[0].replace("\u2009", " and ")
      try:
        if i[1][-1] == 's':
          try:
              i[1] = i[1][:len(i[1])-1]
          except:
            pass
      except:
        pass
      if "_" in i[2] or "_" in i[3]:
          if "_" in i[2]:
              i[2] = i[2].replace("_", " ")
          if "_" in i[3]:
              i[3] = i[3].replace("_", " ")
      if "(" in i[3]:
          i[3].replace("(", "")
          i[3].replace(")", "")
      ingredient_string = " ".join(i)
      final_ingredients.append(ingredient_string)

    final_ingredients_string = "\n".join(final_ingredients)
    final_ingredients_string.replace("\n\n", "\n")
    generated_recipe = recipe.name + "\n\n" + recipe.summary + "\n\n" + final_ingredients_string
    return generated_recipe
  
  # Sue
  def create_ingredients_corpus(self, recipe):
    '''
    ingredients: list of lists (each sublist looks like: [CD] [UNIT] [PREP] [ING])
    '''
    recipe_corpus = []
    for sublist in recipe.ingredients:
        string = " ".join(sublist)
        recipe_corpus.append(string)
    return recipe_corpus

  #Sue
  def categorize(self, recipe):
    '''
    Once the recipe is generated by Chef Raimsey, use BOW/LSA/Doc2Vec to find which category of desserts the generated recipe resembles the most, and assign the recipe that type

    Args:
      recipe: generated Recipe object
    Returns:
      Category name
    '''
    #model_data = open("doc2vec_model.txt", "rb")
    model_data = np.load(open("doc2vec_model.txt", 'rb'), allow_pickle=True)
    vector = self.model.infer_vector(self.create_ingredients_corpus(recipe))
    similarities = {} # dictionary of similarity and type
    for summary in model_data:
      similarity = 1 - spatial.distance.cosine(summary[1], vector)
      similarities[similarity] = summary[0]
    similarity_keys = similarities.keys()
    sorted_keys = sorted(similarity_keys, reverse = True)
    type_similarity = {}
    type_similarity["Cakes"] = 0
    type_similarity["Cobblers"] = 0
    type_similarity["Cookies"] = 0
    type_similarity["Frozen desserts"] = 0
    type_similarity["Pies"] = 0
    '''
    To categorize the recipe, we sum up the similarities under each type and find the type with the highest similarity
    '''
    for item in sorted_keys:
      if similarities[item] == "Cakes":
        type_similarity["Cakes"] += item
      elif similarities[item] == "Cobblers":
        type_similarity["Cobblers"] += item
      elif similarities[item] == "Cookies":
        type_similarity["Cookies"] += item
      elif similarities[item] == "Frozen desserts":
        type_similarity["Frozen desserts"] += item
      else:
        type_similarity["Pies"] += item
    sorted_similarity = sorted(type_similarity.items(), reverse = True, key=lambda item: item[1])
    category = sorted_similarity[0][0]

    return category # a string of the category

  #Sue
  def name_recipe(self, recipe):
    '''
    Once the recipe is categorized, name the recipe using the recipe type + some other information (such as "main" ingredient and/or non-allergen)

    Args:
      recipe: generated Recipe object 
    Returns:
      name of the recipe
      creates file in its corresponding type folder under the newly_generated_recipe folder (e.g. "newly_generated_recipe/Cookies/recipe_name.txt")

      self.favorite_ingredient, self.list_of_allergies
    '''
    name_list = []

    if len(self.list_of_allergies) > 0:
      random_choice = random.choice(self.list_of_allergies)
      if random_choice.lower().strip() == "all of the above":
        random_choice = self.main_allergen
      random_choice.replace("_", "-")
      string = "Non-" + random_choice.title()
      name_list.append(string)

    name_list.append(self.favorite_ingredient.replace("_", "-").title())
    if recipe.recipe_type == "Frozen desserts":
      if name_list[0][:3] == "Non-":
        name_list.insert(1, "Frozen")
      else:
        name_list.insert(0, "Frozen")
      name_list.append("Dessert")
    else:
      name_list.append(recipe.recipe_type[:-1])
    
    name = self.user_name + "'s " + " ".join(name_list)
    return name

  #Nicole
  def create_summary(self, recipe):
    '''
    Once the recipe is named and categorized, generate a recipe summary
    options: 
    1. CFG for each category, sub in recipe ingredients
    2. choose a summary from self.summaries in same category
    -- tag to find ingredients
    -- replace ingredient with new recipe ingredients
    3. hybrid marcovModel-esque
    -- generate sentence from summaries using marcov (or RNN?)
    -- tag to find ingredients
    -- replace with recipe ingredients
    4. Use InferKit (GPT-2) for python (located in InferKit folder)
    -- issue: API doesn't allow for keywords

    Args:
      recipe: generated Recipe object 
    Returns:
      summary of the recipe
    '''
    inferKit = InferKit(api_key='48016474-4a28-48d4-a3e2-b104d4f07451')
    ingr1 = recipe.ingredients[0][3].replace("_", " ")
    ingr2 = recipe.ingredients[1][3].replace("_", " ")
    category = recipe.recipe_type[:-1].lower()
    text = "This tasty %s uses %s and %s," % (category, ingr1, ingr2)
    summary = inferKit.generate(text, length=80)
    #replace ingredients not in recipe with ones that are
    tag_dict = preprocessing.create_tag_dict()
    tagger = UnigramTagger(model = tag_dict)
    # summary_tokens = nltk.word_tokenize(summary)
    summary_tokens = summary.split(" ")
    tagged_tokens = tagger.tag(summary_tokens)
    needs_new_ingredient = []
    ingredients = []
    for line in recipe.ingredients:
      ingredients.append(line[3])
    for token in tagged_tokens:
      if token[1] == "ING":
        if token[0] not in ingredients:
          needs_new_ingredient.append(token[0])
    for ingr in needs_new_ingredient:
      try: #try and except in case the same ingredients appears more than once
        summary.replace(ingr, random.choice(ingredients))
      except:
        pass
    summary = text + " " + summary
    index_sent_period, index_sent_exclaim, index_sent_question, index_sent_comma = 0, 0, 0, 0
    if summary.count(".") > 0:
        index_sent_period = summary.rindex(".")
    if summary.count("!") > 0:
        index_sent_exclaim = summary.rindex("!")
    if summary.count("?") > 0:
        index_sent_question = summary.rindex("?")
    if summary.count(",") > 0:
        index_sent_comma = summary.rindex(",")
    index_sent = max(index_sent_period, index_sent_exclaim, index_sent_question, index_sent_comma)
    if index_sent == index_sent_comma:
        index_sent = index_sent - 1
    if index_sent > 0:
        summary = summary[:index_sent+1]
    summary.replace("\n", " ")
    summary.replace("\n\n", " ")
    summary.replace("  ", " ")
    if summary[len(summary)-1] != "." or summary[len(summary)-1] != "!" or summary[len(summary)-1] != ",":
        index = summary.rindex(" ")
        summary = summary[:index]
    return summary

  #Maanya (completed)
  #accounts for multiple allergies
  def conversation_starter(self):
    '''
    First few words of the greatest dessert Chef ever.
    '''
    ingredients_allergens = []
    main_allergen = ""
    name = input("Hi. This is Chef Raimsey! And what is your name? ").capitalize()
    print("Oh Great! Hi", name, ". ")
    favorite_ingredient = input("What is your favorite ingredient in a dessert? ").lower()
    print(favorite_ingredient.capitalize(), "! Yummy, good choice!!")
    if favorite_ingredient not in self.ingredients.keys():
        print("Sorry, we don't have your ingredient in our recipe shelf but let's see what we can concoct for you! ")
        favorite_ingredient = random.choice(list(self.ingredients.keys()))
    allergic = input("And do you have any allergies that I should be aware of (Y/N)? ")
    while allergic.upper() != "Y" and allergic.upper() != "N":
        allergic = input("I need a Yes or No response (Y/N). ")
    if allergic.upper() == "Y":
        allergies = True
        while allergies:
          print("Oh no! I will generate a recipe for you that takes the allergy into account. So what is it that you are allergic to? Here is a list of possible options to help you out: ")
          allergens_dict = preprocessing.allergen()
          list_of_allergens = list(allergens_dict.keys())
          mapping = {}
          for idx in range(len(list_of_allergens)):
              mapping[idx] = list_of_allergens[idx]
              print(idx, ") ", list_of_allergens[idx])
          choice = input("Which of the above are you allergic to? Enter the corresponding numbers. So if you are allergic to dairy, choose 0: ")
          while choice.isnumeric() == False or int(choice) < 0 or int(choice) > 4:
              print("The instructions say that you need to input integers between 0 and 4.")
              choice = input("Which of the above are you allergic to? Enter the corresponding numbers. So if you are allergic to dairy, choose 0: ")
          choice = int(choice)
          allergy = mapping[choice]
          print("Ok noted! So you are allergic to", allergy,".")
          main_allergen = allergy
          allergies_list = allergens_dict[list_of_allergens[choice]]
          allergies_list = [s.strip().lower() for s in allergies_list]
          for i in range(len(allergies_list)):
              print(i, ") ", allergies_list[i])
          final_allergy = input("Which of these are you allergic to? Enter the specific ingredient as shown in the list above: ").lower()
          while final_allergy.capitalize() not in allergies_list and final_allergy not in allergies_list and final_allergy.strip() not in allergies_list:
              final_allergy = input("The instructions asked you to enter the specific ingredient as shown in the list above. Try again: ")
          print("Okay, thanks for sharing.", final_allergy.capitalize(), "will not be part of the recipe I generate for your dessert!")
          if final_allergy.capitalize() == "All of the Above" or final_allergy == "All of the Above" or final_allergy.strip() == "All of the Above":
              for k in range(len(allergies_list)-1):
                  ingredients_allergens.append(allergies_list[k].lower())
          else:
              ingredients_allergens.append(final_allergy.lower())
          more_allergies = input("Do you have any more allergies I should know about? (Y/N) ")
          while more_allergies.upper() != "Y" and more_allergies.upper() != "N":
            more_allergies = input("I need a Yes or No response (Y/N). ")
          if more_allergies.upper() == "N":
            allergies = False
            print("Alright, cool. We can move on then!")
    else:
        print("Alright, cool. We can move on then!")
    return name, favorite_ingredient, ingredients_allergens, main_allergen

#Maanya
def main():
  '''
  Method to get the Chef working!
  '''
  chef = Chef_Raimsey(gui=True)
  print("\n")
  print(f"Here is dessert recipe custom made for {chef.user_name}! \n")
  recipe = chef.generate()

  # Sue's test
  # recipe = preprocessing.Recipe(name="",summary="",ingredients=["1 (18.25 ounce) package yellow cake mix"],recipe_type="")
  # name = chef.name_recipe(recipe)
  # category = chef.categorize(recipe)
  # print(name)
  # print(category)
  
if __name__ == "__main__":
  main()
  