# coding: utf-8

# WORDNET - last updated for NodeBox 1.9.2
# Author: Tom De Smedt <tomdesmedt@organisms.be>
# Copyright (c) 2007 Tom De Smedt.
# See LICENSE.txt for details.

# All other files are from PyWordNet by Oliver Steele and WordNet 2:
# http://osteele.com/projects/pywordnet/
# http://wordnet.princeton.edu

#This tells wordnet.py where to look the WordNet dictionary.
import os
pywordnet_path = os.path.join(os.path.dirname(__file__), "wordnet2")
os.environ["WNHOME"] = pywordnet_path

import wordnet as wn
import wntools

import re

NOUNS = wn.N
VERBS = wn.V
ADJECTIVES = wn.ADJ
ADVERBS = wn.ADV

ignore_accents = [
    ("á|ä|â|å|à", "a"), 
    ("é|ë|ê|è", "e"), 
    ("í|ï|î|ì", "i"), 
    ("ó|ö|ô|ø|ò", "o"), 
    ("ú|ü|û|ù", "u"), 
    ("ÿ|ý", "y"), 
    ("š", "s"), 
    ("ç", "ç"), 
    ("ñ", "n")
]
def _normalize(s):
    
    """ Normalize common accented letters, WordNet does not take unicode.
    """
    
    if isinstance(s, int): return s
    try: s = str(s)
    except:
        try: s = s.encode("utf-8")
        except:
            pass
    for a, b in ignore_accents: s = re.sub(a, b, s)
    return s    

def _synset(q, sense=0, pos=NOUNS):

    """Queries WordNet for q.

    The query function always returns data related to 
    the sense of q.

    Example: the word "tree" has the following senses:
    [["tree"], 
     ["tree", "tree diagram"], 
     ["Tree", "Sir Herbert Beerbohm Tree"]]

    Setting sense=0 would interpret "tree" as "a tree in a wood".

    """

    try: return pos[_normalize(q)][sense]
    except:
        return None

def _parse(data):

    """_parses data from PyWordnet to lists-in-lists.

    Human-readable strings from PyWordnet are
    converted to a list. This list contains lists.
    Each of these contains a series of words in the same "sense".
    Example: [["fly", "wing"], ["travel", "go", "move", "locomote"]]

   """

    if not isinstance(data, (list, tuple)):
        data = [data]
    return [
        [word.strip(" ") for word in m.split(",")]
            # Parse text between : and }
            for m in re.findall("\:(.*?)\}", str(data))
    ]

def senses(q, pos=NOUNS):

    """Returns all senses for q.
    """
    
    try: return _parse(pos[_normalize(q)].getSenses())
    except:
        return []

def count_senses(q, pos=NOUNS):
    
    """ Returns the number of senses/interpretations of q.
    
    Example:
    for i in range(noun.count_senses(q)):
        print noun.gloss(q, sense=i)
    
    """
    
    return len(senses(q, pos))

def gloss(q, sense=0, pos=NOUNS):

    """Returns a description text for q.

    Example: gloss("glass") returns
    "a brittle transparent solid with irregular atomic structure".

    """

    s = _synset(q, sense, pos)
    if not s:
        return ""
    return s.synset.gloss

def lexname(q, sense=0, pos=NOUNS):

    """Returns a type of q.

    Example: lexname("bee") returns "animal".

    """

    s = _synset(q, sense, pos)
    if not s: 
        return "" 
    data = str(s.lexname)
    data = data[data.index(".")+1:]
    if data == "Tops": 
        return q
    return data

def hyponym(q, sense=0, pos=NOUNS):

    """Returns the implementation of q.

    This can usually be considered as an "example" of q.
    Example: hyponym("train") returns
    [["boat train"], ["car train"], ["freight train", "rattler"], 
     ["hospital train"], ["mail train"], ["passenger train"], ["streamliner"], 
     ["subway train"]].

    """
    
    s = _synset(q, sense, pos)
    if not s: 
        return []
    return _parse(s.getPointers(wn.HYPONYM))

def hyponyms(q, sense=0, pos=NOUNS):

    """Returns all hyponyms of q.
    """

    s = _synset(q, sense, pos)
    if not s: 
        return []
    return _parse(flatten(wntools.tree(s, wn.HYPONYM)))

def hypernym(q, sense=0, pos=NOUNS):

    """Returns the abstraction of q.

    This can usually be considered as a class to which q belongs.
    Example: hypernym("train") returns [["public transport"]].

    """

    s = _synset(q, sense, pos)
    if not s: 
        return []
    return _parse(s.getPointers(wn.HYPERNYM))

