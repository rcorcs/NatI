# PLURAL - last updated for NodeBox 1rc7
# Author: Tom De Smedt <tomdesmedt@organisms.be>
# See LICENSE.txt for details.

# Based on "An Algorithmic Approach to English Pluralization" by Damian Conway:
# http://www.csse.monash.edu.au/~damian/papers/HTML/Plurals.html

# Prepositions are used to solve things like
# "mother-in-law" or "man at arms"
plural_prepositions = ["about", "above", "across", "after", "among", "around", "at", "athwart", "before", "behind", "below", "beneath", "beside", "besides", "between", "betwixt", "beyond", "but", "by", "during", "except", "for", "from", "in", "into", "near", "of", "off", "on", "onto", "out", "over", "since", "till", "to", "under", "until", "unto", "upon", "with"]

# Inflection rules that are either general,
# or apply to a certain category of words,
# or apply to a certain category of words only in classical mode,
# or apply only in classical mode.

# Each rule consists of:
# suffix, inflection, category and classic flag.

plural_rules = [

    # 0/ Indefinite articles and demonstratives.
    [
    ["^a$|^an$", "some", None, False],
    ["^this$", "these", None, False],
    ["^that$", "those", None, False],
    ["^any$", "all", None, False]
    ],

    # 1/ Possessive adjectives.
    # Overlaps with 1/ for "his" and "its".
    # Overlaps with 2/ for "her".
    [
    ["^my$", "our", None, False],
    ["^your$|^thy$", "your", None, False],
    ["^her$|^his$|^its$|^their$", "their", None, False]
    ],

    # 2/
    # Possessive pronouns.
    [
    ["^mine$", "ours", None, False],
    ["^yours$|^thine$", "yours", None, False],
    ["^hers$|^his$|^its$|^theirs$", "theirs", None, False]
    ],
    
    # 3/ 
    # Personal pronouns.
    [
    ["^I$", "we", None, False],
    ["^me$", "us", None, False],
    ["^myself$", "ourselves", None, False],
    ["^you$", "you", None, False],
    ["^thou$|^thee$", "ye", None, False],
    ["^yourself$|^thyself$", "yourself", None, False],
    ["^she$|^he$|^it$|^they$", "they", None, False],
    ["^her$|^him$|^it$|^them$", "them", None, False],
    ["^herself$|^himself$|^itself$|^themself$", "themselves", None, False],
    ["^oneself$", "oneselves", None, False]
    ],
    
    # 4/
    # Words that do not inflect.
    [
    ["$", "", "uninflected", False],
    ["$", "", "uncountable", False],
    ["s$", "s", "s-singular", False],
    ["fish$", "fish", None, False],
    ["([- ])bass$", "\\1bass", None, False],
    ["ois$", "ois", None, False],
    ["sheep$", "sheep", None, False],
    ["deer$", "deer", None, False],
    ["pox$", "pox", None, False],
    ["([A-Z].*)ese$", "\\1ese", None, False],
    ["itis$", "itis", None, False],
    ["(fruct|gluc|galact|lact|ket|malt|rib|sacchar|cellul)ose$", "\\1ose", None, False]
    ],

    # 5/
    # Irregular plurals.
    # (mongoose, oxen).
    [
    ["atlas$", "atlantes", None, True],
    ["atlas$", "atlases", None, False],
    ["beef$", "beeves", None, True],
    ["brother$", "brethren", None, True],
    ["child$", "children", None, False],
    ["corpus$", "corpora", None, True],
    ["corpus$", "corpuses", None, False],
    ["^cow$", "kine", None, True],
    ["ephemeris$", "ephemerides", None, False],
    ["ganglion$", "ganglia", None, True],
    ["genie$", "genii", None, True],
    ["genus$", "genera", None, False],
    ["graffito$", "graffiti", None, False],
    ["loaf$", "loaves", None, False],
    ["money$", "monies", None, True],
    ["mongoose$", "mongooses", None, False],
    ["mythos$", "mythoi", None, False],
    ["octopus$", "octopodes", None, True],
    ["opus$", "opera", None, True],
    ["opus$", "opuses", None, False],
    ["^ox$", "oxen", None, False],
    ["penis$", "penes", None, True],
    ["penis$", "penises", None, False],
    ["soliloquy$", "soliloquies", None, False],
    ["testis$", "testes", None, False],
    ["trilby$", "trilbys", None, False],
    ["turf$", "turves", None, True],
    ["numen$", "numena", None, False],
    ["occiput$", "occipita", None, True],
    ],
    
    # 6/
    # Irregular inflections for common suffixes
    # (synopses, mice, men).
    [
    ["man$", "men", None, False],
    ["person$", "people", None, False],
    ["([lm])ouse$", "\\1ice", None, False],
    ["tooth$", "teeth", None, False],
    ["goose$", "geese", None, False],
    ["foot$", "feet", None, False],
    ["zoon$", "zoa", None, False],
    ["([csx])is$", "\\1es", None, False]
    ],
    
    # 7/
    # Fully assimilated classical inflections
    # (vertebrae, codices).
    [
    ["ex$", "ices", "ex-ices", False],
    ["ex$", "ices", "ex-ices-classical", True],
    ["um$", "a", "um-a", False],
    ["um$", "a", "um-a-classical", True],
    ["on$", "a", "on-a", False],
    ["a$", "ae", "a-ae", False],
    ["a$", "ae", "a-ae-classical", True]
    ],
    
    # 8/
    # Classical variants of modern inflections
    # (stigmata, soprani).
    [
    ["trix$", "trices", None, True],
    ["eau$", "eaux", None, True],
    ["ieu$", "ieu", None, True],
    ["([iay])nx$", "\\1nges", None, True],
    ["en$", "ina", "en-ina-classical", True],
    ["a$", "ata", "a-ata-classical", True],
    ["is$", "ides", "is-ides-classical", True],
    ["us$", "i", "us-i-classical", True],
    ["us$", "us", "us-us-classical", True],
    ["o$", "i", "o-i-classical", True],
    ["$", "i", "-i-classical", True],
    ["$", "im", "-im-classical", True]
    ],
    
    # 9/
    # -ch, -sh and -ss take -es in the plural
    # (churches, classes).
    [
    ["([cs])h$", "\\1hes", None, False],
    ["ss$", "sses", None, False],
    ["x$", "xes", None, False]
    ],
    
    # 10/
    # Certain words ending in -f or -fe take -ves in the plural 
    # (lives, wolves).
    [
    ["([aeo]l)f$", "\\1ves", None, False],
    ["([^d]ea)f$", "\\1ves", None, False],
    ["arf$", "arves", None, False],
    ["([nlw]i)fe$", "\\1ves", None, False],
    ],
    
    # 11/
    # -y takes -ys if preceded by a vowel,
    # or when a proper noun,
    # but -ies if preceded by a consonant
    # (storeys, Marys, stories).
    [
    ["([aeiou])y$", "\\1ys", None, False],
    ["([A-Z].*)y$", "\\1ys", None, False],
    ["y$", "ies", None, False]
    ],
    
    # 12/
    # Some words ending in -o take -os,
    # the rest take -oes.
    # Words in which the -o is preceded by a vowel always take -os
    # (lassos, potatoes, bamboos).
    [
    ["o$", "os", "o-os", False],
    ["([aeiou])o$", "\\1os", None, False],
    ["o$", "oes", None, False]
    ],
    
    # 13/
    # Miltary stuff (Major Generals).
    [
    ["l$", "ls", "general-generals", False]
    ],
    
    # 14/
    # Otherwise, assume that the plural just adds -s 
    # (cats, programmes).
    [
    ["$", "s", None, False]
    ],
]

