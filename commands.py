import numpy as np

import nltk
import nlpy
import en

import psw
import gapi

import player

songPlayer = player.Player()
player.init()

import subprocess
from grooveshark import Client
songClient = Client()
songClient.init()

from sets import Set

def matchWord(tokens, words):
	s = Set(tokens).intersection(Set(words))
	if len(s)>0:
		return [(w,1.0,w) for w in s]
	else:
		from nltk.metrics import distance
		import operator
		result = []
		for token in Set(tokens):
			vals = {w : (1.0-float(distance.edit_distance(token, w))/float(max(len(token),len(w)))) for w in words}
			sortedvals = sorted(vals.iteritems(), key=operator.itemgetter(1),reverse=True)
			result.append( (token, sortedvals[0][1], sortedvals[0][0]) )
		return sorted(result, key=lambda tup: tup[1], reverse=True)

def matchMeaning(tokens, words):
	s = Set(tokens).intersection(Set(words))
	if len(s)>0:
		return [(w,1.0) for w in s]
	else:
		from nltk.metrics import distance
		import operator

		tokens = Set(tokens)
		words = Set(words)

		extendedWords = {}
		for w in words:
			extwords = []			
			extwords.extend([w])
			extwords.extend(nlpy.autoWordToNoun(w))
			extwords.extend(nlpy.autoWordToVerb(w))
			extendedWords[w] = Set(extwords)
		result = []
		for token in tokens:
			extwords = []			
			extwords.extend([token])
			extwords.extend(nlpy.autoWordToNoun(token))
			extwords.extend(nlpy.autoWordToVerb(token))
			count = sum([1 for w in words if len(extendedWords[w].intersection(Set(extwords)))>0])
			result.append((token, float(count)/float(len(words))))
		return sorted(result, key=lambda tup: tup[1], reverse=True)

stopwords = nltk.corpus.stopwords.words('english')

def scoreExactPhrase(tokens, phrase):
	score = np.mean([p[1] for p in phrase])
	remaining = Set(tokens).difference(Set([p[0] for p in phrase]))
	global stopwords
	remaining = remaining.difference(Set(w for w in remaining if w in stopwords))
	return score*(1-float(len(remaining))/float(len(Set(tokens))))

def scoreQuery(tokens, phrase):
	score = np.mean([p[1] for p in phrase])
	remaining = Set(tokens).difference(Set([p[0] for p in phrase]))
	#global stopwords
	#remaining = remaining.difference(Set(w for w in remaining if w in stopwords))
	return (score, [w for w in tokens if w in remaining])

def changeLanguage(tokens, languages):
	phrase = []
	phrase.append( matchMeaning(tokens,['switch','change','exchange','modify'])[0] )
	phrase.append( matchWord(tokens,['language'])[0] )
	lang = matchWord(tokens,languages)[0]
	phrase.append( lang )
	score = scoreExactPhrase(tokens, phrase)
	return (score, lang[2] )

def openProgram(tokens, programs):
	phrase = []
	phrase.append( matchMeaning(tokens,['execute','start','open','run'])[0] )
	prog = matchWord(tokens,programs)[0]
	phrase.append( prog )
	score = scoreExactPhrase(tokens, phrase)
	return (score, prog[2] )

def closeProgram(tokens, programs):
	phrase = []
	phrase.append( matchMeaning(tokens,['finish','close','terminate','exit','quit'])[0] )
	prog = matchWord(tokens,programs)[0]
	phrase.append( prog )
	score = scoreExactPhrase(tokens, phrase)
	return (score, prog[2] )

def whatTime(tokens):
	phrase = []
	phrase.append( matchWord(tokens,['how','what','tell'])[0] )
	time = matchWord(tokens,['time','hours'])[0]
	phrase.append( time )
	score = scoreExactPhrase(tokens, phrase)
	return (score, time[0] )

def whatDay(tokens):
	phrase = []
	phrase.append( matchWord(tokens,['what'])[0] )
	date = matchWord(tokens,['day','date'])[0]
	phrase.append( date )
	phrase.append( matchWord(tokens,['today','it'])[0] )
	score = scoreExactPhrase(tokens, phrase)
	return (score, date[0] )

def playSong(tokens):
	phrase = []
	phrase.append( matchWord(tokens,['play'])[0] )
	phrase.append( matchWord(tokens,['song','music'])[0] )
	phrase.append( matchWord(tokens,['by','from'])[0] )
	score1 = scoreQuery(tokens, phrase)

	phrase = []
	phrase.append( matchWord(tokens,['play'])[0] )
	phrase.append( matchWord(tokens,['song','music'])[0] )
	score2 = scoreQuery(tokens, phrase)
	if score1[0]>=score2[0]:
		return (score1[0], score1[1], 'artist')
	else:
		return (score2[0], score2[1], 'song')

