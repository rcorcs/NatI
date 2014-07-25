# COMMONSENSE - last updated for NodeBox 1.9.4
# Author: Tom De Smedt <tomdesmedt@organisms.be>
# See LICENSE.txt for details.

import numeral
import tags
import wordnet
import singular

# Connectives from a file somewhere in Darwin:
commonsense_connectives = [
    "I", "the", "of", "and", "to", "a", "in", "that", 
    "is", "was", "he", "for", "it", "with", "as", "his", 
    "on", "be", "at", "by", "i", "this", "had", "not", 
    "are", "but", "from", "or", "have", "an", "they", 
    "which", "one", "you", "were", "her", "all", "she", 
    "there", "would", "their", "we", "him", "been", "has", 
    "when", "who", "will", "more", "no", "if", "out", 
    "so", "said", "what", "u", "its", "about", "into", 
    "than", "them", "can", "only", "other", "new", "some", 
    "could", "time", "these", "two", "may", "then", "do", 
    "first", "any", "my", "now", "such", "like", "our", 
    "over", "man", "me", "even", "most", "made", "after", 
    "also", "did", "many", "before", "must", "through", 
    "back", "years", "where", "much", "your", "way", 
    "well", "down", "should", "because", "each", "just", 
    "those", "eople", "mr", "how", "too", "little",
     "state", "good", "very", "make", "world", "still", 
     "own", "see", "men", "work", "long", "get", "here", 
     "between", "both", "life", "being", "under", "never", 
     "day", "same", "another", "know", "while", "last", 
     "might", "us", "great", "old", "year", "off", 
     "come", "since", "against", "go", "came", "right", 
     "used", "take", "three"
]

# Common connectives:
commonsense_connectives.extend([
    "whoever", "nonetheless", "therefore", "although",
    "consequently", "furthermore", "whereas",
    "nevertheless", "whatever", "however", "besides",
    "henceforward", "yet", "until", "alternatively",
    "meanwhile", "notwithstanding", "whenever",
    "moreover", "despite", "similarly", "firstly",
    "secondly", "lastly", "eventually", "gradually",
    "finally", "thus", "hence", "accordingly",
    "otherwise", "indeed", "though", "unless"
    
])

def is_connective(word):
    
    """ Guesses whether the word is a connective.
    
    Connectives are conjunctions such as "and", "or", "but",
    transition signals such as "moreover", "finally",
    and words like "I", "she".
    
    It's useful to filter out connectives
    when guessing the concept of a piece of text.
    ... you don't want "whatever" to be the most important word
    parsed from a text.
    
    """
    
    if word.lower() in commonsense_connectives:
        return True
    else:
        return False

def sentence_keywords(str, top=10, nouns=True, singularize=True, filters=[]):
    
    """ Guesses keywords in a piece of text.
    
    Strips delimiters from the text and counts words occurences.
    By default, uses WordNet to filter out words,
    and furthermore ignores connectives, numbers and tags.
    By default, attempts to singularize nouns.
    
    The return value is a list (length defined by top)
    of (count, word) tuples.
    
    For example:
    from urllib import urlopen
    html = urlopen("http://news.bbc.co.uk/").read()
    meta = ["news", "health", "uk", "version", "weather", "video", "sport", "return", "read", "help"]
    print sentence_keywords(html, filters=meta)
    >>> [(6, 'funeral'), (5, 'beirut'), (3, 'war'), (3, 'service'), (3, 'radio'), (3, 'mull'), (3, 'lebanon'), (3, 'islamist'), (3, 'function'), (3, 'female')]
    
    """
    
    str = tags.strip_tags(str)
    str = str.replace("\n", " ")
    str = str.split(" ")

    count = {}
    for word in str:
        
        word = word.lower()
        
        # Remove special characters.
        # Do this a number of times to counter typos like:: this.
        for i in range(10):
            word = word.strip("(){}[]'\"\r\n\t,.?!;:-*/ ")
        
        # Determine nouns using WordNet.
        # Attempt singularization.
        noun = False
        if nouns == True:
            if singularize \
            and len(word) > 3 \
            and wordnet.is_noun(singular.singular(word)):
                noun = True
                word = singular.singular(word)
            elif wordnet.is_noun(word):
                noun = True
        
        # Filter for connectives, numbers, tags
        # and (by default) keep only nouns.
        if len(word) > 1 \
        and not word in filters \
        and not is_connective(word) \
        and not numeral.is_number(word) \
        and not tags.is_tag(word) \
        and (not nouns or noun):
            if word in count.keys():
                count[word] += 1
            else:
                count[word] = 1
    
    sorted = []
    for word in count.keys():
        sorted.append((count[word], word))
    sorted.sort()
    sorted.reverse()
    
    return sorted[:top]

#from urllib import urlopen
#html = urlopen("http://nodebox.net/code/index.php/Ideas_from_the_Heart").read()
#print sentence_keywords(html, singularize=True)
#>>> [(19, 'agent'), (12, 'creativity'), (12, 'art'), (11, 'design'), (11, 'computer'), (10, 'something'), (10, 'composition'), (9, 'concept'), (8, 'problem'), (7, 'need')]

