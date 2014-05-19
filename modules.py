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

class module_reload(object):
	def __init__(self,config,bot):
		self.enabled = True
		self.rate = int(config.get('reload','rate',0))
		self.bot = bot
		triggers = config.get('reload','triggers')
		self.triggers = triggers.split('\n')

	def enable(self):
		self.enabled = True

	def run(self):
		self.enabled = False
		#schedule this module to be reenabled after 'self.rate' seconds
		reactor.callLater(self.rate,lambda:self.enable())
		if self.bot.user == 'Evidlo':
				self.bot.loadModules()
				self.bot.msg(self.bot.channel,u'▷ '.encode('utf-8')+'Reloaded all modules'+u' ◁'.encode('utf-8'))
		return
	
class module_shesaid(object):
	def __init__(self,config,bot):
		self.enabled = True
		self.rate = int(config.get('shesaid','rate',0))
		self.bot = bot
		triggers = config.get('shesaid','triggers')
		self.triggers = triggers.split('\n')
		quotesFile = 'quotes.txt'
		with open(quotesFile) as quotesFileObj:
			self.quotes = quotesFileObj.readlines()

	def enable(self):
		self.enabled = True

	def run(self):
		self.enabled = False
		#schedule this module to be reenabled after 'self.rate' seconds
		reactor.callLater(self.rate,lambda:self.enable())
		self.bot.msg(self.bot.channel,choice(self.quotes))


class module_youtube(object):
	def __init__(self,config,bot):
		self.enabled = True
		self.rate = int(config.get('youtube','rate',0))
		self.bot = bot
		triggers = config.get('youtube','triggers')
		self.triggers = triggers.split('\n')

	def enable(self):
		self.enabled = True

	def run(self):
		self.enabled = False
		#schedule this module to be reenabled after 'self.rate' seconds
		reactor.callLater(self.rate,lambda:self.enable())
		
		id = re.match(".*?v=([a-zA-Z0-9_-]{11}).*",str(self.bot.chat))
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
			self.bot.msg(self.bot.channel,u'▷ '.encode('utf-8')+ title +" - " + views +" views"+" - "+"Rating " + str(rating)+"% - "+ratings+" ratings"+u' ◁'.encode('utf-8'))


class module_food(object):
	def __init__(self,config,bot):
		self.enabled = True
		self.rate = int(config.get('food','rate',0))
		self.bot = bot
		triggers = config.get('food','triggers')
		self.triggers = triggers.split('\n')
		self.acceptable_courts = ["hillenbrand","ford","wiley","earhart","windsor"]
		self.acceptable_mealtimes = acceptable_mealtime=["Lunch","Dinner","Breakfast"]

	def enable(self):
		self.enabled = True
	
	def foodHelp(self):
		self.bot.notice(self.bot.user," Usage: !food COURT [MEAL] [YYYY-MM-DD]")
		self.bot.notice(self.bot.user," Example usage: !food hillenbrand")
		self.bot.notice(self.bot.user," Example usage: !food hillenbrand lunch 2013-12-29")
		return

	def run(self):
		self.enabled = False
		#schedule this module to be reenabled after 'self.rate' seconds
		reactor.callLater(self.rate,lambda:self.enable())
		
		params = self.bot.chat.split(' ')

		if len(params) < 2 or 'help' in params or '-h' in params:
			self.foodHelp()
			return

		court = None
		meal = None
		day = None
		for param in params:
			if param.lower() in self.acceptable_courts:
				court = param.lower()
			if param.title() in self.acceptable_mealtimes:
				meal = param.title()
			if re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}',param.lower()):
				day = datetime.strptime(param,'%Y-%m-%d')
		if not court:
			self.foodHelp()
			return
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
			time = datetime.now()
			day = time

		url = "http://api.hfs.purdue.edu/menus/v1/locations/"+court+"/"+day.strftime("%m-%d-%Y")
		json = simplejson.load(urllib.urlopen(url))

		items = [item["Name"] for bar in json[meal] for item in bar["Items"][:3]]
		if not items:
			items = ['Not Serving']
		message = court.title() + ' ' + meal.title() + ': ' + ', '.join(items[:10])
		self.bot.msg(self.bot.channel,message)
