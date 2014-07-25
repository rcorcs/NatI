# VERB - last updated for NodeBox 1rc7
# Author: Tom De Smedt <tomdesmedt@organisms.be>
# See LICENSE.txt for details.

# The verb.txt morphology was adopted from the XTAG morph_englis.flat:
# http://www.cis.upenn.edu/~xtag/

# Each verb and its tenses is a list,
# indexed according to the following keys:
verb_tenses_keys = {
    "infinitive"           : 0,
    "1st singular present" : 1,
    "2nd singular present" : 2,
    "3rd singular present" : 3,
    "present plural"       : 4,
    "present participle"   : 5,
    "1st singular past"    : 6,
    "2nd singular past"    : 7,
    "3rd singular past"    : 8,
    "past plural"          : 9,
    "past"                 : 10,
    "past participle"      : 11
}

verb_tenses_aliases = {
    "inf"     : "infinitive",
    "1sgpres" : "1st singular present",
    "2sgpres" : "2nd singular present",
    "3sgpres" : "3rd singular present",
    "pl"      : "present plural",
    "prog"    : "present participle",
    "1sgpast" : "1st singular past",
    "2sgpast" : "2nd singular past",
    "3sgpast" : "3rd singular past",
    "pastpl"  : "past plural",
    "ppart"   : "past participle"
}

# Each verb has morphs for infinitve,
# 3rd singular present, present participle,
# past and past participle.
# Verbs like "be" have other morphs as well
# (i.e. I am, you are, she is, they aren't)
# Additionally, the following verbs can be negated:
# be, can, do, will, must, have, may, need, dare, ought.
verb_tenses = {}
import os
path = os.path.join(os.path.dirname(__file__), "verb.txt")
data = open(path).readlines()
for i in range(len(data)):
    a = data[i].strip().split(",")
    verb_tenses[a[0]] = a

# Each verb can be lemmatised:
# inflected morphs of the verb point
# to its infinitive in this dictionary.
verb_lemmas = {}
for infinitive in verb_tenses:
    for tense in verb_tenses[infinitive]:
        if tense != "":
            verb_lemmas[tense] = infinitive

def verb_infinitive(v):
    
    """ Returns the uninflected form of the verb.
    """
    
    try:
        return verb_lemmas[v]
    except:
        return ""
        
def verb_conjugate(v, tense="infinitive", negate=False):
    
    """Inflects the verb to the given tense.
    
    For example: be
    present: I am, you are, she is,
    present participle: being,
    past: I was, you were, he was,
    past participle: been,
    negated present: I am not, you aren't, it isn't.
    
    """
    
    v = verb_infinitive(v)
    i = verb_tenses_keys[tense]
    if negate is True: i += len(verb_tenses_keys)
    return verb_tenses[v][i]
    
def verb_present(v, person="", negate=False):
    
    """Inflects the verb in the present tense.
    
    The person can be specified with 1, 2, 3, "1st", "2nd", "3rd", "plural", "*".
    Some verbs like be, have, must, can be negated.
    
    """
    
    person = str(person).replace("pl","*").strip("stndrgural")
    hash = {
        "1" : "1st singular present",
        "2" : "2nd singular present",
        "3" : "3rd singular present",
        "*" : "present plural",
    }
    if person in hash \
    and verb_conjugate(v, hash[person], negate) != "":
        return verb_conjugate(v, hash[person], negate)
    
    return verb_conjugate(v, "infinitive", negate)
    
def verb_present_participle(v):
    
    """Inflects the verb in the present participle.
    
    For example:
    give -> giving, be -> being, swim -> swimming
    
    """
    
    return verb_conjugate(v, "present participle")

def verb_past(v, person="", negate=False):

    """Inflects the verb in the past tense.

    The person can be specified with 1, 2, 3, "1st", "2nd", "3rd", "plural", "*".
    Some verbs like be, have, must, can be negated.
    
    For example:
    give -> gave, be -> was, swim -> swam
    
    """
    
    person = str(person).replace("pl","*").strip("stndrgural")
    hash = {
        "1" : "1st singular past",
        "2" : "2nd singular past",
        "3" : "3rd singular past",
        "*" : "past plural",
    }
    if person in hash \
    and verb_conjugate(v, hash[person], negate) != "":
        return verb_conjugate(v, hash[person], negate)
    
    return verb_conjugate(v, "past", negate)
    
def verb_past_participle(v):

    """Inflects the verb in the present participle.
    
    For example:
    give -> given, be -> been, swim -> swum
    
    """
    
    return verb_conjugate(v, "past participle")

def verb_all_tenses():
    
    """Returns all possible verb tenses.
    """
    
    return verb_tenses_keys.keys()

def verb_tense(v):
    
    """Returns a string from verb_tenses_keys representing the verb's tense.
    
    For example:
    given -> "past participle"
    
    """
    
    infinitive = verb_infinitive(v)
    a = verb_tenses[infinitive]
    for tense in verb_tenses_keys:
        if a[verb_tenses_keys[tense]] == v:
            return tense
        if a[verb_tenses_keys[tense]+len(verb_tenses_keys)] == v:
            return tense

def verb_is_tense(v, tense, negated=False):
    
    """Checks whether the verb is in the given tense.
    """
    
    if tense in verb_tenses_aliases:
        tense = verb_tenses_aliases[tense]
    if verb_tense(v) == tense:
        return True
    else:
        return False
        
def verb_is_present(v, person="", negated=False):

    """Checks whether the verb is in the present tense.
    """

    person = str(person).replace("*","plural")
    tense = verb_tense(v)
    if tense is not None:
        if "present" in tense and person in tense:
            if negated is False:
                return True
            elif "n't" in v or " not" in v:
                return True
    
    return False
    
def verb_is_present_participle(v):

    """Checks whether the verb is in present participle.
    """
    
    tense = verb_tense(v)
    if tense == "present participle":
        return True
    else:
        return False
        
def verb_is_past(v, person="", negated=False):

    """Checks whether the verb is in the past tense.
    """

    person = str(person).replace("*","plural")
    tense = verb_tense(v)
    if tense is not None:
        if "past" in tense and person in tense:
            if negated is False:
                return True
            elif "n't" in v or " not" in v:
                return True
    
    return False
    
def verb_is_past_participle(v):

    """Checks whether the verb is in past participle.
    """
    
    tense = verb_tense(v)
    if tense == "past participle":
        return True
    else:
        return False
            
#print verb_present("have", person=3)
#print verb_present_participle("swim")
#print verb_past("swim")
#print verb_past_participle("give")
#print verb_tense("given")
#print verb_is_tense("am", "1st singular present")
#print verb_is_present("am", person=1, negated=False)
#print verb_is_present_participle("doing")