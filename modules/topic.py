#Evan Widloski - 2014-09-11
from twisted.internet import reactor, defer
from twisted.web.client import getPage
from basemodules import botmodule
import json
from datetime import datetime
import urllib

#updates the topic with the latest events from the Purdue Linux Users Group Calendar
class module_topic(botmodule):
    def init(self):
        self.key = self.bot.config.get(self.name,'key')

    def run(self):
        #Current datetime for calculating which events have not occured
        date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S-0500')
        #Google Calendar Api URL
        url = 'https://www.googleapis.com/calendar/v3/calendars/0q5kmi03heskp39fpg73iniapc%40group.calendar.google.com/events?orderBy=startTime&singleEvents=true&maxResults=50&timeMin='+date+'&fields=items%28start%2Csummary%2Clocation%29&key='+self.key
        self.log.info('Using key:'+self.key)

        #grab data from api
        try:
            data = json.load(urllib.urlopen(url))
            self.log.debug(data)
        except:
            self.log.info('Unable to fetch Gcal results')

        events_text = []
        for event in data['items']:
            event_text=''
            if 'office hours' not in event['summary'].lower():
                #read in date, chop off 6 char timezone
                #apply custom formatting to data
                if 'summary' in event:
                    event_text+=event['summary']
                if 'location' in event:
                    event_text += ' ' + event['location']
                if 'start' in event:
                    if 'dateTime' in event['start']:
                        time = datetime.strptime(event['start']['dateTime'][:-6],'%Y-%m-%dT%H:%M:%S')
                        event_text += ' - ' + time.strftime('%a., %b. %d, %I:%M%p')
                    else:
                        time = datetime.strptime(event['start']['date'],'%Y-%m-%d')
                        event_text += ' - ' + time.strftime('%a., %b. %d')

                events_text.append(event_text)

        message = 'Upcoming Events :: ' + ' | '.join(events_text[:2])
        self.log.info('Got calendar results')
        self.log.info(message)
        self.bot.topic(self.bot.channel,message.encode('utf8'))
