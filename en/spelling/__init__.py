# Peter Norvig's spelling corrector, with adaptions for Python 2.3
# http://norvig.com/spell-correct.html

import os
import re
try: from collections import defaultdict
except:

    from sets import Set as set
    import copy
    class defaultdict(dict):
        """Dictionary with a default value for unknown keys.
        P. Novig, http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/389639
        """
        def __init__(self, default):
            self.default = default

        def __getitem__(self, key):
            if key in self: 
                return self.get(key)
            else:
                ## Need copy in case self.default is something like []
                return self.setdefault(key, copy.deepcopy(self.default))
        def __copy__(self):
            copy = defaultdict(self.default)
            copy.update(self)
            return copy
            
    def max(seq, key=None):
        def _cmp(a,b): 
            if key(b) > key(a): return 1
            return -1
        seq = [e for e in seq]
        if key:
            seq.sort(_cmp)
        else:
            seq.sort()
        return seq[0]

def words(text): 
    return re.findall('[a-z]+', text.lower()) 

def train(features):
    try:
        # for the custom definition of defaultdict
        model = defaultdict(1)         
    except: 
        model = defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

path = os.path.join(os.path.dirname(__file__), "spelling.txt")
NWORDS = train(words(open(path).read()))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
    n = len(word)
    return set([word[0:i]+word[i+1:] for i in range(n)] +                     # deletion
               [word[0:i]+word[i+1]+word[i]+word[i+2:] for i in range(n-1)] + # transposition
               [word[0:i]+c+word[i+1:] for i in range(n) for c in alphabet] + # alteration
               [word[0:i]+c+word[i:] for i in range(n+1) for c in alphabet])  # insertion

def known_edits2(word):
    #return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)
    s = set()
    for e1 in edits1(word):
        for e2 in edits1(e1):
            if e2 in NWORDS: s.add(e2)
    return s

def known(words): 
    #return set(w for w in words if w in NWORDS)
    s = set()
    for w in words: 
        if w in NWORDS: s.add(w)
    return s

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=lambda w: NWORDS[w])

def suggest(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return list(candidates)

#print suggest("beautiufl")
#print suggest("beautifull")