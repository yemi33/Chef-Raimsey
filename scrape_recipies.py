from bs4 import BeautifulSoup
import urllib.request
# pip install bs4

def get_recipe_text(list_name, link):
  url = link
  html = urllib.request.urlopen(url).read()
  soup = BeautifulSoup(html, "html.parser")

  title = soup.find("div", class_="intro article-info")
  new_file = open("corpus/%s/%s.txt" % (list_name, title.text.strip()), "a")
  new_file.write(title.text.strip() + "\n")

  summary = soup.find("div", class_="recipe-summary")
  new_file.write(summary.text + "\n")
  
  recipe = soup.find_all("span", class_="ingredients-item-name")
  for item in recipe:
    new_file.write(item.text + "\n")

def read_list(list_name):
  topic_list = open("topic lists/%s.txt" % list_name, "r")
  for link in topic_list:
    get_recipe_text(list_name, link)

def create_corpus():
  read_list("Frozen desserts") #Yemi
  read_list("Cakes") #Sue
  read_list("Pies") #Maanya
  read_list("Cobblers") #Nicole
  read_list("Cookies") #Maanya

create_corpus()