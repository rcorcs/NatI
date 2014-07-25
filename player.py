import pygst
pygst.require('0.10')
import gst
import gobject

class Player:
	def __init__(self):
		self.songs = []
		self.current = 0
		self.player = gst.element_factory_make("playbin2", "player")
		#pulse = gst.element_factory_make("pulsesink", "pulse")
		#fakesink = gst.element_factory_make("fakesink", "fakesink")
		#self.player.set_property("audio-sink", pulse)
		#self.player.set_property("video-sink", fakesink)
		bus = self.player.get_bus()
		bus.add_signal_watch()
		#bus.enable_sync_message_emission()	
		bus.connect("message", self.on_message)
		#bus.connect('message::eos', on_EOS)

	def on_message(self, bus, message):
		#print 'msg:',str(message)
		t = message.type
		if t == gst.MESSAGE_EOS:
			self.player.set_state(gst.STATE_NULL)
			self.current += 1
			if self.current<len(self.songs):
				self._play_current()
				self.player.set_state(gst.STATE_PLAYING)
			else:
				self.current = 0
			#print 'END of audio'
		elif t == gst.MESSAGE_ERROR:
			self.player.set_state(gst.STATE_NULL)
			err, debug = message.parse_error()
			print "Error: %s" % err, debug
	
	def play(self, song=None):
		if song!=None:
			self.player.set_state(gst.STATE_NULL)
			if isinstance(song, list):
				self.songs = song
			else:
				self.songs = [song]
			self.current = 0
			self._play_current()
		self.player.set_state(gst.STATE_PLAYING)

	def _play_current(self):
		import grooveshark
		song = self.songs[self.current]
		if isinstance(song, grooveshark.classes.Song):
			import locale
			print 'Playing song:',unicode(song).encode(locale.getpreferredencoding())
			song = song.stream.url
		self.player.set_property('uri', song)

	def next(self):
		self.current += 1
		self.player.set_state(gst.STATE_NULL)
		if self.current<len(self.songs):
			self._play_current()
			self.player.set_state(gst.STATE_PLAYING)
		else:
			self.current = 0
	
	def previous(self):
		self.current -= 1
		self.player.set_state(gst.STATE_NULL)
		if self.current<len(self.songs) and self.current>=0:
			self._play_current()
			self.player.set_state(gst.STATE_PLAYING)
		else:
			self.current = 0

	def pause(self):
		self.player.set_state(gst.STATE_PAUSED)


def init():
	gobject.threads_init()
	import threading
	mainloop = gobject.MainLoop()
	t = threading.Thread(target=mainloop.run, args=())
	t.start()

#player = Player()
#init()
#from grooveshark import Client
#client = Client()
#client.init()
#songs = list(client.popular())
#player.play(songs)
#while True:
#	continue
