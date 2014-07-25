# PARSER - last updated for NodeBox 1.9.2
# Author: Tom De Smedt <tomdesmedt@organisms.be>
# See LICENSE.txt for details.

# The part-of-speech-tagger was adopted by Jason Wiener from Mark Watson:
# http://jasonwiener.wordpress.com/category/nlp/
# Based on Brill's lexicon.
# The chunker relies on NLTK from the University of Pennsylvania:
# http://nltk.sourceforge.net/

# I changed the import statements in NLTK from
# "from nltk_lite." to "from en.parser.nltk_lite." for them to work.
# Additionally, two lines in ntlk_lite/probability.py 
# were try/excepted (search source for "numpy").
# They use imported tools from NumPy but are not needed here,
# so NumPy (which is 7MB) is unnecessary.

import pickle
import re

### PART OF SPEECH TAGGER ############################################################################

class PartOfSpeechTagger:
    
	"""
	Original Copyright (C) Mark Watson.  All rights reserved.
	Python port by Jason Wiener (http://www.jasonwiener.com)
    
	THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY
	KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
	IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A
	PARTICULAR PURPOSE.
    
	"""
	
	lexHash = {}
	
	def __init__(self):

		if(len(self.lexHash) == 0):
			import os
			path = os.path.join(os.path.dirname(__file__), "Brill_lexicon")
			upkl = open(path, 'r')
			self.lexHash = pickle.load(upkl)
			upkl.close()

	def tokenize(self,s):

		v = []
		reg = re.compile('(\S+)\s')
		m = reg.findall(s+" ");
		
		for m2 in m:
			if len(m2) > 0:
				if m2.startswith("("):
					v.append(m2[0])
					m2 = m2[1:]
				if m2.endswith(";") \
				or m2.endswith(",") \
				or m2.endswith("?") \
				or m2.endswith(")") \
				or m2.endswith(":") \
				or m2.endswith(".") \
				or m2.endswith("!"):
					v.append(m2[0:-1])
					v.append(m2[-1])
				else:
					v.append(m2)

		return v

	def tag(self,words):
		
		ret = []
		for i in range(len(words)):
			ret.append("NN") #the default entry
			if self.lexHash.has_key(words[i]):
				ret[i] = self.lexHash[words[i]]
			elif self.lexHash.has_key(words[i].lower()):
				ret[i] = self.lexHash[words[i].lower()]

		#apply transformational rules
		for i in range(len(words)):
			
			#rule 1 : DT, {VBD | VBP} --> DT, NN
			if i > 0 and ret[i-1] == "DT":
				if ret[i] == "VBD" or ret[i] == "VBP" or ret[i] == "VB":
					ret[i] = "NN"

			#rule 2: convert a noun to a number (CD) if "." appears in the word
			if ret[i].startswith("N"):
				if words[i].find(".") > -1:
					ret[i] = "CD"

			# rule 3: convert a noun to a past participle if ((string)words[i]) ends with "ed"
			if ret[i].startswith("N") and words[i].endswith("ed"):
				ret[i] = "VBN"

			# rule 4: convert any type to adverb if it ends in "ly"
			if words[i].endswith("ly"):
				ret[i] = "RB"

			# rule 5: convert a common noun (NN or NNS) to a adjective if it ends with "al"
			if ret[i].startswith("NN") and words[i].endswith("al"):
				ret[i] = "JJ"

			# rule 6: convert a noun to a verb if the preceeding work is "would"
			if i > 0 and ret[i].startswith("NN") and words[i - 1].lower() == "would":
				ret[i] = "VB"

			# rule 7: if a word has been categorized as a common noun and it ends with "s",
			# then set its type to plural common noun (NNS)
			if ret[i] == "NN" and words[i].endswith("s"):
				ret[i] = "NNS"

			# rule 8: convert a common noun to a present participle verb (i.e., a gerand)
			if ret[i].startswith("NN") and words[i].endswith("ing"):
				ret[i] = "VBG"

		return ret

