# -*- coding: utf-8 -*-
from twisted.internet import reactor
from random import choice
#youtube
import simplejson
import urllib
import re
#food
from datetime import datetime

class shesaid(object):
	def __init__(self,config):
		self.enabled = True
		self.rate = int(config.get('shesaid','rate',0))
		triggers = config.get('shesaid','triggers')
		self.triggers = triggers.split('\n')
		quotesFile = 'quotes.txt'
		with open(quotesFile) as quotesFileObj:
			self.quotes = quotesFileObj.readlines()

	def run(self,user,msg):
		self.enabled = False
		#schedule this module to be reenabled after 'self.rate' seconds
		reactor.callLater(self.rate,lambda:self.enable())
		return choice(self.quotes)

	def enable(self):
		self.enabled = True


class youtube(object):
	def __init__(self,config):
		self.enabled = True
		self.rate = int(config.get('youtube','rate',0))
		triggers = config.get('youtube','triggers')
		self.triggers = triggers.split('\n')

	def run(self,user,msg):
		self.enabled = False
		#schedule this module to be reenabled after 'self.rate' seconds
		reactor.callLater(self.rate,lambda:self.enable())
		
		id = re.match(".*?v=([a-zA-Z0-9_-]{11}).*",str(msg))
		if id:
			id = id.group(1)
			url = 'http://gdata.youtube.com/feeds/api/videos/%s?alt=json&v=2' % id 
			try:
				video = simplejson.load(urllib.urlopen(url))
			except:
				pass

			try:
				ups = video['entry']['yt$rating']['numLikes']
				downs = video['entry']['yt$rating']['numDislikes']
				rating=round(float(ups)/(int(ups)+int(downs)),2)*100;
				ratings=str(int(ups)+int(downs))
			except:
				rating='0'
				ratings='0'
			title = video['entry']['title']['$t']
			views = video['entry']['yt$statistics']['viewCount']
			return(u'▷ '.encode('utf-8')+ title +" - " + views +" views"+" - "+"Rating " + str(rating)+"% - "+ratings+" ratings"+u' ◁'.encode('utf-8'))

	def enable(self):
		self.enabled = True




