# QUANTIFY - last updated for NodeBox 1rc7
# Author: Tom De Smedt <tomdesmedt@organisms.be>
# See LICENSE.txt for details.

# Based on the Ruby Linguistics module by Michael Granger:
# http://www.deveiate.org/projects/Linguistics/wiki/English

from article import article
from numeral import spoken_number, thousands as numeral_thousands
from plural import plural
from math import log, pow

quantify_custom_plurals = {
    "built-in function" : "built-in functions"
}

def quantify(word, number=0):
    
    """ Returns a phrase describing the number of given objects.
    
    Two objects are described as being a pair,
    smaller than eight is several,
    smaller than twenty is a number of,
    smaller than two hundred are dozens,
    anything bigger is described as being
    tens or hundreds of thousands or millions.
    
    For example:
    chicken, 100 -> dozens of chickens 
    
    """
    
    def _plural(word):
        return plural(word, custom=quantify_custom_plurals)
    
    if number == 0:
        return "no " + _plural(word)
    if number == 1:
        return article(word)
    if number == 2:
        return "a pair of " + _plural(word)
    if number in range(3,8):
        return "several " + _plural(word)
    if number in range(8,20):
        return "a number of " + _plural(word)
    if number in range(20,200):
        return "dozens of " + _plural(word)
        
    if number >= 200:
        
        thousands = int( log(number, 10) / 3 )
        subthousands = int( log(number, 10) % 3 )
        
        if subthousands == 2:
            stword = "hundreds of "
        elif subthousands == 1:
            stword = "tens of "
        else:
            stword = ""
        if thousands > 0:
            thword = _plural(numeral_thousands(thousands-1)) + " of "
        else:
            thword = ""
            
        return stword + thword + _plural(word)

def conjunction(words, generalize=False):
    
    if generalize == True:
        words = _reflect(words)
    
    # Keep a count of each object in the list of words.
    count = {}
    for word in words:
        if count.has_key(word):
            count[word] += 1
        else:
            count[word] = 1

    # Create a list of (count, word) tuples
    # which we can sort highest-first.
    sortable = []
    for word in count:
        sortable.append((count[word], word))
    sortable.sort()
    sortable.reverse()

    # Concatenate quantifications of each object,
    # starting with the one that has the highest occurence.
    phrase = ""
    i = 0
    for n, word in sortable:
        if i == len(count)-2:
            separator = " and "
        else:
            separator = ", "
        phrase += quantify(word, n) + separator
        i += 1
    
    phrase = phrase.rstrip(separator)
    return phrase

#print quantify("chicken", 0)
#print quantify("chicken", 1)
#print quantify("chicken", 2)
#print quantify("chicken", 3)
#print quantify("chicken", 10)
#print quantify("chicken", 100)
#print quantify("chicken", 1000)
#print quantify("chicken", 10000)
#print quantify("chicken", 100000)
#print quantify("chicken", 2000000)

#print conjunction(["goose", "goose", "duck", "chicken", "chicken", "chicken"])
#print conjunction(["penguin", "polar bear"])
#print conjunction(["whale"])

reflect_readable_types = {
    "<type '"         : "",
    "<class '(.*)'\>" : "\\1 class",
    "'>"              : "",
    "objc.pyobjc"     : "Python Objective-C",
    "objc_class"      : "Objective-C class",
    "objc"            : "Objective-C",
    "<objective-c class  (.*) at [0-9][0-9|a-z]*>" : "Objective-C \\1 class",
    "bool"            : "boolean",
    "int"             : "integer",
    "long"            : "long integer",
    "float"           : "float",
    "str"             : "string",
    "dict"            : "dictionary",
    "NoneType"        : "None type",
    "instancemethod"  : "instance method",
    "builtin_function_or_method" : "built-in function",
    "classobj"        : "class object",
    "\."              : " ",
    "_"               : " "          
}

def _reflect(object):
    
    """ Returns the type of each object in the given object.
    
    For modules, this means classes and functions etc.
    For list and tuples, means the type of each item in it.
    For unsubscriptable objects, means the type of the object itself.
    
    """
    
    types = []
    try: 
    
        # Classes and modules have a __dict__ attribute
        # listing methods, functions etc.    
        for a in object.__dict__:
            a = getattr(object, a)
            try:
                types.append(str(a.__class__))
            except: 
                types.append(str(type(a)))
        
        # Possibly object is a function.
        if len(object.__dict__) == 0:
            types.append(str(type(object)))
    
    except:
        
        # Lists and tuples can consist
        # of several types of objects.
        if isinstance(object, list) \
        or isinstance(object, tuple):
            for item in object:
                types.append(str(type(item)))
        
        # Dictionaries have string keys
        # pointing to objects.
        elif isinstance(object, dict):
            for key in object:
                types.append("str key")
                types.append(str(type(object[key])))
            
        else:
            types.append(str(type(object)))
    
    # Clean up type strings.
    import re
    for i in range(len(types)):
        for p in reflect_readable_types:
            types[i] = re.sub(p, reflect_readable_types[p], types[i])
    
    return types

#print conjunction("hello", generalize=True)
#print conjunction(["hello", "goobye"], generalize=True)
#print conjunction((1,2,3,4,5), generalize=True)
#print conjunction({"name": "linguistics", "version": 1.0}, generalize=True)
#print conjunction(conjunction, generalize=True)
#print conjunction(__dict__, generalize=True)
#import Foundation; print conjunction(Foundation, generalize=True)
#import Numeric; print conjunction(Numeric, generalize=True)