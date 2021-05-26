import nltk

# just quick test by Nicole
# note that 1 cup is not taken a single unit, cup is NN
# we will need a way to address this
# the medium article does this by creating their own tagging
# each line is [cardinal][unit][ingredient]

#TLDR; we need to clean up the ingredient lists
nltk.download("punkt")
nltk.download('averaged_perceptron_tagger')

recipe_file = open("corpus/Cakes/Battenburg Cake.txt", "r")
for line in recipe_file:
  text = nltk.word_tokenize(line)
  print(nltk.pos_tag(text))

'''
[('Battenburg', 'NNP'), ('Cake', 'NNP')]
[]
[('This', 'DT'), ('fancy', 'JJ'), ('almond-flavored', 'JJ'), ('tea', 'NN'), ('cake', 'NN'), (',', ','), ('also', 'RB'), ('called', 'VBD'), ("'Battenberg/Battenburg", 'CD'), ('Cake', 'NNP'), ("'", 'POS'), ('or', 'CC'), ("'Battenberg/Battenburg", 'CD'), ('Square', 'NNP'), ("'", 'POS'), ('features', 'NNS'), ('a', 'DT'), ('homemade', 'NN'), ('marzipan', 'NN'), ('.', '.')]
[]
[('1', 'CD'), ('cup', 'NN'), ('butter', 'NN'), (',', ','), ('softened', 'VBD')]
[('1', 'CD'), ('cup', 'JJ'), ('white', 'JJ'), ('sugar', 'NN')]
[('3', 'CD'), ('eggs', 'NNS')]
[('¼', 'JJ'), ('teaspoon', 'NN'), ('vanilla', 'NN'), ('extract', 'NN')]
[('2', 'CD'), ('cups', 'NNS'), ('all-purpose', 'JJ'), ('flour', 'NN')]
[('1', 'CD'), ('teaspoon', 'NN'), ('baking', 'NN'), ('powder', 'NN')]
[('⅛', 'JJ'), ('teaspoon', 'NN'), ('salt', 'NN')]
[('2', 'CD'), ('drops', 'NNS'), ('red', 'JJ'), ('food', 'NN'), ('coloring', 'NN')]
[('1', 'CD'), ('cup', 'NN'), ('apricot', 'NN'), ('preserves', 'NNS')]
[('2', 'CD'), ('cups', 'NNS'), ('ground', 'NN'), ('almonds', 'NNS')]
[('3', 'CD'), ('cups', 'NNS'), ('confectioners', 'NNS'), ("'", 'POS'), ('sugar', 'NN')]
[('1', 'CD'), ('egg', 'NN'), (',', ','), ('room', 'NN'), ('temperature', 'NN')]
[('1', 'CD'), ('½', 'JJ'), ('teaspoons', 'NNS'), ('lemon', 'JJ'), ('juice', 'NN')]
[('¼', 'JJ'), ('teaspoon', 'NN'), ('almond', 'NN'), ('extract', 'NN')]
'''