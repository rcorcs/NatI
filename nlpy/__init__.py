import nltk
import en
import string
import sets
import unicodedata
import random

import pynumber


number = pynumber

def lexicalDiversity(text):
	return len(text) / len(set(text))

def verbToNoun(verb):
	nounsTemp = []
	for val in [(w, w.derivationally_related_forms()) for w in nltk.corpus.wordnet.lemmas(en.verb.infinitive(verb))]:
		nounsTemp.append(set([(w.name).lower() for w in val[1] if '.n.' in str(w)]))
	nouns = []
	for s in nounsTemp:
		for w in s:
			nouns.append(w)
	return list(set(nouns))

def autoWordToNoun(rawword):
	word = rawword
	infVerb = en.verb.infinitive(rawword)
	if infVerb!='' and en.is_verb(infVerb):
		word = infVerb 
	nounsTemp = []
	for val in [(w, w.derivationally_related_forms()) for w in nltk.corpus.wordnet.lemmas(word)]:
		nounsTemp.append(set([(w.name).lower() for w in val[1] if '.n.' in str(w)]))

	for synword in nltk.corpus.wordnet.synsets(word):
		for val in [(w, w.derivationally_related_forms()) for w in synword.lemmas]:
			nounsTemp.append(set([(w.name).lower() for w in val[1] if '.n.' in str(w)]))

	nouns = []
	for s in nounsTemp:
		for w in s:
			nouns.append(w)
	return list(set(nouns))

def autoWordToVerb(rawword):
	word = rawword
	infVerb = en.verb.infinitive(rawword)
	if infVerb!='' and en.is_verb(infVerb):
		word = infVerb 
	nounsTemp = []
	for val in [(w, w.derivationally_related_forms()) for w in nltk.corpus.wordnet.lemmas(word)]:
		nounsTemp.append(set([(w.name).lower() for w in val[1] if '.v.' in str(w)]))

	for synword in nltk.corpus.wordnet.synsets(word):
		for val in [(w, w.derivationally_related_forms()) for w in synword.lemmas]:
			nounsTemp.append(set([(w.name).lower() for w in val[1] if '.v.' in str(w)]))

	nouns = []
	for s in nounsTemp:
		for w in s:
			nouns.append(w)
	return list(set(nouns))

def autoPlural(word):
	if en.is_adjective(word):
		return en.plural.adjective_plural(word)
	else:
		return en.plural.noun_plural(word)

def autoLemmatize(word):
	wnl = nltk.stem.wordnet.WordNetLemmatizer()
	infVerb = en.verb.infinitive(word)
	if infVerb!='' and en.is_verb(infVerb):
		return wnl.lemmatize(infVerb, 'v')
	else:
		return wnl.lemmatize(word)

def correctSpelling(phrase):
	corrected = ''
	for word in phrase.split():
		suggestion = en.spelling.suggest(word)
		corrected = corrected + suggestion[0] + ' '
	return string.strip(corrected)


def __toAscii(uc):
	return uc.encode("ascii", "ignore")

def __removeAccents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

def unicodeToAscii(inputStr):
    return str(__toAscii(__removeAccents(inputStr)))

def dateToStr(date):
	d = date.split('-')
	months = ["January", "February", "March", "April", "May", "June", "July", "August", "Steptember", "October", "November", "December"]
	if len(d)>=3:
		return d[2]+" of "+months[int(d[1])-1]+" "+d[0]
	else:
		return ''

###################################
### TEST OF SOME PIECES OF CODE
###################################

def genderFeatures(word):
	w = word.lower().strip()
	#return {'prefix1': w[0], 'prefix2': w[1], 'suffix1':w[-1], 'suffix2':w[-2]}
	return {'suffix1':w[-1], 'suffix2':w[-2]}

def nameClassifier():
	names = ([(name, 'male') for name in nltk.corpus.names.words('male.txt')]+[(name, 'female') for name in nltk.corpus.names.words('female.txt')])
	random.shuffle(names)
	featuresets = [(genderFeatures(n), g) for (n,g) in names]
	train_set, test_set = featuresets[500:], featuresets[:500]
	classifier = nltk.NaiveBayesClassifier.train(train_set)
	print nltk.classify.accuracy(classifier, test_set)
	return classifier

def documentFeatures(document, wordFeatures):
	document_words = set(document)
	features = {}
	for word in wordFeatures:
		features['contains(%s)' % word] = (word in document_words)
	return features

def filmClassifier():
	documents = [(list(nltk.corpus.movie_reviews.words(fileid)), category) for category in nltk.corpus.movie_reviews.categories() for fileid in nltk.corpus.movie_reviews.fileids(category)]
	random.shuffle(documents)
	#stopwords = nltk.corpus.stopwords.words('english')
	#all_words = nltk.FreqDist(w.lower() for w in nltk.corpus.movie_reviews.words() if w.lower() not in stopwords)
	all_words = nltk.FreqDist(w.lower() for w in nltk.corpus.movie_reviews.words())
	wordFeatures = all_words.keys()[:2000]

	featuresets = [(documentFeatures(d, wordFeatures), c) for (d,c) in documents]
	train_set, test_set = featuresets[100:], featuresets[:100]
	classifier = nltk.NaiveBayesClassifier.train(train_set)
	print nltk.classify.accuracy(classifier, test_set)
	classifier.show_most_informative_features(5)

def chunking(sentence):
	grammar = "NP: {<DT>?<JJ.*>*<NN.*>+}"
	cp = nltk.RegexpParser(grammar)
	result = cp.parse(sentence)
	return result

