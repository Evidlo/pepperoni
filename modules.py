# -*- coding: utf-8 -*-
#Evan Widloski - 2014-05-20 - evan@evanw.org
#Modules for pepperoni bot - 

from twisted.internet import reactor
from random import choice
#module_youtube
import simplejson
import urllib
import re
#module_food
from datetime import datetime,timedelta


#Module class which all modules inherit from
class botmodule(object):
	def __init__(self,config,bot):
		self.enabled = True
		#module name is everything after first underscore
		self.name = ''.join(self.__class__.__name__.split('_')[1:])
		self.rate = int(config.get(self.name,'rate',0))
		self.bot = bot
		triggers = config.get(self.name,'triggers')
		self.triggers = triggers.split('\n')
		#call user defined init function, if it exists
		if hasattr(self,'init'):
			self.init()


	def enable(self):
		self.enabled = True

#reloads this file on !reload command
class module_reload(botmodule):
	def run(self):
		self.enabled = False
		#schedule this module to be reenabled after 'self.rate' seconds
		reactor.callLater(self.rate,lambda:self.enable())
		#only enable for user Evidlo
		if self.bot.user == 'Evidlo':
				self.bot.loadModules()
				self.bot.msg(self.bot.channel,':: Reloaded all modules ::')
		return
	
#spouts a quote by a women as a quip to 'thats what she said'
class module_shesaid(botmodule):
	def init(self):
		quotesFile = 'quotes.txt'
		with open(quotesFile) as quotesFileObj:
			self.quotes = quotesFileObj.readlines()

	def run(self):
		self.enabled = False
		#schedule this module to be reenabled after 'self.rate' seconds
		reactor.callLater(self.rate,lambda:self.enable())
		self.bot.msg(self.bot.channel,choice(self.quotes))

#convert text to 1337
class module_leet(botmodule):
	def init(self):
		self.leet = {'a':'4','b':'8','c':'(','d':')','e':'3','g':'6','h':'#','i':'1','l':'|','o':'0','s':'5','t':'7','w':'vv','4':'a','8':'b','(':'c',')':'d','3':'e','6':'g','#':'h','1':'i','|':'l','0':'o','5':'s','7':'t','vv':'w'}

	def run(self):
		self.enabled = False
		#schedule this module to be reenabled after 'self.rate' seconds
		reactor.callLater(self.rate,lambda:self.enable())
		chat = ' '.join(self.bot.chat.split(' ')[1:])
		chat = chat.lower()
		message = '' 
		for letter in chat:
			try:
				message += self.leet[letter]
			except:
				message += letter
		if message:
			self.bot.msg(self.bot.channel,message)

#xzibit dat stuff
class module_yodawg(botmodule):
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
class module_youtube(botmodule):
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
			self.bot.msg(self.bot.channel,':: ' + title + " - " + views +" views"+" - "+"Rating " + str(rating)+"% - "+ratings+" ratings ::")


#interface for getting the menu from one of purdue's dining courts
class module_food(botmodule):
	def init(self):
		self.acceptable_courts = ["hillenbrand","ford","wiley","earhart","windsor"]
		self.acceptable_mealtimes = ["Lunch","Dinner","Breakfast"]
		self.acceptable_days = {'sunday':6,'monday':0,'tuesday':1,'wednesday':2,'thursday':3,'friday':4,'saturday':5}
		self.relative_days = {'tomorrow':1,'today':0,'yesterday':-1}

	def foodHelp(self,message):
		self.bot.notice(self.bot.user,message)
		self.bot.notice(self.bot.user," Usage: !food <court> [<meal>] [<YYYY-MM-DD>|<weekday>|tomorrow]")
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
				#set 'day' object to same weekday as input
				while day.weekday() != self.acceptable_days[param.lower()]:
						day += one_day
			if param.lower() in self.relative_days.keys():
				day = datetime.now()
				day += timedelta(days = 1)*self.relative_days[param.lower()]

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
		message = ':: '+ court.title() + ' ' + meal.title() + ': ' + ', '.join(items[:10])
		self.bot.msg(self.bot.channel,message)


#responds to actions
class module_action(botmodule):
	def run(self):
		self.enabled = False
		#schedule this module to be reenabled after 'self.rate' seconds
		reactor.callLater(self.rate,lambda:self.enable())
		try:
			message = self.bot.chat.split(' ')[0]+' '+self.bot.user
			self.bot.msg(self.bot.channel,'\001ACTION %s\001' % message)
		except IndexError:
			pass

#dmesg
class module_dmesg(botmodule):
	def run(self):
		self.enabled = False
		reactor.callLater(self.rate,lambda:self.enable())
		self.bot.msg(self.bot.channel,'wat')


#converts text to zalgo using table in zalgo_dict.py
class module_zalgo(botmodule):
	def init(self):
		zalgo_dict={}
		execfile('zalgo_dict.py',zalgo_dict,zalgo_dict)
		self.zalgo_dict = zalgo_dict

	def run(self):
		self.enabled = False
		#schedule this module to be reenabled after 'self.rate' seconds
		message = ' '.join(self.bot.chat.split(' ')[1:])
		reactor.callLater(self.rate,lambda:self.enable())
		out = [letter + choice(self.zalgo_dict['zalgo_up']) * 2 + choice(self.zalgo_dict['zalgo_down']) * 2 + choice(self.zalgo_dict['zalgo_mid']) * 2 for letter in message]
		out = out[:27]
		self.bot.msg(self.bot.channel,''.join(out).encode('utf8'))

#urban dictionary definition grabber
class module_poodict(botmodule):
	def run(self):
		word='%20'.join(self.bot.chat.split(' ')[1:])
		url = "http://api.urbandictionary.com/v0/define?term="+word
		json = simplejson.load(urllib.urlopen(url))
		definition = json['list'][0]['definition']
		message = ':: ' + definition[0:200]
		self.bot.msg(self.bot.channel,message)

#get regular definitions from glosbe dictionary
class module_dict(botmodule):
	def run(self):
		definition = ''
		word=self.bot.chat.split(' ')[1]
		url='http://glosbe.com/gapi/translate?from=eng&dest=eng&format=json&phrase=' + word
		json = simplejson.load(urllib.urlopen(url))
		definition = json['tuc'][0]['meanings'][0]['text']
		if definition:
			self.bot.msg(self.bot.channel,':: ' + definition[0:200])