# From ConceptNetNLTools:
# some common words associated with each Paul Ekman's basic emotions.
commonsense_ekman = ["anger", "disgust", "fear", "joy", "sadness", "surprise"]
commonsense_naive_ekman = [
    ["anger", "angered", "upset", "mad", "angry", "angriness"],
    ["disgust", "disgusted", "dislike", "abhorrence", "abomination", "detest", "detestation", "exercration", "loathe", "loathing", "odium", "hate", "repugnance", "repulsion", "revulsion", "horror"],
    ["fear", "fearful", "fright", "scared", "feared", "scare", "frighten", "frightened", "anxious", "anxiety", "panic", "terror", "horror", "intimidation", "creep", "chill", "shiver", "frisson", "danger", "dangerous"],
    ["joy", "happy", "happiness", "joyful", "joyfulness", "cheer", "cheerful", "cheerfulness", "smile"],
    ["sadness", "sad", "despair", "depressed", "depression"],
    ["surprise", "surprised", "surprising", "surprisal", "astonish", "amazement", "amaze", "excite", "excitement", "exciting", "shock", "stun", "stunning", "shocking", "bombshell", "unexpected", "sudden", "thrill", "tingle"]
]

def is_basic_emotion(word):
    
    """ Returns True if the word occurs in the list of basic emotions.
    """
    
    if word.lower().strip() in commonsense_ekman:
        return True
    else:
        return False

def is_emotion(word, shallow=False, pos=None, boolean=True):
    
    """ Guesses whether the word expresses an emotion.
    
    Returns True when the word is an emotion.
    When the boolean parameter is set to False,
    returns either None or a string hinting at the
    emotion the word expresses.
    
    For example:
    print is_emotion("blub", pos=wordnet.VERBS, boolean=False)
    >>> weep
    
    Preferably the return value would be an is_basic_emotion().
    
    """
    
    def _return(value):
        if boolean and value != None: 
            return True
        elif boolean: 
            return False
        else:
            return value
    
    if pos == None \
    or pos == wordnet.NOUNS:
        ekman = ["anger", "disgust", "fear", "joy", "sadness", "surprise"]
        other = ["emotion", "feeling", "expression"]
    if pos == wordnet.VERBS:
        ekman = ["anger", "disgust", "fear", "enjoy", "sadden", "surprise"]
        other = ["empathize", "feel", "express emotion", "express"]       
    if pos == wordnet.ADJECTIVES \
    or pos == wordnet.ADVERBS:
        ekman = ["angry", "disgusted", "fearful", "happy", "sad", "surprised"]
        other = ["emotional"]
    
    word = word.lower().strip()
    
    # Check the naive lists first.
    for i in range(len(commonsense_naive_ekman)):
        if word in commonsense_naive_ekman[i]:
            return _return(commonsense_ekman[i])

    # Fair competition:
    # if we shuffle the list we have an equal speed
    # for each Ekman emotion to scan.
    from random import shuffle
    indices = range(len(ekman))
    shuffle(indices)
    
    # For each Ekman emotion,
    # take all of its senses,
    # and check the hyponyms of that sense.
    for i in indices:
        emotion = ekman[i]
        s = wordnet.senses(emotion, pos)
        for j in range(len(s)):
            if word in s[j]:
                return _return(commonsense_ekman[i])
            h = wordnet.hyponyms(emotion, j, pos)
            h = wordnet.flatten(h)
            if word in h:
                return _return(commonsense_ekman[i])
    
    # Maybe we get lucky and WordNet has tagged
    # the word as a feeling.
    if shallow and wordnet.lexname(word, 0, pos) == "feeling":
        return _return("feeling")
    
    # Take a generalised word like "emotion"
    # and traverse its hyponyms.
    # When performing a deep search,
    # traverse the hyponyms of those hyponyms as well.
    # Example: "yearning" -> "desire" -> "feeling"
    for emotion in other:
        for w in wordnet.flatten(wordnet.hyponyms(emotion, 0, pos)):
            if word == w:
                return _return(emotion)
            if not shallow:
                if word in wordnet.flatten(wordnet.hyponym(w, 0, pos)):
                    return _return(w)
                    
    return _return(None)

def noun_is_emotion(word, shallow=False, boolean=True): 
    return is_emotion(word, shallow, wordnet.NOUNS, boolean)

def verb_is_emotion(word, shallow=False, boolean=True): 
    return is_emotion(word, shallow, wordnet.VERBS, boolean)

def adjective_is_emotion(word, shallow=False, boolean=True): 
    return is_emotion(word, shallow, wordnet.ADJECTIVES, boolean)

def adverb_is_emotion(word, shallow=False, boolean=True): 
    return is_emotion(word, shallow, wordnet.ADVERBS, boolean)

#print noun_is_emotion("grass")    
#print noun_is_emotion("rage", boolean=False)
#print adjective_is_emotion("anxious", boolean=False)
#print verb_is_emotion("snivel", boolean=False)

commonsense_persuasive_nouns = ["you", "money", "save", "new", "results", "health", "easy", "safety", "love", "discovery", "proven", "guarantee", "free", "important", "because", "together", "secrets"]

def is_persuasive(word):
    
    
    """ Words that evoke powerful emotions.
    
    They have been attributed to research at various universities
    but I can't find a real source.
    
    """
    
    return (word in commonsense_persuasive_nouns)