pos_tagger = PartOfSpeechTagger()

class TaggedSentence(list):
    
    """ A list of (token, tag) tuples representing a POS tagged sentence.
    
    When printed or transformed with str(),
    is represented as a string of token/tag.
    
    For example:
    [(the,DT), (cat,NN), (likes,VBZ), (fish,NN)] ->
    the/DT cat/NN likes/VBZ fish/NN
    
    """
    
    def __repr__(self):
          
        str = [token+"/"+tag for token, tag in self]
        str = " ".join(str)
        return str

def sentence_tag(sentence):
    
    """ Returns a tagged sentence.
    
    Part of speech tagging assigns a marker 
    to each word in the sentence,
    as corresponding to a particular part of speech
    (nouns, verbs, adjectives, ...)
    
    Tagging is done using Jason Wiener's
    parser and a Brill lexicon.
    
    Tagging involves a lot of ambiguity.
    For example, fish has different meanings:
    cats like fish <-> men like to fish
    
    """
    
    tokens = pos_tagger.tokenize(sentence)
    tags = pos_tagger.tag(tokens)
    
    tagged = TaggedSentence()
    for i in range(len(tokens)):
        tagged.append((tokens[i], tags[i]))
        
    return tagged

### CHUNKING #########################################################################################

from nltk_lite.parse import chunk as nltk_chunk
from nltk_lite.parse import tree as nltk_tree

# Simple regular expression rules for chunking.
chunk_rules = [
    ("NP", r"<DT|CD|JJ.*|PRP.*|NN.*>+", "noun phrases with determiner, adjectives, nouns"),
    ("PP", r"<IN><NP>",                 "preposition (in, of, on) followed by noun phrase"),
    ("VP", r"<RB.*|RP|VB.*|MD|TO>+",    "verb phrases"),
    ("VA", r"<VP><NP|PP|S>",            "verbs and arguments/adjuncts"),
    ("S", r"<NP|PP|PRP><VP|VA>",        "subject")
]

def sentence_chunk(sentence):
    
    """ Chunks a tagged sentence into syntactically correlated parts of words.
    """
    
    tagged = sentence_tag(sentence)
    tagged = str(tagged)
    
    leaves = nltk_tree.chunk(tagged).leaves()
    tree = nltk_tree.Tree("", leaves)
    for tag, rule, desc in chunk_rules:
        r = nltk_chunk.ChunkRule(rule,"")
        chunker = nltk_chunk.RegexpChunk([r], chunk_node=tag)
        tree = chunker.parse(tree)
    
    return _traverse_chunktree(tree)
    
def _traverse_chunktree(tree):
    
    """ Converts the output of sentence_chunk() to a Python list.
    
    sentence_chunk() generates an NLTK Tree object,
    but I want something straightforward as a list of lists here.
    
    For example:
    we are going to school ->
    [['SP',
      ['NP', ('we', 'PRP')],
      ['AP',
       ['VP', ('are', 'VBP'), ('going', 'VBG'), ('to', 'TO')],
       ['NP', ('school', 'NN')]]]]
    
    """
    
    list = []
    for child in tree:
        if isinstance(child, nltk_tree.Tree):
            list.append(_traverse_chunktree(child))
            list[-1].insert(0, child.node)
        elif isinstance(child, tuple):
            list.append(child)
                
    return list

def sentence_traverse(sentence, f):
    
    """ Chunks sentence and feeds its parts to function f.
    
    The sentence is chunked and traversed recusively.
    Each chunk is fed to def f(chunk, token, tag).
    The chunk parameter is either a string or None,
    in which case token and tag are strings.
        
    """
    
    def _traverse(tree):
        for child in tree:
            if isinstance(child, str) and child in chunks:
                f(child, None, None)
            elif isinstance(child, tuple):
                f(None, child[0], child[1])
            elif isinstance(child, list):
                _traverse(child)
    
    chunks = [tag for tag, rule, desc in chunk_rules]
    sentence = sentence_chunk(sentence)
    _traverse(sentence)

