from twisted.internet import reactor, defer
from twisted.web.client import getPage
from basemodules import botmodule
import json
import datetime
import urllib

#updates the topic with the latest events from the Purdue Linux Users Group Calendar
class module_topic(botmodule):
	def init(self):
		self.key = self.config.get(self.name,'key')

	def run(self):
		self.enabled = False
		#schedule this module to be reenabled after 'self.rate' seconds
		reactor.callLater(self.rate,lambda:self.enable())
		date = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S-0500')
		url = 'https://www.googleapis.com/calendar/v3/calendars/0q5kmi03heskp39fpg73iniapc%40group.calendar.google.com/events?maxResults=2&timeMin='+date+'&fields=items%28end%2Cstart%2Csummary%2Clocation%29&key='+self.key
		self.log.info('Using key:'+self.key)
		try:
			data = json.load(urllib.urlopen(url))
		except:
			self.log.info('Unable to fetch Gcal results')

		message = 'Upcoming Events :: '
		for event in data['items']:
			#read in date, chop off 6 char timezone
			time = datetime.datetime.strptime(event['start']['dateTime'][:-6],'%Y-%m-%dT%H:%M:%S')
			
			message+='%s - %s at %s | '%(event['summary'],time.strftime('%a., %b. %d, %I:%M%p'),event['location'])

		self.log.info('Got calendar results')
		self.log.info(message)
		self.bot.topic(self.bot.channel,message.encode('utf8'))
