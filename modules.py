# -*- coding: utf-8 -*-
#Modules for pepperoni bot - Modules must begin with module_
from twisted.internet import reactor
from random import choice
#youtube
import simplejson
import urllib
import re
#food
from datetime import datetime

class module_shesaid(object):
	def __init__(self,config):
		self.enabled = True
		self.rate = int(config.get('shesaid','rate',0))
		triggers = config.get('shesaid','triggers')
		self.triggers = triggers.split('\n')
		quotesFile = 'quotes.txt'
		with open(quotesFile) as quotesFileObj:
			self.quotes = quotesFileObj.readlines()

	def enable(self):
		self.enabled = True

	def run(self,bot):
		self.enabled = False
		#schedule this module to be reenabled after 'self.rate' seconds
		reactor.callLater(self.rate,lambda:self.enable())
		bot.msg(bot.channel,choice(self.quotes))


class module_youtube(object):
	def __init__(self,config):
		self.enabled = True
		self.rate = int(config.get('youtube','rate',0))
		triggers = config.get('youtube','triggers')
		self.triggers = triggers.split('\n')

	def enable(self):
		self.enabled = True

	def run(self,bot):
		self.enabled = False
		#schedule this module to be reenabled after 'self.rate' seconds
		reactor.callLater(self.rate,lambda:self.enable())
		
		id = re.match(".*?v=([a-zA-Z0-9_-]{11}).*",str(bot.chat))
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
			bot.msg(bot.channel,u'▷ '.encode('utf-8')+ title +" - " + views +" views"+" - "+"Rating " + str(rating)+"% - "+ratings+" ratings"+u' ◁'.encode('utf-8'))


class module_food(object):
	def __init__(self,config):
		self.enabled = False
		self.rate = int(config.get('food','rate',0))
		triggers = config.get('food','triggers')
		self.triggers = triggers.split('\n')
		self.acceptable_courts = ["hillenbrand","ford","wiley","earhart","windsor"]
		self.acceptable_mealtimes = acceptable_mealtime=["Lunch","Dinner","Breakfast"]

	def enable(self):
		self.enabled = False
	
	def foodHelp(bot):
		bot.notice(bot.user," Usage: !food COURT [MEAL] [YYYY-MM-DD]")
		bot.notice(bot.user," Example usage: !food hillenbrand")
		bot.notice(bot.user," Example usage: !food hillenbrand lunch 2013-12-29")
		return

	def run(self,bot):
		self.enabled = False
		#schedule this module to be reenabled after 'self.rate' seconds
		reactor.callLater(self.rate,lambda:self.enable())
		
		params = chat.split(' ')

		if len(params) < 2 or 'help' in params or '-h' in params:
			foodHelp(bot)
			return

		for param in params:
			if param.lower() in self.acceptable_courts:
				court = param.lower()
			if param.title() in self.acceptable_mealtimes:
				meal = param.title()
			if re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}',param.lower()):
				day = datetime.strptime(param,'%Y-%m-%d')
		if not court:
			foodHelp(bot)
		if not meal:
			time = datetime.now()
			hour = time.strftime('%H')
			if hour > 14:
				meal = 'Dinner'
			elif hour > 10:
				meal = 'Lunch'
			else:
				meal = 'Breakfast' 

			if not day:
				day = time
		else:
			if not day:
				foodHelp(bot)