### PATTERN MATCHING #################################################################################
# A powerful mechanism for searching tagged text.
# "Beautiful fresh flowers and plants are all around the lush garden."
# "(JJ) (JJ) NN" --> Beautiful fresh flowers, plants, lush garden.
# We can use it to compare stuff (NN is bigger than NN),
# to aggregate commonsense data (red NN | NN VB red), etc. 

def combinations(items, n):
    """ Returns all possible combinations of length n of the given items.
    """
    if n == 0: yield []
    else:
        for i in xrange(len(items)):
            for c in combinations(items, n-1):
                yield [items[i]] + c

def is_optional(pattern):
    """ An optional pattern is enclosed in brackets.
    """
    if pattern.startswith("(") and pattern.endswith(")"):
        return True
    return False 
    
def variations(pattern):
    """ Returns all possible variations of a pattern containing optional pieces.
    """
    # Boolean pattern, True where pattern is optional.
    # (JJ) (NN) NN --> True True False
    o = [is_optional(p) for p in pattern]
    V = []
    # All the possible True/False combinations of optionals.
    # (JJ) (NN) NN --> True True, True False, False True, False False.
    for c in combinations([True, False], sum(o)):
        # If True in boolean pattern, replace by boolean in current combination.
        # (JJ) (NN) NN --> True True False, True False False, False True False, False False False.
        v = [b and (b and c.pop(0)) for b in o]
        # Replace True by pattern at that index.
        # --> (JJ) (NN) NN, (JJ) NN, (NN) NN, NN.
        v = [pattern[i] for i in range(len(v)) if not v[i]]
        v = [p.strip("()") for p in v]
        if v not in V: V.append(v)
    # Longest-first.
    V.sort(lambda a, b: len(b) - len(a))
    return V

# 1) Pattern NN matches /NN as well as /NNS tokens.
# 2) Pattern "new" matches token "new".
# 3) Pattern "*" matches any token.
# 4) Pattern "new*" matches tokens "new", "news", "newest", ...
# 5) Pattern "*new" matches tokens "new", "renew", ...
# 6) Pattern "*new*" matches "new", "renewal", ...
matching_rules = [
    lambda p, token, tag: tag.startswith(p),
    lambda p, token, tag: token == p,
    lambda p, token, tag: p == "*",
    lambda p, token, tag: p.endswith("*") and token.startswith(p[:-1]),
    lambda p, token, tag: p.startswith("*") and token.endswith(p[1:]),
    lambda p, token, tag: p.startswith("*") and p.endswith("*") and token.find(p[1:-1]) >= 0
]
def is_match(pattern, token, tag):
    """ Returns True if one of the rules matches pattern to token/tag.
    """
    # Case-insensitive search:
    pattern, token, tag = pattern.lower(), token.lower(), tag.lower()
    for r in matching_rules:
        if r(pattern, token, tag): return True
    return False

def matches(sentence, pattern, chunked=True):
    """ Find sequences of tokens that match the pattern.
    The pattern can include tokes, part-of-speech tags and wildcards.
    The algorithm is greedy: it will return the longest possible match.
    Example: "The new president was in the news" --> "new* (NN)" --> ["new president", "news"].
    """
    t = sentence_tag(sentence)
    v = variations(pattern.split())
    m = []
    # Move from token to token in the sentence.
    i = 0
    while i < len(t):
        # Check each variation of the pattern.
        for p in v:
            # If it is smaller than the remainder of the sentence,
            # see if it matches the next tokens in the sentence.
            # In this case is_match() will return True for each token (count them).
            n = len(p)
            if n <= len(t[i:]):
                b = sum( [is_match(p, token, tag) 
                          for p, (token, tag) in zip(p, t[i:i+n])] )
                if b == len(t[i:i+n]):
                    # Found the longest possible pattern,
                    # greedily skip to the next part of the sentence.
                    m.append(t[i:i+n])
                    i += n
                    break            
        i += 1
    
    if not chunked:
        for i in range(len(m)):
            m[i] = " ".join([token for token, tag in m[i]])
    
    return m
    
