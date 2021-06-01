from chef_raimsey import *
from chef_raimsey_graphic import *
from graphics import *
import time

class Chef_Raimsey_Controller:
  def __init__(self):
    self.chef = Chef_Raimsey(gui=True)

  def start(self):
    recipe = self.chef.generate()
    self.start_over()

  def start_over(self):
    if self.chef.gui:
      window = self.chef.chef_raimsey_graphic.window

      button_yes = Rectangle(Point(8,3),Point(13,5))
      button_yes_text = Text(button_yes.getCenter(),"Start Over")
      button_yes.setFill('green')
      button_no = Rectangle(Point(17,3),Point(22,5))
      button_no_text = Text(button_no.getCenter(),"Exit")

      button_yes.draw(window)
      button_yes_text.draw(window)
      button_no.draw(window)
      button_no_text.draw(window)

      self.chef.chef_raimsey_graphic.guide.setText("")

      while True:
        clickPoint = window.getMouse()
        if inside(clickPoint,button_yes):
          window.close()
          self.start()
          break
        elif inside(clickPoint,button_no):
          button_yes.undraw()
          button_yes_text.undraw()
          button_no.undraw()
          button_no_text.undraw()
          bye_box = Rectangle(Point(8,3),Point(22,5))
          bye_text = Text(bye_box.getCenter(), "I hope you enjoying the recipe. Bye!")
          bye_box.draw(window)
          bye_text.draw(window)
          time.sleep(10)
          bye_box.undraw()
          button_no_text.undraw()
          window.close()
          break

      button_yes.undraw()
      button_yes_text.undraw()
      button_no.undraw()
      button_no_text.undraw()
    else:
      start_over = input("Start Over? (Y/N)")
      if start_over.lower() == "y":
        self.start()
      else:
        print("Good bye!")

# for GUI button
def inside(point, rectangle):
  """ Is point inside rectangle? """

  ll = rectangle.getP1()  # assume p1 is ll (lower left)
  ur = rectangle.getP2()  # assume p2 is ur (upper right)

  return ll.getX() < point.getX() < ur.getX() and ll.getY() < point.getY() < ur.getY()

if __name__ == "__main__":
  controller = Chef_Raimsey_Controller()
  controller.start()
