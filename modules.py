# -*- coding: utf-8 -*-
#Evan Widloski - 2014-05-20 - evan@evanw.org
#Modules for pepperoni bot - Modules must begin with module_

from twisted.internet import reactor
from random import choice
#module_youtube
import simplejson
import urllib
import re
#module_food
from datetime import datetime,timedelta
#module zalgo
from zalgo_dict import *

#reloads this file on !reload command
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
		#only enable for user Evidlo
		if self.bot.user == 'Evidlo':
				self.bot.loadModules()
				self.bot.msg(self.bot.channel,u'▷ '.encode('utf-8')+'Reloaded all modules'+u' ◁'.encode('utf-8'))
		return
	
#spouts a quote by a women as a quip to 'thats what she said'
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

#convert text to 1337
class module_leet(object):
	def __init__(self,config,bot):
		self.enabled = True
		self.rate = int(config.get('leet','rate',0))
		self.bot = bot
		triggers = config.get('leet','triggers')
		self.triggers = triggers.split('\n')
		self.leet = {'a':'4','b':'8','c':'(','d':')','e':'3','g':'6','h':'#','i':'1','l':'|','o':'0','s':'5','t':'7','w':'vv','4':'a','8':'b','(':'c',')':'d','3':'e','6':'g','#':'h','1':'i','|':'l','0':'o','5':'s','7':'t','vv':'w'}

	def enable(self):
		self.enabled = True

	def run(self):
		self.enabled = False
		#schedule this module to be reenabled after 'self.rate' seconds
		reactor.callLater(self.rate,lambda:self.enable())
		chat = ' '.join(self.bot.chat.split(' ')[1:])
		chat = chat.lower()
		message = '' 
		for letter in chat:
			print letter
			try:
				message += self.leet[letter]
			except:
				print 'nf'
				message += letter
		print message
		if message:
			self.bot.msg(self.bot.channel,message)

#xzibit dat stuff
class module_yodawg(object):
	def __init__(self,config,bot):
		self.enabled = True
		self.rate = int(config.get('yodawg','rate',0))
		self.bot = bot
		triggers = config.get('yodawg','triggers')
		self.triggers = triggers.split('\n')

	def enable(self):
		self.enabled = True

	def run(self):
		self.enabled = False
		#schedule this module to be reenabled after 'self.rate' seconds
		reactor.callLater(self.rate,lambda:self.enable())
		words = self.bot.chat.split(' ')
		a = b = None
		if len(words) == 2:
			a = words[1]
			b = a
		if len(words) >= 3:
			a = words[1]
			b = words[2]
		if a and b:
			self.bot.msg(self.bot.channel,'Yo dawg, I heard you like '+a+', so we put '+a+' in your '+b+' so you can '+a+' while you '+b)

#gets statistics for youtube links - title, rating, views
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

			#if ratings exist, calculate percent upvote
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
			self.bot.msg(self.bot.channel,u'▷ '.encode('utf-8') + u'\x02'.encode('utf-8') + title + u'\x0F'.encode('utf-8') + " - " + views +" views"+" - "+"Rating " + str(rating)+"% - "+ratings+" ratings"+u' ◁'.encode('utf-8'))