def pauseSong(tokens):
	phrase = []
	phrase.append( matchMeaning(tokens,['pause', 'stop', 'finish', 'close'])[0] )
	phrase.append( matchWord(tokens,['song','music'])[0] )
	score = scoreExactPhrase(tokens, phrase)
	return (score, 'pause')

def nextSong(tokens):
	phrase = []
	phrase.append( matchWord(tokens,['next', 'change'])[0] )
	phrase.append( matchWord(tokens,['song','music'])[0] )
	score = scoreExactPhrase(tokens, phrase)
	return (score, 'next')


def previousSong(tokens):
	phrase = []
	phrase.append( matchWord(tokens,['previous'])[0] )
	phrase.append( matchWord(tokens,['song','music'])[0] )
	score = scoreExactPhrase(tokens, phrase)
	return (score, 'previous')

def wakeUp(tokens):
	phrase = []
	phrase.append( matchMeaning(tokens,['wake','awake'])[0] )
	phrase.append( matchWord(tokens,['up','awake'])[0] )
	score = scoreExactPhrase(tokens, phrase)
	return (score, 'awake')


def goSleep(tokens):
	phrase = []
	phrase.append( matchMeaning(tokens,['sleep'])[0] )
	phrase.append( matchWord(tokens,['go','sleep'])[0] )
	score = scoreExactPhrase(tokens, phrase)
	return (score, 'sleep')

def whatIs(tokens):
	phrase = []
	phrase.append( matchWord(tokens,['who','what','which'])[0] )
	phrase.append( matchMeaning(tokens,['are','is'])[0] )
	score = scoreQuery(tokens, phrase)
	return score

def doChangeLanguage(text, score, speech, translator):
	lang = score[1]
	print lang
	speech.lang = gapi.languages[lang]
	translator.to_lang = gapi.languages[lang]
	psw.play(speech.getAudio(translator.translate('language changed to '+lang)))

def doOpenProgram(text, score, speech, translator):
	openAppList = {'editor': 'gedit', 'browser':'google-chrome', 'console':'gnome-terminal', 'calculator':'gnome-calculator'}
	prog = score[1]
	psw.play(speech.getAudio(translator.translate('I will open the '+prog)))
	from os import system
	system('nohup '+openAppList[prog]+' &')

def doCloseProgram(text, score, speech, translator):
	closeAppList = {'editor': 'gedit', 'browser':'chrome', 'console':'gnome-terminal', 'calculator':'gnome-calculator'}
	prog = score[1]
	psw.play(speech.getAudio(translator.translate('I will close the '+prog)))
	from os import system
	system('killall '+closeAppList[prog])

def doWhatTime(text, score, speech, translator):
	import time
	ts = time.time()
	import datetime
	st = datetime.datetime.fromtimestamp(ts).strftime('It is %-H hours and %-M minutes')
	psw.play(speech.getAudio(translator.translate(st)))

def doWhatDay(text, score, speech, translator):
	import time
	ts = time.time()
	import datetime
	st = datetime.datetime.fromtimestamp(ts).strftime('Today is %A, %-d. %B %Y')
	psw.play(speech.getAudio(translator.translate(st)))

def doPlaySong(text, score, speech, translator):
	if score[2]=='song':
		if len(score[1])>0:
			songs = list(songClient.search(' '.join(score[1])))
			#song = songs[0]
			print 'Found',len(songs),'songs'
			#subprocess.call(['cvlc', song.stream.url])
			#subprocess.call(['mplayer', song.stream.url])
			songPlayer.play(songs)
		else:
			songPlayer.play()
	elif score[2]=='artist':
		songs = list(list(songClient.search(' '.join(score[1]),Client.ARTISTS))[0].songs)
		#n = int(np.random.rand()*len(songs))
		#song = songs[n]
		print 'Found',len(songs),'songs'
		songPlayer.play(songs)
		#print 'Playing song',n
		#print str(song), song.duration
		#subprocess.call(['cvlc',song.stream.url])
		#subprocess.call(['mplayer',song.stream.url])
		#player.set_state(gst.STATE_NULL)
		#player.set_property('uri',song.stream.url)
		#player.set_state(gst.STATE_PLAYING)

def doPauseSong(text, score, speech, translator):
	songPlayer.pause()

def doNextSong(text, score, speech, translator):
	songPlayer.next()

def doPreviousSong(text, score, speech, translator):
	songPlayer.previous()

