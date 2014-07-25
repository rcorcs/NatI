# ORDINAL - last updated for NodeBox 1rc7
# Author: Tom De Smedt <tomdesmedt@organisms.be>
# See LICENSE.txt for details.

# Based on the Ruby Linguistics module by Michael Granger:
# http://www.deveiate.org/projects/Linguistics/wiki/English

ordinal_nth = {
    0  : "th",
    1  : "st",
    2  : "nd",
    3  : "rd",
    4  : "th",
    5  : "th",
    6  : "th",
    7  : "th",
    8  : "th",
    9  : "th",
    11 : "th",
    12 : "th",
    13 : "th",   
}

ordinal_suffixes = [
                    
    ["ty$"    , "tieth"],
    ["one$"   , "first"],
    ["two$"   , "second"],
    ["three$" , "third"],
    ["five$"  , "fifth"],
    ["eight$" , "eighth"],
    ["nine$"  , "ninth"],
    ["twelve$", "twelfth"],
    ["$"      , "th"],
    
]

def ordinal(number):
    
    """ Returns the ordinal word of a given number.
    
    For example: 103 -> 103rd, twenty-one -> twenty first.
    The given number can be either integer or string,
    returns None otherwise.
    
    """
    
    if isinstance(number, int):
        if ordinal_nth.has_key(number%100):
            return str(number) + ordinal_nth[number%100]
        else:
            return str(number) + ordinal_nth[number%10]
    
    if isinstance(number, str):
        import re
        for suffix, inflection in ordinal_suffixes:
            if re.search(suffix, number) is not None:
                return re.sub(suffix, inflection, number) 
        

#print ordinal(103)    
#print ordinal("twenty-one")