#interface for getting the menu from one of purdue's dining courts
class module_food(object):
	def __init__(self,config,bot):
		self.enabled = True
		self.rate = int(config.get('food','rate',0))
		self.bot = bot
		triggers = config.get('food','triggers')
		self.triggers = triggers.split('\n')
		self.acceptable_courts = ["hillenbrand","ford","wiley","earhart","windsor"]
		self.acceptable_mealtimes = ["Lunch","Dinner","Breakfast"]
		self.acceptable_days = {'sunday':6,'monday':0,'tuesday':1,'wednesday':2,'thursday':3,'friday':4,'saturday':5}

	def enable(self):
		self.enabled = True
	
	def foodHelp(self,message):
		self.bot.notice(self.bot.user,message)
		self.bot.notice(self.bot.user," Usage: !food COURT [MEAL] [YYYY-MM-DD | weekday]")
		self.bot.notice(self.bot.user," Example usage: !food hillenbrand")
		self.bot.notice(self.bot.user," Example usage: !food hillenbrand lunch 2013-12-29")
		self.bot.notice(self.bot.user," Example usage: !food hillenbrand lunch monday")
		return

	def run(self):
		self.enabled = False
		#schedule this module to be reenabled after 'self.rate' seconds
		reactor.callLater(self.rate,lambda:self.enable())
		
		params = self.bot.chat.split(' ')

		if len(params) < 2 or 'help' in params or '-h' in params:
			self.foodHelp('')
			return

		court = None
		meal = None
		day = None

		#grab the interesting bits of the arguments
		for param in params:
			if param.lower() in self.acceptable_courts:
				court = param.lower()
			if param.title() in self.acceptable_mealtimes:
				meal = param.title()
			if re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}',param.lower()):
				day = datetime.strptime(param,'%Y-%m-%d')
			#handles optional weekday input
			if param.lower() in self.acceptable_days.keys():
				day = datetime.now()
				one_day = timedelta(days = 1)
				while day.weekday() != self.acceptable_days[param.lower()]:
						day += one_day

		#logic for dealing with missing input
		if not court:
			self.foodHelp('You must specify a dining court.')
			return
		#try to guess what mealtime user is interested in
		if not day:
			time = datetime.now()
			day = time
			if not meal:
				time = datetime.now()
				hour = int(time.strftime('%H'))
				print hour
				if hour > 19:
					meal = 'Breakfast'
				elif hour > 14:
					meal = 'Dinner'
				elif hour > 10:
					meal = 'Lunch'
				else:
					meal = 'Breakfast' 
		else:
			if not meal:
				self.foodHelp('You must specify a meal when you specify a day.')

		url = "http://api.hfs.purdue.edu/menus/v1/locations/"+court+"/"+day.strftime("%m-%d-%Y")
		json = simplejson.load(urllib.urlopen(url))

		#grab first 3 items from every bar
		items = [item["Name"] for bar in json[meal] for item in bar["Items"][:3]]
		if not items:
			items = ['Not Serving']
		message = u'\x02'.encode('utf-8') + court.title() + ' ' + meal.title() + ': ' + u'\x0F'.encode('utf-8') + ', '.join(items[:10])
		self.bot.msg(self.bot.channel,message)


#responds to actions
class module_action(object):
	def __init__(self,config,bot):
		self.enabled = True
		self.rate = int(config.get('action','rate',0))
		self.bot = bot
		triggers = config.get('action','triggers')
		self.triggers = triggers.split('\n')

	def enable(self):
		self.enabled = True

	def run(self):
		self.enabled = False
		#schedule this module to be reenabled after 'self.rate' seconds
		reactor.callLater(self.rate,lambda:self.enable())
		try:
			message = self.bot.chat.split(' ')[0]+' '+self.bot.user
			self.bot.msg(self.bot.channel,'\001ACTION %s\001' % message)
		except IndexError:
			pass

#converts text to zalgo using table in zalgo_dict.py
class module_zalgo(object):
	def __init__(self,config,bot):
		self.enabled = True
		self.rate = int(config.get('zalgo','rate',0))
		self.bot = bot
		triggers = config.get('zalgo','triggers')
		self.triggers = triggers.split('\n')

	def enable(self):
		self.enabled = True

	def run(self):
		self.enabled = False
		#schedule this module to be reenabled after 'self.rate' seconds
		message = ' '.join(self.bot.chat.split(' ')[1:])
		reactor.callLater(self.rate,lambda:self.enable())
		out = [letter + choice(zalgo_up) * 2 + choice(zalgo_down) * 2 + choice(zalgo_mid) * 2 for letter in message]
		out = out[:27]
		self.bot.msg(self.bot.channel,''.join(out).encode('utf8'))