def testChunking():
	text = 'Has Michael Caine portrayed Alfred Pennyworth?'
	result = chunking(nltk.pos_tag(nltk.word_tokenize(text)))
	return result

class UnigramChunker(nltk.ChunkParserI):
	def __init__(self, train_sents):
		train_data = [[(t,c) for w,t,c in nltk.chunk.tree2conlltags(sent)] for sent in train_sents]
		self.tagger = nltk.UnigramTagger(train_data)

	def parse(self, sentence):
		pos_tags = [pos for (word,pos) in sentence]
		tagged_pos_tags = self.tagger.tag(pos_tags)
		chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
		conlltags = [(word, pos, chunktag) for ((word,pos),chunktag) in zip(sentence, chunktags)]
		return nltk.chunk.conlltags2tree(conlltags)

def evaluateUnigramChunker():
	test_sents = nltk.corpus.conll2000.chunked_sents('test.txt', chunk_types=['NP'])
	train_sents = nltk.corpus.conll2000.chunked_sents('train.txt', chunk_types=['NP'])
	unigram_chunker = UnigramChunker(train_sents)
	print unigram_chunker.evaluate(test_sents)

def testUnigramChunker(text=None):
	if text==None:
		text = 'Has Michael Caine portrayed Alfred Pennyworth?'

	train_sents = nltk.corpus.conll2000.chunked_sents('train.txt', chunk_types=['NP'])
	unigram_chunker = UnigramChunker(train_sents)
	result = unigram_chunker.parse(nltk.pos_tag(nltk.word_tokenize(text)))
	return result

def npchunk_features(sentence, i, history):
	word, pos = sentence[i]
	if i == 0:
		prevword, prevpos = "<START>", "<START>"
	else:
		prevword, prevpos = sentence[i-1]
	if i == len(sentence)-1:
		nextword, nextpos = "<END>", "<END>"
	else:
		nextword, nextpos = sentence[i+1]
	return {"pos": pos, "word": word, "prevpos": prevpos, "nextpos": nextpos, "prevpos+pos": "%s+%s" % (prevpos, pos), "pos+nextpos": "%s+%s" % (pos, nextpos), "tags-since-dt": tags_since_dt(sentence, i)}

def tags_since_dt(sentence, i):
	tags = set()
	for word, pos in sentence[:i]:
		if pos == 'DT':
			tags = set()
		else:
			tags.add(pos)
	return '+'.join(sorted(tags))

class ConsecutiveNPChunkTagger(nltk.TaggerI):
	def __init__(self, train_sents):
		train_set = []
		for tagged_sent in train_sents:
			untagged_sent = nltk.tag.untag(tagged_sent)
			history = []
			for i, (word, tag) in enumerate(tagged_sent):
				featureset = npchunk_features(untagged_sent, i, history)
				train_set.append( (featureset, tag) )
				history.append(tag)
		self.classifier = nltk.MaxentClassifier.train(train_set, algorithm='megam', trace=0)

	def tag(self, sentence):
		history = []
		for i, word in enumerate(sentence):
			featureset = npchunk_features(sentence, i, history)
			tag = self.classifier.classify(featureset)
			history.append(tag)
		return zip(sentence, history)

class ConsecutiveNPChunker(nltk.ChunkParserI):
	def __init__(self, train_sents):
		tagged_sents = [[((w,t),c) for (w,t,c) in nltk.chunk.tree2conlltags(sent)] for sent in train_sents]
		self.tagger = ConsecutiveNPChunkTagger(tagged_sents)

	def parse(self, sentence):
		tagged_sents = self.tagger.tag(sentence)
		conlltags = [(w,t,c) for ((w,t),c) in tagged_sents]
		return nltk.chunk.conlltags2tree(conlltags)

def evaluateConsecutiveChunker():
	test_sents = nltk.corpus.conll2000.chunked_sents('test.txt', chunk_types=['NP'])
	train_sents = nltk.corpus.conll2000.chunked_sents('train.txt', chunk_types=['NP'])
	chunker = ConsecutiveNPChunker(train_sents)
	print chunker.evaluate(test_sents)

def neChunking(text):
	return nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(text)))

#print('was', autoLemmatize('was'))
#print('computers', autoLemmatize('computers'))
#print('saw', autoLemmatize('saw'))
#print('done', autoLemmatize('done'))
#print('june', autoLemmatize('june'))
#print('tree', autoLemmatize('tree'))
#print('spoken', autoLemmatize('spoken'))
#print('Einstein', autoLemmatize('Einstein'))
#print('Turing', autoLemmatize('Turing'))
#print('NASA', autoLemmatize('NASA'))
#print('algol', autoLemmatize('algol'))
#print('php', autoLemmatize('php'))

#print('child', autoPlural('child'))
#print('woman', autoPlural('woman'))
#print('fan', autoPlural('fan'))
#print('machine', autoPlural('machine'))
#print('book', autoPlural('book'))

#phrase = 'cmoputer'
#print(phrase, correctSpelling(phrase))

#phrase = 'studen'
#print(phrase, correctSpelling(phrase))

#phrase = 'studetn'
#print(phrase, correctSpelling(phrase))

#phrase = 'Einstein'
#print(phrase, correctSpelling(phrase))

#phrase = 'NASA'
#print(phrase, correctSpelling(phrase))

#phrase = 'Turing'
#print(phrase, correctSpelling(phrase))

#phrase = 'algol'
#print(phrase, correctSpelling(phrase))

#phrase = 'php'
#print(phrase, correctSpelling(phrase))

#phrase = 'i broken my compuetr'
#print(phrase, correctSpelling(phrase))
#
#print(en.sentence.tag(correctSpelling(phrase)))

