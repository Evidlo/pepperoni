from twisted.internet import reactor, defer
from twisted.web.client import getPage
import simplejson
from datetime import datetime,timedelta
from basemodules import botmodule

#interface for getting the menu from one of purdue's dining courts
class module_food(botmodule):
	def init(self):
		self.acceptable_courts = ["hillenbrand","ford","wiley","earhart","windsor"]
		self.acceptable_mealtimes = ["Lunch","Dinner","Breakfast"]
		self.acceptable_days = {'sunday':6,'monday':0,'tuesday':1,'wednesday':2,'thursday':3,'friday':4,'saturday':5}
		self.relative_days = {'tomorrow':1,'today':0,'yesterday':-1}
		self.jsoncache={}

	def help(self,message):
		self.bot.notice(self.bot.user,message)
		self.bot.notice(self.bot.user," Usage: !food <court> [<meal>] [<YYYY-MM-DD>|<weekday>|tomorrow]")
		self.bot.notice(self.bot.user," Example usage: !food hillenbrand")
		self.bot.notice(self.bot.user," Example usage: !food hillenbrand lunch 2013-12-29")
		self.bot.notice(self.bot.user," Example usage: !food hillenbrand lunch monday")


	#update cache for specified dining court
	def updateCache(self, court, day = datetime.now()):
		self.log.debug("Updating cache: court - {0} : day - {1}".format(court.title(),day.strftime('%Y-%m-%d')))
		return self.getJSONWeb(court,day).addCallback(simplejson.loads).addCallback(self.updateCacheCallback,court,day)

	#once requested json is downloaded, add it to the cache
	def updateCacheCallback(self,json,court,day):
		self.log.debug("Adding data to cache: court - {0} : day - {1}".format(court.title(),day.strftime('%Y-%m-%d')))
		self.jsoncache[court]={'date':day.date(),'json':json}
		return self.jsoncache[court]
	
	#try to find the requested cached data, raise error if not found
	def getJSONCache(self,court,day):
		self.log.debug("Currently in cache: "+self.jsoncache.keys().__repr__())
		if self.jsoncache[court]['date']==day.date():
			self.log.debug("Downloading from cache : {0} - {1}".format(court.title(),day.strftime('%Y-%m-%d')))
			self.log.debug("Success in finding cache")
			return defer.succeed(self.jsoncache[court]['json'])
		else:
			self.log.debug("Not found in cache : court - {0} : day - {1}".format(court.title(),day.strftime('%Y-%m-%d')))
			raise

	#download json data for this dining court from the web
	def getJSONWeb(self,court,day):
			self.log.debug("Downloading from web : court - {0}".format(court.title()))
			url = "http://api.hfs.purdue.edu/menus/v1/locations/"+court+"/"+day.strftime("%m-%d-%Y")
			return getPage(url)

	#retrieves requested data either from cache or download
	def getJSON(self,court,day):
		self.log.debug("Getting JSON")
		#if user requests today's menu, try to get from cache
		if day.date() == datetime.now().date():
			try:
				return self.getJSONCache(court,day)
			#if not found in cache (old cache?), update cache and try via web, then return the deferred
			except:
				self.log.debug("Not found in cache: court - {0} : day - {1}".format(court.title(),day.strftime('%Y-%m-%d')))
				return self.updateCache(court).addCallback(self.getJSONCache)

		#if user requests meal for any other day, download it
		else:
			return self.getJSONWeb(court,day).addCallback(simplejson.loads)

	def run(self):
		params = self.bot.chat.split(' ')

		if len(params) < 2 or 'help' in params or '-h' in params:
			self.help('')
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
				day = datetime.today()
				one_day = timedelta(days = 1)
				#set 'day' object to same weekday as input
				while day.weekday() != self.acceptable_days[param.lower()]:
						day += one_day
			#parse relative days, like 'today', 'tomorrow', 'yesterday'
			if param.lower() in self.relative_days.keys():
				day = datetime.now()
				day += timedelta(days = self.relative_days[param.lower()])

		#logic for dealing with missing input
		if not court:
			self.help('You must specify a dining court.')
			return
		#try to guess what mealtime user is interested in
		if not day:
			day = datetime.now()
			if not meal:
				hour = int(datetime.now().strftime('%H'))
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
				self.help('You must specify a meal when you specify a day.')

		self.getJSON(court,day).addCallback(self.print_results,court,meal)

	def print_results(self,json,court,meal):
			#grab first 3 items from every bar
			items = [item["Name"] for bar in json[meal] for item in bar["Items"][:3]]
			if not items:
				items = ['Not serving or not found']
			message = ':: '+ court.title() + ' ' + meal.title() + ': ' + ', '.join(items[:10])
			self.bot.msg(self.bot.channel,message)