isAwaken = True
def doWakeUp(text, score, speech, translator):
	global isAwaken
	isAwaken = True
	psw.play(speech.getAudio(translator.translate('Hi, I am back')))

def doGoSleep(text, score, speech, translator):
	global isAwaken
	isAwaken = False
	psw.play(speech.getAudio(translator.translate('I am going to sleep')))

def clearText(text,left, right):
	ctext = ''
	idx = 0
	for c in unicode(text):
		if c==left:
			idx += 1
		elif c==right:
			idx -= 1
		elif idx==0:
			ctext += c
	return ctext

def doWhatIs(text, score, speech, translator):
	query = ' '.join(score[1]).strip()
	if query=='you':
		psw.play(speech.getAudio(translator.translate('My name is Nati, a Natural interface.')))
	else:
		import wikipedia
		titles = wikipedia.search(query)
		#print titles
		#score = matchWord([query], titles)
		#print score
		#print wikipedia.summary(score[0][2])
		text = wikipedia.summary(titles[0])
		#print text
		print translator.translate(text)
		text = clearText(text, '(',')')
		text = clearText(text, '[',']')
		import re
		text = re.sub(re.compile(u"/[^/]+/"), " ", text)
		text = text.replace(',',' ')
		phrase = text.split('.')[0]
		print '*',phrase
		psw.play(speech.getAudio(translator.translate(phrase)))

def execute(text, speech):
	translator = gapi.Translator('en-uk', speech.lang)
	global isAwaken

	from os import system
	import sys

	openAppList = {'editor': 'gedit', 'browser':'google-chrome', 'console':'gnome-terminal', 'calculator':'gnome-calculator'}
	closeAppList = {'editor': 'gedit', 'browser':'chrome', 'console':'gnome-terminal', 'calculator':'gnome-calculator'}

	from nltk.tokenize import RegexpTokenizer
	tokenizer = RegexpTokenizer(r'\w+')

	tokens = tokenizer.tokenize(text)

	if isAwaken:
		cmds = ['goSleep','changeLanguage','openProgram','closeProgram','whatTime','whatDay','playSong','pauseSong','nextSong','previousSong','whatIs']
		cmd = {}
		cmd['changeLanguage'] = changeLanguage(tokens, gapi.languages.keys())
		cmd['openProgram'] = openProgram(tokens, openAppList.keys())
		cmd['closeProgram'] = closeProgram(tokens, closeAppList.keys())
		cmd['whatTime'] = whatTime(tokens)
		cmd['whatDay'] = whatDay(tokens)
		cmd['playSong'] = playSong(tokens)
		cmd['pauseSong'] = pauseSong(tokens)
		cmd['nextSong'] = nextSong(tokens)
		cmd['previousSong'] = previousSong(tokens)
		cmd['goSleep'] = goSleep(tokens)
		cmd['whatIs'] = whatIs(tokens)

		maxScore = 0
		maxCmd = None
		for c in cmds:
			s = cmd[c]
			if s[0]>maxScore:
				maxScore = s[0]
				maxCmd = c
		print 'do command:',maxCmd,maxScore

		if maxScore>0.7:
			if maxCmd=='changeLanguage':
				doChangeLanguage(text, cmd[maxCmd], speech, translator)
			elif maxCmd=='openProgram':
				doOpenProgram(text, cmd[maxCmd], speech, translator)
			elif maxCmd=='closeProgram':
				doCloseProgram(text, cmd[maxCmd], speech, translator)
			elif maxCmd=='whatTime':
				doWhatTime(text, cmd[maxCmd], speech, translator)
			elif maxCmd=='whatDay':
				doWhatDay(text, cmd[maxCmd], speech, translator)
			elif maxCmd=='playSong':
				doPlaySong(text, cmd[maxCmd], speech, translator)
			elif maxCmd=='pauseSong':
				doPauseSong(text, cmd[maxCmd], speech, translator)
			elif maxCmd=='nextSong':
				doNextSong(text, cmd[maxCmd], speech, translator)
			elif maxCmd=='previousSong':
				doPreviousSong(text, cmd[maxCmd], speech, translator)
			elif maxCmd=='goSleep':
				doGoSleep(text, cmd[maxCmd], speech, translator)
			elif maxCmd=='whatIs':
				doWhatIs(text, cmd[maxCmd], speech, translator)
			else:
				print 'command not known:',text
		else:
			print 'command not known:',text
	else:
		score = wakeUp(tokens)
		print 'do command: wakeUp',score[0]
		if score[0]>0.7:
			doWakeUp(text, score, speech, translator)
		else:
			print 'command not known:',text
		
