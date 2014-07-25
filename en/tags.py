# TAGS - last updated for NodeBox 1rc7
# Author: Tom De Smedt <tomdesmedt@organisms.be>
# See LICENSE.txt for details.

tags_html = [
    "!--", "!doctype", "a", "abbr", "acronym", "address",
    "applet", "area", "b", "base", "basefont", "bdo",
    "big", "blockquote", "body", "br", "button", "caption",
    "center", "cite", "code", "col", "colgroup", "dd", "del",
    "dir", "div", "dfn", "dl", "dt", "em", "fieldset",
    "font", "form", "frame", "frameset", "h1", "h2", "h3",
    "h4", "h5", "h6", "head", "hr", "html", "i", "iframe",
    "img", "input", "ins", "isindex", "kbd", "label",
    "legend", "li", "link", "map", "menu", "meta",
    "noframes", "noscript", "object", "ol", "optgroup",
    "option", "p", "param", "pre", "q", "s", "samp",
    "script", "select", "small", "span", "strike",
    "strong", "style", "sub", "sup", "table", "tbody",
    "td", "textarea", "tfoot", "th", "thead", "title",
    "tr", "tt", "u", "ul", "var", "xmp"
]

def is_tag(str):
    
    if str.startswith("<") and str.endswith(">"):
        return True
    else:
        return False    

def is_html_tag(str):
    
    """ Guesses whether the word is a HTML tag.
    
    Checks if the string is a tag,
    and if the tag is in the list of HTML entitities.
    
    """
    
    if is_tag(str):
        str = str.strip("</>").lower()
        i = str.find(" ")
        if i > 0:
            str = str[:i]
        if str in tags_html:
            return True
    
    return False

#print is_html_tag("</HTML>")
#print is_html_tag("<a href>")
#print is_html_tag("<xml>")

import sgmllib
class TagStripper(sgmllib.SGMLParser):
    
	def __init__(self):
		sgmllib.SGMLParser.__init__(self)
		
	def strip(self, html):
		self.data = ""
		self.feed(html)
		self.close()
		return self.data
		
	def handle_data(self, data):
	    self.data += data + " "

def strip_tags(str, clean=True):
    
    s = TagStripper()
    str = s.strip(str)
    
    import re
    str = re.sub("[ ]+", " ", str)
    
    if clean:
        lines = str.split("\n")
        str = ""
        for l in lines:
            if len(l.strip()) > 0:
                str += l.strip() + "\n"
        str.strip().strip()
        
    return str.strip()

#from urllib import urlopen
#html = urlopen("http://news.bbc.co.uk/").read()
#html = open("bbc.txt", "r").read()
#print strip_tags(html)