from bs4 import BeautifulSoup
import urllib.request
# pip install bs4

def get_recipe_text(list_name, link):
  '''
  input: name of list with links
  link: link from list
  
  purpose: write desired text of link into a text file in the list name's folder in the corpus
  '''
  #get the html from the link, and make it a beautifulSoup object
  html = urllib.request.urlopen(link).read()
  soup = BeautifulSoup(html, "html.parser")

  #get the title of the recipe and write to file of the same name
  title = soup.find("div", class_="intro article-info")
  new_file = open("corpus/%s/%s.txt" % (list_name, title.text.strip()), "a")
  new_file.write(title.text.strip() + "\n")

  #get the summary of the recipe and write to file
  summary = soup.find("div", class_="recipe-summary")
  new_file.write(summary.text + "\n")
  
  #get list of ingredients and write to file
  recipe = soup.find_all("span", class_="ingredients-item-name")
  for item in recipe:
    new_file.write(item.text + "\n")

def read_list(list_name):
  #iterate over links in the file list_name.txt
  topic_list = open("topic lists/%s.txt" % list_name, "r")
  for link in topic_list:
    get_recipe_text(list_name, link)

def create_corpus():
  #create corpus files for given categories
  read_list("Frozen desserts") #Yemi
  read_list("Cakes") #Sue
  read_list("Pies") #Maanya
  read_list("Cobblers") #Nicole
  read_list("Cookies") #Maanya

create_corpus()