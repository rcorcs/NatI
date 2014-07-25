import alsaaudio, wave
import numpy as np
#python sound wave

import string

def _randstr(size=6, chars=string.ascii_uppercase + string.digits):
	import random
	return ''.join(random.choice(chars) for _ in range(size))

def convert(fileName):
	from os import system
	cFileName = fileName
	if cFileName.endswith('.wav'):
		cFileName = cFileName[:-4]+'.flac'
	system("sox %s -t wav -r 8000 -t flac %s" % (fileName, cFileName))
	return cFileName

def play(filename):
	"""
	Plays an mp3 depending on the system.
	"""
	import sys
	import subprocess

	if sys.platform == "linux" or sys.platform == "linux2":
		# linux
		subprocess.call(["play", '-q', filename])
	elif sys.platform == "darwin":
		# OS X
		subprocess.call(["afplay", filename])
		# only 32 bit windows, but a lot of win x86_64
		# py installs are 32bit. Too much work for _64 fix
	elif sys.platform == 'win32':
		print ("trying windows default")
		subprocess.call(["WMPlayer", filename])

class Microphone:
	def __init__(self):
		self.start()

	def start(self):
		self.inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE)
		self.inp.setchannels(1)
		self.inp.setrate(44100)
		self.inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
		self.inp.setperiodsize(1024)

	def sample(self, n=100):
		sample = []
		while len(sample)<200:
			l, data = self.inp.read()
			a = np.fromstring(data, dtype='int16')
			sample.append(np.abs(a).mean())
		return sample

	def listen(self, handler, noiseMean=140, noiseStd=30, factor=5):
		#import os
		import sys

		fileName = '.'+_randstr(size=10)+'.wav'
		w = wave.open(fileName, 'w')
		w.setnchannels(1)
		w.setsampwidth(2)
		w.setframerate(44100)

		buff = []
		notSpeaking = 100
		while True:
			l, data = self.inp.read()
			a = np.fromstring(data, dtype='int16')
			if np.abs(a).mean()>(noiseMean+factor*noiseStd):
				sys.stdout.write('.')
				sys.stdout.flush()
				for d in buff:
					w.writeframes(d)
				w.writeframes(data)
				notSpeaking = 0
				buff = []
			else:
				notSpeaking += 1
				buff.append(data)
				if len(buff)>10:
					buff.pop(0)
				if notSpeaking<50:
					w.writeframes(data)
				elif notSpeaking==50:
					print '.'
					w.close()
					#self.inp.close()
					if not handler(fileName):
						break
					#os.remove(fileName)
					#self.start()
					fileName = '.'+_randstr(size=10)+'.wav'
					w = wave.open(fileName, 'w')
					w.setnchannels(1)
					w.setsampwidth(2)
					w.setframerate(44100)
					notSpeaking = 100
