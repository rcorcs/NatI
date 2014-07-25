# NUMERAL - last updated for NodeBox 1rc7
# Author: Tom De Smedt <tomdesmedt@organisms.be>
# See LICENSE.txt for details.

# Based on "Numbers and plural words as spoken English" by Christopher Dunn:
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/413172

numerals = {
    0: "zero",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
    11: "eleven",
    12: "twelve",
    13: "thirteen",
    14: "fourteen",
    15: "fifteen",
    16: "sixteen",
    17: "seventeen",
    18: "eighteen",
    19: "nineteen",
    20: "twenty",
    30: "thirty",
    40: "forty",
    50: "fifty",
    60: "sixty",
    70: "seventy",
    80: "eighty",
    90: "ninety"
}

numeral_thousands = ["thousand"]
numeral_thousands.extend([m+"illion" for m in [
    "m", 
    "b", 
    "tr", 
    "quadr", 
    "quint",
    "sext",
    "sept",
    "oct",
    "non",
    "dec",
    "undec",
    "duodec",
    "tredec",
    "quattuordec",
    "quindec",
    "sexdec",
    "septemdec",
    "octodec",
    "novemdec",
    "vigint"
]])

numerals_all = [numerals[i] for i in numerals]
numerals_all.extend(numeral_thousands)
numerals_all.append("hundred")

def is_number(s):
    
    """ Determines whether the string is a number.
    
    A number is:
    - a series of digits
    - a digit series that contains one comma or one point
    - a digit series starting with a minus sign
    - a word in the numeral_all list
    - a compound numeral like "seventy-three"
    
    """
    
    s = str(s)
    s = s.lstrip("-")
    s = s.replace(",", ".", 1)
    s = s.replace(".", "0", 1)
    import re
    if re.match("^[0-9]+$", s):
        return True
    elif s in numerals_all:
        return True
    else:
        try:
            a, b = s.split("-")
            if a in numerals_all \
            and b in numerals_all:
                return True
        except:
            return False
        
#print is_number("-20.5")
#print is_number("seventy-three")

def thousands(i):
    return numeral_thousands[i]

def _chunk(n):

    """ Recursively transforms the number to words.
    
    A number is either in the numerals dictionary,
    smaller than hundred and a combination of numeals separated by a dash
    (for example: twenty-five),
    a multitude of hundred and a remainder,
    a multitude of thousand and a remainder.
    
    """

    if n in numerals:
        return numerals[n]
        
    ch = str(n)
    remainder = 0
    
    if n < 100:
        ch = _chunk((n//10)*10) + "-" + _chunk(n%10)
        return ch
    elif n < 1000:
        ch = _chunk(n//100) + " " + "hundred"
        remainder = n%100
    else:
        base = 1000
        for i in range(len(numeral_thousands)):
            base *= 1000
            if n < base:
                ch = _chunk(n//(base/1000)) + " " + numeral_thousands[i]
                remainder = n%(base/1000)
                break
    
    if remainder:
        if remainder >= 1000: 
            separator = ","
        elif remainder <= 100:
            separator = " and"
        else:
            separator = ""
        return ch + separator + " " + _chunk(remainder)
    else:
        return ch
    
def spoken_number(n):
    
    """ Tranforms integers and longs to spoken word.
    
    For example: 2385762345876 ->
    two trillion, three hundred and eighty-five billion, 
    seven hundred and sixty-two million, three hundred and forty-five thousand 
    eight hundred and seventy-six
    
    """

    if not isinstance(n, int) and not isinstance(n, long): 
        return n
    
    if n < 0:
        if n in numerals: 
            return numerals[n]
        else:
            return "minus " + _chunk(-n)
    
    return _chunk(n)

#print spoken_number(5)
#print spoken_number(2004)
#print spoken_number(2385762345876)