sentence_find = matches

### PART OF SPEECH TAGS ##############################################################################

# A description and an example for each part-of-speech
# used in tagging and chunking.
# See http://en.wikipedia.org/wiki/Brown_Corpus#Part-of-speech_tags_used.
pos_tags = {
    "np"   : ("noun phrase", "the pink panther"),
    "vp"   : ("verb phrase", "die laughing madly"),
    "va"   : ("verb phrase and arguments", "telling a lie"),
    "s"    : ("subject phrase", "suzy [is telling [a lie]]"),
    "ax"   : ("", ""),
    "vb"   : ("verb, base form", "think"),
    "vbz"  : ("verb, 3rd person singular present", "she thinks"),
    "vbp"  : ("verb, non-3rd person singular present", "I think"),
    "vbd"  : ("verb, past tense", "they talked"),
    "vbn"  : ("verb, past participle", "a sunken ship"),
    "vbg"  : ("verb, gerund or present participle", "programming is fun"),
    "md"   : ("verb, modal auxillary", "may, should, wouldn't"),
    "nn"   : ("noun, singular or mass", "tiger, chair, laughter"),
    "nns"  : ("noun, plural", "tigers, chairs, insects"),
    "nnp"  : ("noun, proper singular", "Germany, God, Alice"),
    "nnps" : ("noun, proper plural", "we met two Christmases ago"),
    "jj"   : ("adjective", "nice, easy, boring"),
    "jjr"  : ("adjective, comparative", "nicer, easier, more boring"),
    "jjs"  : ("adjective, superlative", "nicest, easiest, most boring"),
    "rb"   : ("adverb", "extremely, loudly, hard"),
    "wrb"  : ("adverb, wh-", "where, when"),
    "rbr"  : ("adverb, comparative", "better"),
    "rbs"  : ("adverb, superlative", "best"),
    "rp"   : ("adverb, particle", "about, off, up"),
    "prp"  : ("pronoun, personal", "me, you, it"),
    "prp$" : ("pronoun, possessive", "my, your, our"),
    "wp"   : ("pronoun, personal", "what, who, whom"),
    "wp$"  : ("pronoun, possessive", "whose, whosever"),
    "pdt"  : ("", ""),
    "wdt"  : ("determiner", "which, whatever, whichever"),
    "dt"   : ("determiner", "the, a, these"),
    "ex"   : ("existential there", "there were six boys"),
    "cc"   : ("conjunction, coordinating", "and, or, but"),
    "in"   : ("conjunction, subordinating or preposition", "of, on, before, unless"),
    "to"   : ("infinitival to", "what to do?"),
    "cd"   : ("cardinal number", "fixe, three, 13%"),
    "uh"   : ("interjection", "oh, oops, gosh"),
    "fw"   : ("foreign word", "mais"),
    "sym"  : ("", ""),
    "."    : ("punctuation mark, sentence closer", ".;?*"),
    ","    : ("punctuation mark, comma", ","),
    ":"    : ("punctuation mark, colon", ":"),
    "("    : ("contextual separator, left paren", "("),
    ")"    : ("contextual separator, right paren", ")"),
    "ls"   : ("", "")
}

def tag_description(postag):
    return pos_tags[postag.lower()]

#s = "that cat looks like a hamster"
#s = "the sun is shining"
#s = "that has been plaguing john"
#s = "he is always trying to feed her with lies"
#s = "we are going to school"
#from pprint import pprint
#pprint( sentence_chunk(s) )

#def callback(chunk, token, tag):
#    if chunk != None : print tag_description(chunk)[0].upper()
#    if chunk == None : print token, "("+tag_description(tag)[0]+")"
#sentence_traverse(s, callback)