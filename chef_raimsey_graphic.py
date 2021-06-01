from graphics import *
import random 
import preprocessing

# for GUI button
def inside(point, rectangle):
  """ Is point inside rectangle? """

  ll = rectangle.getP1()  # assume p1 is ll (lower left)
  ur = rectangle.getP2()  # assume p2 is ur (upper right)

  return ll.getX() < point.getX() < ur.getX() and ll.getY() < point.getY() < ur.getY()

class Chef_Raimsey_Graphic:
  def __init__(self, ingredients_dict):
    self.ingredients_dict = ingredients_dict
    self.window = GraphWin("Chef Raimsey", 600, 800)
    self.window.setCoords(0,0,30,40)
    self.image = Image(Point(15,32), "ramsay.gif")
    self.message = Text(Point(15, 22),"Hi. This is Chef Raimsey! And what is your name? ")
    self.message.setSize(20)
    self.entry = Entry(Point(15, 5), 15)
    self.entry.setSize(20)
    self.entry.setFill(color_rgb(247,247,222))
    self.guide = Text(Point(15,2), "Hit Enter to move on.")
    self.guide.setTextColor('red')
    self.reply = Text(Point(15, 8), "")
    self.reply.setSize(20)

  def conversation_starter_graphic(self):
    '''
    First few words of the greatest dessert Chef ever.
    '''
    name = ""
    favorite_ingredient = ""
    ingredients_allergens = []
    main_allergen = []
    
    # Initialize self.window and various graphical elements
    self.image.draw(self.window)
    self.message.draw(self.window)
    self.entry.draw(self.window)
    self.guide.draw(self.window)
    self.reply.draw(self.window)

    # Get user name
    while self.window.getKey() != "Return":
      name = self.entry.getText().capitalize()
    name = self.entry.getText().capitalize()
    self.entry.undraw()

    # self.reply to user name
    self.message.setText("")
    self.reply.setText(f"Oh Great! Hi {name}.")
    
    # Transition
    while self.window.getKey() != "Return":
      self.reply.setSize(20) 
    self.reply.setText("")

    # Ask for user favorite ingredient
    self.message.setText("What is your favorite ingredient in a dessert? ")
    self.entry.setText("")
    self.entry.draw(self.window)

    while self.window.getKey() != "Return":
      favorite_ingredient = self.entry.getText().capitalize()
    favorite_ingredient = self.entry.getText().lower()
    self.entry.undraw()
    self.message.setText("")

    # Check if user favorite ingredient in ingredients dict
    if favorite_ingredient in list(self.ingredients_dict.keys()):
      self.reply.setText(f"{favorite_ingredient.capitalize()}! Yummy, good choice!!")
      while self.window.getKey() != "Return":
        self.reply.setSize(20)
    else:
      res = [key for key in self.ingredients_dict.keys() if favorite_ingredient in key]
      if len(res) == 0:
          self.reply.setText("Sorry, we don't have your ingredient in our recipe shelf \nbut let's see what we can concoct for you! ")
          favorite_ingredient = random.choice(list(self.ingredients_dict.keys()))
          while self.window.getKey() != "Return":
            self.reply.setSize(20)
      else:
        self.reply.setText(f"{favorite_ingredient.capitalize()}! Yummy, good choice!!")
        while self.window.getKey() != "Return":
          self.reply.setSize(20)
        favorite_ingredient = res[0]
    self.reply.setText("")

    # Check for user allergies
    self.message.setText("And do you have any allergies that I should be aware of (Y/N)? ")
    self.guide.undraw()
    
    button_yes = Rectangle(Point(9,5),Point(12,7))
    button_yes_text = Text(button_yes.getCenter(),"Yes")
    button_no = Rectangle(Point(18,5),Point(21,7))
    button_no_text = Text(button_no.getCenter(),"No")

    button_yes.draw(self.window)
    button_yes_text.draw(self.window)
    button_no.draw(self.window)
    button_no_text.draw(self.window)

    allergic = False
    while True:
      clickPoint = self.window.getMouse()
      if inside(clickPoint,button_yes):
        allergic = True
        break
      elif inside(clickPoint,button_no):
        break
    
    button_yes.undraw()
    button_yes_text.undraw()
    button_no.undraw()
    button_no_text.undraw()

    self.guide.draw(self.window)
    if allergic:
        allergies = True
        while allergies:
          self.message.setText("Oh no! I will generate a recipe for you that takes the allergy into account.\nSo what is it that you are allergic to? \nHere is a list of possible options to help you out: ")
          allergens_dict = preprocessing.allergen()
          list_of_allergens = list(allergens_dict.keys())
          mapping = {}
          options = []
          for idx in range(len(list_of_allergens)):
              mapping[idx] = list_of_allergens[idx]
              option = Text(Point(15, (18 - idx * 1)),f"{idx}) {list_of_allergens[idx]}")
              option.setSize(16)
              option.draw(self.window)
              options.append(option)
          self.message.setText("Which of the above are you allergic to? \nEnter the corresponding numbers. \nSo if you are allergic to dairy, choose 0: ")
          self.entry.setText("")
          choice = ""
          self.entry.draw(self.window)
          while self.window.getKey() != "Return":
            choice = self.entry.getText().capitalize()
          choice = self.entry.getText().capitalize()

          self.reply.setText("The instructions say that you need \nto input integers between 0 and 4.")
          while choice.isnumeric() == False or int(choice) < 0 or int(choice) > 4:
              self.entry.setText("")
              while self.window.getKey() != "Return":
                choice = self.entry.getText().capitalize()
              choice = self.entry.getText().capitalize()
          
          self.reply.setText("")
          for option in options:
            option.undraw()

          choice = int(choice)
          allergy = mapping[choice]
          self.reply.setText(f"Ok noted! So you are allergic to {allergy}.")
          main_allergen.append(allergy.strip())
          allergies_list = allergens_dict[list_of_allergens[choice]]
          allergies_list = [s.strip().lower() for s in allergies_list]

          options = []

          y = 0
          renewed = False
          for i in range(len(allergies_list)):
              x = 10
              if i > len(allergies_list)/2:
                x = 20
                if not renewed:
                  renewed = True
                  y = 0
              option = Text(Point(x, (18 - y * 1)),f"{i}) {allergies_list[i]}")
              option.setSize(16)
              option.draw(self.window)
              options.append(option)
              y += 1
          self.reply.setText("")
          
          self.message.setText("Which of these are you allergic to? \nEnter the specific ingredient as shown in the list above: ")
          self.entry.setText("")
          final_allergy = ""
          while self.window.getKey() != "Return":
              final_allergy = self.entry.getText()
          final_allergy = self.entry.getText()

          while final_allergy.capitalize() not in allergies_list and final_allergy not in allergies_list and final_allergy.strip() not in allergies_list:
              self.reply.setText("The instructions asked you to enter the \nspecific ingredient as shown in the list above. \nTry again:")
              self.entry.setText("")
              while self.window.getKey() != "Return":
                final_allergy = self.entry.getText()
              final_allergy = self.entry.getText()

          self.reply.setText("")
          for option in options:
            option.undraw()
          self.entry.undraw()
          self.message.setText("")

          if final_allergy.lower() == "all of the above" or final_allergy.strip() == "All of the Above":
              for k in range(len(allergies_list)-1):
                  ingredients_allergens.append(allergies_list[k].lower())
          else:
              ingredients_allergens.append(final_allergy.lower())
          
          self.reply.setText(f"Okay, thanks for sharing. {final_allergy} will not be \npart of the recipe I generate for your dessert!")
          while self.window.getKey() != "Return":
            self.reply.setSize(20)

          self.reply.setText("")
          self.message.setText("Do you have any more allergies I should know about? (Y/N) ")
          more_allergies = ""

          button_yes = Rectangle(Point(9,5),Point(12,7))
          button_yes_text = Text(button_yes.getCenter(),"Yes")
          button_no = Rectangle(Point(18,5),Point(21,7))
          button_no_text = Text(button_no.getCenter(),"No")
        
          button_yes.draw(self.window)
          button_yes_text.draw(self.window)
          button_no.draw(self.window)
          button_no_text.draw(self.window)

          allergic = False
          while True:
            clickPoint = self.window.getMouse()
            if inside(clickPoint,button_yes):
              more_allergies = "Y"
              break
            elif inside(clickPoint,button_no):
              more_allergies = "N"
              break
          
          button_yes.undraw()
          button_yes_text.undraw()
          button_no.undraw()
          button_no_text.undraw()

          if more_allergies == "N":
            allergies = False
            self.reply.setText("Alright, cool. We can move on then!")
            self.message.setText("")
            while self.window.getKey() != "Return":
              self.reply.setSize(20)
          self.entry.undraw()
          self.reply.setText("")
    else:
        self.reply.setText("Alright, cool. We can move on then!")
        self.message.setText("")
        while self.window.getKey() != "Return":
          self.reply.setSize(20)
        self.reply.setText("")
    
    self.message.setText("Wait for it...")
    time.sleep(2)
    return name, favorite_ingredient, ingredients_allergens, main_allergen

  def display_recipe_graphic(self,formatted_recipe, user_name):
    self.image.undraw()
    self.image = Image(Point(15,32), "gordon_done.gif")
    self.image.draw(self.window)
    self.guide.setText("")
    self.message.setText(f"Here is dessert recipe custom made for {user_name}! \n")
    split_string = formatted_recipe.split("\n\n")

    # Make sure summary string fits in the window.
    summary = split_string[1].split(" ")
    lines = []
    line = ""
    for token in summary:
      if len(line) > 50: # 50 seems like a nice threshhold.
        lines.append(line)
        line = token + " "
      else:
        line += token + " "
    lines.append(line)
    
    summarystr = "\n".join(lines) + "."
    final_string = "\n\n".join([split_string[0], summarystr, split_string[2]])
    recipe_display = Text(Point(15,13),final_string)
    recipe_display.setSize(15)
    recipe_display.setFace('courier')
    recipe_display.draw(self.window)
    self.guide.setText("Hit Enter to move on.")
    while self.window.getKey() != "Return":
      recipe_display.setSize(15)