def hypernyms(q, sense=0, pos=NOUNS):

    """Returns all hypernyms of q.
    """

    s = _synset(q, sense, pos)
    if not s: 
        return []
    return _parse(flatten(wntools.tree(s, wn.HYPERNYM)))

def antonym(q, sense=0, pos=NOUNS):

    """Returns the opposite of q.

    Example: antonym("death") returns
    [["birth", "nativity", "nascency", "nascence"]].

    """

    s = _synset(q, sense, pos)
    if not s: 
        return []
    return _parse(s.getPointers(wn.ANTONYM))

def holonym(q, sense=0, pos=NOUNS):

    """Returns the components of q.

    Example: holonym("house") returns
    [["library"], ["loft", "attic", "garret"], ["porch"], ["study"]]

    """

    s = _synset(q, sense, pos)
    if not s: 
        return []
    return _parse(s.getPointers(wn.PART_HOLONYM))

def meronym(q, sense=0, pos=NOUNS):

    """Returns the collection of many q"s.

    That of which q is a member.
    Example: meronym("tree") returns [["forest", "wood", "woods"]].

    """

    s = _synset(q, sense, pos)
    if not s: 
        return []
    return _parse(s.getPointers(wn.MEMBER_MERONYM)) 

def meet(q1, q2, sense1=0, sense2=0, pos=NOUNS):

    """Returns what q1 and q2 have in common.
    """

    s1 = _synset(q1, sense1, pos)
    s2 = _synset(q2, sense2, pos)
    if not s1: return []
    if not s2: return []
    return _parse(wntools.meet(s1, s2))

def flatten(tree):

    """Flattens a tree to a list.

    Example: ["one", ["two", ["three", ["four"]]]]
    becomes: ["one", "two", "three", "four"]

    """

    i = 0
    while i < len(tree):
        while isinstance(tree[i], (list, tuple)):
            if not tree[i]:
                tree.pop(i)
                if not len(tree): break
            else:
                tree[i:i+1] = list(tree[i])
        i += 1
    return tree

def absurd_gloss(q, sense=0, pos=NOUNS, up=3, down=2):

    """
    
    Attempts to simulate humor:
    takes an abstract interpretation of the word,
    and takes random examples of that abstract;
    one of these is to be the description of the word.
    
    The returned gloss is thus not purely random,
    it is still faintly related to the given word.
    
    """

    from random import random, choice

    def _up(path):
        p = hypernym(path, sense, pos)
        if p: return p[0][0]
        return path

    def _down(path):
        p = hyponym(path, sense, pos)
        if p: return choice(p)[0]
        return path

    for i in range(up): q = _up(q)
    for i in range(down): q = _down(q)
    return gloss(q)

def is_noun(q):
    return NOUNS.has_key(_normalize(q))
    
def is_verb(q):
    return VERBS.has_key(_normalize(q))
    
def is_adjective(q):
    return ADJECTIVES.has_key(_normalize(q))
    
def is_adverb(q):
    return ADVERBS.has_key(_normalize(q))

def all_nouns()      : return NOUNS
def all_verbs()      : return VERBS
def all_adjectives() : return ADJECTIVES
def all_adverbs()    : return ADVERBS

def _meta_create_shortcuts():

    """ Writes and compiles shortcut commands.
    
    For example: a noun_hyponym() command 
    is created that has the following definition:
    
    def noun_hyponym(q, sense=0):
        return hyponym(q, sense, pos=NOUNS)
    
    When the loop has executed you'll have comparable 
    verb_, adjective_ and adverb_ shortcuts 
    for each WordNet command.
    
    """

    def_prefixes = ["noun", "verb", "adjective", "adverb"]
    defs = ["count_senses", "senses", "gloss", "lexname", 
            "hyponym", "hyponyms", "hypernym", "hypernyms", 
            "antonym", "meronym", "holonym", "meet", "absurd_gloss"]

    for p in def_prefixes:
        for f in defs:
            if f == "count_senses" \
            or f == "senses": 
                params1 = "q"
                params2 = "q"
            elif f == "meet": 
                params1 = "q1, q2, sense1=0, sense2=0"
                params2 = "q1, q2, sense1, sense2"
            else:
                 params1 = "q, sense=0"
                 params2 = "q, sense"    
            code  = "global "+p+"_"+f+"\n"
            code += "def "+p+"_"+f+"("+params1+"):\n"
            code += "    return "+f+"("+params2+", pos="+p.upper()+"S)"
            eval(compile(code, "<string>", "exec"))
            #print code

_meta_create_shortcuts()

#print len(all_adverbs())
#print [str(x).rstrip("(n.)") for x in all_nouns()[:20]]
#print noun_lexname("fear")
#print noun_holonym("fish")
#print adjective_gloss("weak")
#print verb_antonym("sleep")