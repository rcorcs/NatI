# OGDEN - last updated for NodeBox 1.9.4
# Author: Tom De Smedt <tomdesmedt@organisms.be>
# See LICENSE.txt for details.

# Based on Charles K. Ogden list of basic English words:
# http://ogden.basic-english.org

import os
path = os.path.join(os.path.dirname(__file__), "ogden_2000.txt")

words = open(path).readlines()
words = [x.split(" ") for x in words]
words.sort(lambda a, b: cmp(a[0].lower(), b[0].lower))   

nouns      = [word for word, tags in words if "NN" in tags]
verbs      = [word for word, tags in words if "VB" in tags]
adjectives = [word for word, tags in words if "JJ" in tags]
adverbs    = [word for word, tags in words if "RB" in tags]

words = [word for word, tags in words]

