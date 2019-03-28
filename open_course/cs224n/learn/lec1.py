
from nltk.corpus import wordnet as wn
poses = {"n": "noun", "v":"verb", "s":"adj(s)", 'a':"adj", 'r':'adv'}

for synset in wn.synset('good'):
    print("{}: {}".format(poses[synset.pos()], ))