# Suffix categories

plural_categories = {

          "uninflected" : ["bison", "bream", "breeches", "britches", "carp", "chassis", "clippers", "cod", "contretemps", "corps", "debris", "diabetes", "djinn", "eland", "elk", "flounder", "gallows", "graffiti", "headquarters", "herpes", "high-jinks", "homework", "innings", "jackanapes", "mackerel", "measles", "mews", "mumps", "news", "pincers", "pliers", "proceedings", "rabies", "salmon", "scissors", "series", "shears", "species", "swine", "trout", "tuna", "whiting", "wildebeest"],
          "uncountable" : ["advice", "bread", "butter", "cheese", "electricity", "equipment", "fruit", "furniture", "garbage", "gravel", "happiness", "information", "ketchup", "knowledge", "love", "luggage", "mathematics", "mayonnaise", "meat", "mustard", "news", "progress", "research", "rice", "sand", "software", "understanding", "water"],
           "s-singular" : ["acropolis", "aegis", "alias", "asbestos", "bathos", "bias", "caddis", "cannabis", "canvas", "chaos", "cosmos", "dais", "digitalis", "epidermis", "ethos", "gas", "glottis", "glottis", "ibis", "lens", "mantis", "marquis", "metropolis", "pathos", "pelvis", "polis", "rhinoceros", "sassafras", "trellis"],

              "ex-ices" : ["codex", "murex", "silex"],
    "ex-ices-classical" : ["apex", "cortex", "index", "latex", "pontifex", "simplex", "vertex", "vortex"],
                 "um-a" : ["agendum", "bacterium", "candelabrum", "datum", "desideratum", "erratum", "extremum", "ovum", "stratum"],
       "um-a-classical" : ["aquarium", "compendium", "consortium", "cranium", "curriculum", "dictum", "emporium", "enconium", "gymnasium", "honorarium", "interregnum", "lustrum", "maximum", "medium", "memorandum", "millenium", "minimum", "momentum", "optimum", "phylum", "quantum", "rostrum", "spectrum", "speculum", "stadium", "trapezium", "ultimatum", "vacuum", "velum"],
                 "on-a" : ["aphelion", "asyndeton", "criterion", "hyperbaton", "noumenon", "organon", "perihelion", "phenomenon", "prolegomenon"],
                 "a-ae" : ["alga", "alumna", "vertebra"],
       "a-ae-classical" : ["abscissa", "amoeba", "antenna", "aurora", "formula", "hydra", "hyperbola", "lacuna", "medusa", "nebula", "nova", "parabola"],
       
     "en-ina-classical" : ["foramen", "lumen", "stamen"],
      "a-ata-classical" : ["anathema", "bema", "carcinoma", "charisma", "diploma", "dogma", "drama", "edema", "enema", "enigma", "gumma", "lemma", "lymphoma", "magma", "melisma", "miasma", "oedema", "sarcoma", "schema", "soma", "stigma", "stoma", "trauma"],
    "is-ides-classical" : ["clitoris", "iris"],
       "us-i-classical" : ["focus", "fungus", "genius", "incubus", "nimbus", "nucleolus", "radius", "stylus", "succubus", "torus", "umbilicus", "uterus"],
      "us-us-classical" : ["apparatus", "cantus", "coitus", "hiatus", "impetus", "nexus", "plexus", "prospectus", "sinus", "status"],
        "o-i-classical" : ["alto", "basso", "canto", "contralto", "crescendo", "solo", "soprano", "tempo"],
         "-i-classical" : ["afreet", "afrit", "efreet"],
        "-im-classical" : ["cherub", "goy", "seraph"],

	            "o-os" : ["albino", "archipelago", "armadillo", "commando", "ditto", "dynamo", "embryo", "fiasco", "generalissimo", "ghetto", "guano", "inferno", "jumbo", "lingo", "lumbago", "magneto", "manifesto", "medico", "octavo", "photo", "pro", "quarto", "rhino", "stylo"],

	"general-generals" : ["Adjutant", "Brigadier", "Lieutenant", "Major", "Quartermaster", 
	                      "adjutant", "brigadier", "lieutenant", "major", "quartermaster"],

}

