
import sys

import alsaaudio, wave

import numpy as np

import psw
import gapi

import commands

speech = gapi.Speech('en-uk')

if len(sys.argv)==2:
	if sys.argv[1] in gapi.languages.keys():
		speech.lang = gapi.languages[sys.argv[1]]
	elif sys.argv[1] in gapi.languages.values():
		speech.lang = sys.argv[1]

def handler(fileName):
	global speech

	translator = gapi.Translator(speech.lang, 'en-uk')
	try:
		cfileName = psw.convert(fileName)
		phrase = speech.getText(cfileName)
		import os
		os.remove(fileName)
		os.remove(cfileName)
		if phrase!=None:
			phrase = phrase.lower()
			if len(phrase.strip())>0:
				print 'text:',phrase
				#psw.play(speech.getAudio(phrase))
				cmd = translator.translate(phrase).strip().lower()
				print 'cmd:',cmd
				commands.execute(cmd, speech)
	except Exception, e:
		print "Unexpected error:", sys.exc_info()[0], e
	return True


mic = psw.Microphone()
print 'sampling...'
sample = np.array(mic.sample(200))
print 'done'

#import matplotlib.pyplot as plt
#plt.plot(sample)
#plt.show()
#from scipy import ndimage
#sample = ndimage.gaussian_filter(sample, sigma=3)
#plt.plot(sample)
#plt.show()

mic.listen(handler, sample.mean(), sample.std())
