import random
from preprocessing import allergen

class Recipe:
  def __init__(self, name, summary, ingredients):
    self.name = name
    self.summary = summary
    self.ingredients = ingredients
    
class Chef_Raimsey:
    
  def find_frequently_paired_ingredients():
    pass

  def find_frequently_paired_measurements():
    pass

  #Maanya
  def num_of_ingredients():
    number_of_ingredients = random.randint(6, 12)
    return number_of_ingredients

  def generate(user_favorite_food):
    # start generation process off of the user's favorite food
    pass

  def categorize(recipe):
    # BOW model 
    pass

  def name_recipe(recipe):
    pass

  #Maanya
  def conversation_starter():
    name = input("Hi. This is Chef Raimsey! And what is your name? ")
    favorite_ingredient = input("Oh Great! Hi ", name, ". What is your favorite ingredient in a dessert ")
    allergic = input(favorite_ingredient.upper(), "! Yummy!! And do you have any allergies that I should be aware of (Y/N)? ")
    while allergic != "Y" and allergic != "N":
        allergic = ("I need a Yes or No response (Y/N). ")
    if allergic == "Y":
        allergen = input("Oh no! I will generate a recipe for you that takes the allergy into account. So what is it that you are allergic to? Here is a list of possible options to help you out. Choose one. ")
        allergens_dict = allergen()
        list_of_allergens = allergens_dict.keys()
        for idx in range(len(list_of_allergens)):
            print(idx, element)
    else:
        print("Ok cool. We can move on then!")

  def main():
    pass
  
  main()

  