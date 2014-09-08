from twisted.internet import reactor, defer
from twisted.web.client import getPage
import simplejson
import re
from basemodules import botmodule

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
			getPage(url).addCallback(simplejson.loads).addCallback(self.results)

	def results(self,video):
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

