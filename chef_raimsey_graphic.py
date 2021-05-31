from graphics import *
import random 
import preprocessing

def conversation_starter_graphic(ingredients_dict):
  '''
  First few words of the greatest dessert Chef ever.
  '''
  name = ""
  favorite_ingredient = ""
  ingredients_allergens = []
  main_allergen = []
  
  # Initialize window and various graphical elements
  window = GraphWin("Chef Raimsey", 600, 800)
  window.setCoords(0,0,30,40)
  image = Image(Point(15,32), "ramsay.gif")
  image.draw(window)
  message = Text(Point(15, 22),"Hi. This is Chef Raimsey! And what is your name? ")
  message.setSize(20)
  message.draw(window)
  entry = Entry(Point(15, 5), 15)
  entry.setSize(20)
  entry.setFill(color_rgb(247,247,222))
  entry.draw(window)
  guide = Text(Point(15,2), "Hit Enter to move on.")
  guide.setTextColor('red')
  guide.draw(window)
  reply = Text(Point(15, 8), "")
  reply.setSize(20)
  reply.draw(window)

  # Get user name
  while window.getKey() != "Return":
    name = entry.getText().capitalize()
  name = entry.getText().capitalize()
  entry.undraw()

  # Reply to user name
  message.setText("")
  reply.setText(f"Oh Great! Hi {name}.")
  
  # Transition
  while window.getKey() != "Return":
    reply.setSize(20) 
  reply.setText("")

  # Ask for user favorite ingredient
  message.setText("What is your favorite ingredient in a dessert? ")
  entry.setText("")
  entry.draw(window)

  while window.getKey() != "Return":
    favorite_ingredient = entry.getText().capitalize()
  favorite_ingredient = entry.getText().lower()
  entry.undraw()
  message.setText("")

  # Check if user favorite ingredient in ingredients dict
  if favorite_ingredient in list(ingredients_dict.keys()):
    reply.setText(f"{favorite_ingredient.capitalize()}! Yummy, good choice!!")
    while window.getKey() != "Return":
      reply.setSize(20)
  else:
    res = [key for key in ingredients_dict.keys() if favorite_ingredient in key]
    if len(res) == 0:
        reply.setText("Sorry, we don't have your ingredient in our recipe shelf \nbut let's see what we can concoct for you! ")
        favorite_ingredient = random.choice(list(ingredients_dict.keys()))
        while window.getKey() != "Return":
          reply.setSize(20)
    else:
      reply.setText(f"{favorite_ingredient.capitalize()}! Yummy, good choice!!")
      while window.getKey() != "Return":
        reply.setSize(20)
      favorite_ingredient = res[0]
  reply.setText("")

  # Check for user allergies
  message.setText("And do you have any allergies that I should be aware of (Y/N)? ")
  guide.undraw()
  
  button_yes = Rectangle(Point(9,5),Point(12,7))
  button_yes_text = Text(button_yes.getCenter(),"Yes")
  button_no = Rectangle(Point(18,5),Point(21,7))
  button_no_text = Text(button_no.getCenter(),"No")

  button_yes.draw(window)
  button_yes_text.draw(window)
  button_no.draw(window)
  button_no_text.draw(window)

  allergic = False
  while True:
    clickPoint = window.getMouse()
    if inside(clickPoint,button_yes):
      allergic = True
      break
    elif inside(clickPoint,button_no):
      break
  
  button_yes.undraw()
  button_yes_text.undraw()
  button_no.undraw()
  button_no_text.undraw()

  guide.draw(window)
  if allergic:
      allergies = True
      while allergies:
        message.setText("Oh no! I will generate a recipe for you that takes the allergy into account.\nSo what is it that you are allergic to? \nHere is a list of possible options to help you out: ")
        allergens_dict = preprocessing.allergen()
        list_of_allergens = list(allergens_dict.keys())
        mapping = {}
        options = []
        for idx in range(len(list_of_allergens)):
            mapping[idx] = list_of_allergens[idx]
            option = Text(Point(15, (18 - idx * 1)),f"{idx}) {list_of_allergens[idx]}")
            option.setSize(16)
            option.draw(window)
            options.append(option)
        message.setText("Which of the above are you allergic to? \nEnter the corresponding numbers. \nSo if you are allergic to dairy, choose 0: ")
        entry.setText("")
        choice = ""
        entry.draw(window)
        while window.getKey() != "Return":
          choice = entry.getText().capitalize()
        choice = entry.getText().capitalize()

        reply.setText("The instructions say that you need \nto input integers between 0 and 4.")
        while choice.isnumeric() == False or int(choice) < 0 or int(choice) > 4:
            entry.setText("")
            while window.getKey() != "Return":
              choice = entry.getText().capitalize()
            choice = entry.getText().capitalize()
        
        reply.setText("")
        for option in options:
          option.undraw()

        choice = int(choice)
        allergy = mapping[choice]
        reply.setText(f"Ok noted! So you are allergic to {allergy}.")
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
            option.draw(window)
            options.append(option)
            y += 1
        reply.setText("")
        
        message.setText("Which of these are you allergic to? \nEnter the specific ingredient as shown in the list above: ")
        entry.setText("")
        final_allergy = ""
        while window.getKey() != "Return":
            final_allergy = entry.getText()
        final_allergy = entry.getText()

        while final_allergy.capitalize() not in allergies_list and final_allergy not in allergies_list and final_allergy.strip() not in allergies_list:
            reply.setText("The instructions asked you to enter the \nspecific ingredient as shown in the list above. \nTry again:")
            entry.setText("")
            while window.getKey() != "Return":
              final_allergy = entry.getText()
            final_allergy = entry.getText()

        reply.setText("")
        for option in options:
          option.undraw()
        entry.undraw()
        message.setText("")

        if final_allergy.lower() == "all of the above" or final_allergy.strip() == "All of the Above":
            for k in range(len(allergies_list)-1):
                ingredients_allergens.append(allergies_list[k].lower())
        else:
            ingredients_allergens.append(final_allergy.lower())
        
        reply.setText(f"Okay, thanks for sharing. {final_allergy} will not be \npart of the recipe I generate for your dessert!")
        while window.getKey() != "Return":
          reply.setSize(20)

        reply.setText("")
        message.setText("Do you have any more allergies I should know about? (Y/N) ")
        more_allergies = ""

        button_yes = Rectangle(Point(9,5),Point(12,7))
        button_yes_text = Text(button_yes.getCenter(),"Yes")
        button_no = Rectangle(Point(18,5),Point(21,7))
        button_no_text = Text(button_no.getCenter(),"No")
      
        button_yes.draw(window)
        button_yes_text.draw(window)
        button_no.draw(window)
        button_no_text.draw(window)

        allergic = False
        while True:
          clickPoint = window.getMouse()
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
          reply.setText("Alright, cool. We can move on then!")
          message.setText("")
          while window.getKey() != "Return":
            reply.setSize(20)
          reply.setText("Check the terminal for your recipe!")
          time.sleep(2)
        entry.undraw()
        reply.setText("")
  else:
      reply.setText("Alright, cool. We can move on then!")
      message.setText("")
      while window.getKey() != "Return":
        reply.setSize(20)
      reply.setText("Check the terminal for your recipe!")
      time.sleep(2)

  return name, favorite_ingredient, ingredients_allergens, main_allergen

# for GUI
def inside(point, rectangle):
  """ Is point inside rectangle? """

  ll = rectangle.getP1()  # assume p1 is ll (lower left)
  ur = rectangle.getP2()  # assume p2 is ur (upper right)

  return ll.getX() < point.getX() < ur.getX() and ll.getY() < point.getY() < ur.getY()