import random
import preprocessing
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import numpy as np
from scipy import spatial
#from InferKit.InferMain import InferKit

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
  def __init__(self,test=False):
    self.recipe_list, self.ingredients, self.amount, self.unit, self.prep = preprocessing.preprocess(test=test)

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
  def generate(self, user_favorite_food):
    '''
    Uses user's favorite ingredient or food to initiate the recipe generation process.

    Args:
      user_favorite_food: user-specied favorite food/ingredient
    Returns:
      A recipe object
    '''
    # start generation process off of the user's favorite food
    new_recipe = preprocessing.Recipe(name="",summary="",ingredients=[],recipe_type="")
    
    #get user favorite ingredient amount, then append to ingredient list
    fav_ingredient_amount = self.find_frequently_used_amount(user_favorite_food)
    fav_ingredient_unit = self.find_frequently_used_unit(user_favorite_food)
    fav_ingredient_prep = self.find_frequently_used_prep(user_favorite_food)
    new_recipe.ingredients.append([fav_ingredient_amount,fav_ingredient_unit,fav_ingredient_prep,user_favorite_food]) # this should be a len 4 list
    
    #start a for loop to add all the other ingredient
    last_ingredient = user_favorite_food
    for i in range(self.num_of_ingredients()):
      next_ingredient = self.find_frequently_paired_ingredient(last_ingredient)
      next_amount = self.find_frequently_used_amount(next_ingredient)
      next_ingredient_unit = self.find_frequently_used_unit(next_ingredient)
      next_ingredient_prep = self.find_frequently_used_prep(next_ingredient)
      new_recipe.ingredients.append([next_amount,next_ingredient_unit,next_ingredient_prep,next_ingredient]) # this should be a len 4 list
      last_ingredient = next_ingredient
    print(new_recipe.ingredients)
    new_recipe.name = self.name_recipe(new_recipe)
    print(new_recipe.name)
    # new_recipe.recipe_type = self.categorize(new_recipe)
    # new_recipe.summary = self.create_summary(new_recipe)
    
    return new_recipe

  #Sue
  def categorize(self, recipe):
    '''
    Once the recipe is generated by Chef Raimsey, use BOW/LSA/Doc2Vec to find which category of desserts the generated recipe resembles the most, and assign the recipe that type

    Args:
      recipe: generated Recipe object
    Returns:
      Category name
    '''
    model_data = open("doc2vec_model.txt", "rb")
    vector = model.infer_vector(recipe.processed_summary)
    similarities = {} # dictionary of similarity and type
    for summary in model_data:
      similarity = 1 - spatial.distance.cosine(summary[1], vector)
      similarities[similarity] = summary[0]
    similarity_keys = similarities.keys()
    sorted_keys = sorted(similarity_items, reverse = True)
    type_similarity = {}
    type_similarity["Cakes"] = 0
    type_similarity["Cobblers"] = 0
    type_similarity["Cokkies"] = 0
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
    '''
    name_list = []
    # name_list[0] = ingredient and/or non-allergen

    if recipe.recipe_type == "Frozen desserts":
      name_list.insert(0, "Frozen")
      name_list.append("Dessert")
    else:
      name_list.append(recipe.recipe_type[:-1])
    
    name = " ".join(name_list)
    save_file = open(f"newly_generated_recipe/{recipe.recipe_type}/{name}.txt", "x")

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
    text = "This recipe includes %s and %s," % (recipe.ingredients[0], recipe.ingredients[1])
    response = inferKit.generate(text, length=40)
    return response

  #Maanya (completed)
  #accounts for multiple allergies
  def conversation_starter(self):
    '''
    First few words of the greatest dessert Chef ever.
    '''
    name = input("Hi. This is Chef Raimsey! And what is your name? ")
    print("Oh Great! Hi", name, ". ")
    favorite_ingredient = input("What is your favorite ingredient in a dessert? ")
    print(favorite_ingredient.capitalize(), "! Yummy, good choice!!")
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
          allergies_list = allergens_dict[list_of_allergens[choice]]
          allergies_list = [s.strip() for s in allergies_list]
          for i in range(len(allergies_list)):
              print(i, ") ", allergies_list[i])
          final_allergy = input("Which of these are you allergic to? Enter the specific ingredient as shown in the list above: ")
          while final_allergy.capitalize() not in allergies_list:
              final_allergy = input("The instructions asked you to enter the specific ingredient as shown in the list above. Try again: ")
          ingredients_allergens = []
          print("Okay, thanks for sharing.", final_allergy.capitalize(), "will not be part of the recipe I generate for your dessert!")
          ingredients_allergens.append(final_allergy)
          more_allergies = input("Do you have any more allergies I should know about? (Y/N) ")
          while more_allergies.upper() != "Y" and more_allergies.upper() != "N":
            more_allergies = input("I need a Yes or No response (Y/N). ")
          if more_allergies.upper() == "N":
            allergies = False
            print("Alright, cool. We can move on then!")
    else:
        print("Alright, cool. We can move on then!")
        
#Maanya
def main():
  '''
  Method to get the Chef working!
  '''
  chef = Chef_Raimsey(test=True)
  # chef.conversation_starter()
  chef.generate("blueberries")
  
if __name__ == "__main__":
  main()
  