NOUN = "noun"
ADJECTIVE = "adjective"

def plural(word, pos=NOUN, classical=True, custom={}):

	""" Returns the plural of a given word.
	
	For example: child -> children.
	Handles nouns and adjectives, using classical inflection by default
	(e.g. where "matrix" pluralizes to "matrices" instead of "matrixes".
	The custom dictionary is for user-defined replacements.
	
	"""
	
	if word in custom.keys():
		return custom[word]

	# Recursion of genitives
	# remove the apostrophe and any trailing -s, 
	# form the plural of the resultant noun, and then append an apostrophe.
	# (dog's -> dogs')
	if (len(word) > 0 and word[-1] == ",") or \
	   (len(word) > 1 and word[-2:] == "'s"):
		owner = word.rstrip("'s")
		owners = plural(owner, classical, custom)
		if owners[-1] == "s":
			return owners + "'"
		else:
			return owners + "'s"
            
	# Recursion of compound words
	# (Postmasters General, mothers-in-law, Roman deities).    
	words = word.replace("-", " ").split(" ")
	if len(words) > 1:
		if words[1] == "general" or words[1] == "General" and \
		   words[0] not in categories["general-generals"]:
			return word.replace(words[0], plural(words[0], classical, custom))
		elif words[1] in plural_prepositions:
			return word.replace(words[0], plural(words[0], classical, custom))
		else:
			return word.replace(words[-1], plural(words[-1], classical, custom))
    
	# Only a very few number of adjectives inflect.
	n = range(len(plural_rules))
	if pos == ADJECTIVE:
		n = [0, 1]

	import re        
	for i in n:
		ruleset = plural_rules[i]	
		for rule in ruleset:
			suffix, inflection, category, classic = rule
        
			# A general rule,
			# or a classic rule in classical mode.
			if category == None:
				if not classic or (classic and classical):
					if re.search(suffix, word) is not None:
						return re.sub(suffix, inflection, word)
        
			# A rule relating to a specific category of words   
			if category != None:
				if word in plural_categories[category] and (not classic or (classic and classical)):
					if re.search(suffix, word) is not None:
						return re.sub(suffix, inflection, word)
    
	return word
    
#print plural("part-of-speech")
#print plural("child")
#print plural("dog's")
#print plural("wolf")
#print plural("bear")
#print plural("kitchen knife")
#print plural("octopus", classical=True)
#print plural("matrix", classical=True)
#print plural("matrix", classical=False)
#print plural("my", pos=ADJECTIVE)

def noun_plural(word, classical=True, custom={}):
	return plural(word, NOUN, classical, custom)

def adjective_plural(word, classical=True, custom={}):
	return plural(word, ADJECTIVE, classical, custom)