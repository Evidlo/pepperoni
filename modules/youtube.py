from twisted.internet import reactor, defer
from twisted.web.client import getPage
import simplejson
import re
from basemodules import botmodule

# get statistics for youtube links - title, rating, views
class module_youtube(botmodule):
    def init(self):
        self.key = self.bot.factory.config.get('module_youtube','key')
    def run(self):
        
        video_id = re.match(".*?v=([a-zA-Z0-9_-]{11}).*",str(self.bot.chat))
        if video_id:
            video_id = video_id.group(1)
            url = 'http://gdata.youtube.com/feeds/api/videos/%s?alt=json&v=2' % id 
            url = 'https://www.googleapis.com/youtube/v3/videos?part=snippet%2Cstatistics&id={0}&key={1}'.format(video_id,self.key)
            self.log.debug('Getting URL: {0}'.format(url))
            getPage(url).addCallback(simplejson.loads).addCallback(self.results)

    def results(self,video):
            #if ratings exist, calculate percent upvote
            self.log.debug('Retrieved Json')
            self.log.debug(video)
            ups = video['items'][0]['statistics']['likeCount']
            downs = video['items'][0]['statistics']['dislikeCount']
            rating=round(float(ups)/(int(ups)+int(downs)),2)*100;
            total_ratings=str(int(ups)+int(downs))
            title = video['items'][0]['snippet']['title']
            views = video['items'][0]['statistics']['viewCount']

            self.log.debug('Got results.')
            self.bot.msg(self.bot.channel,':: {0} - {1} views - {2}% - {3} ratings ::'.format(title,views,rating,total_ratings))

