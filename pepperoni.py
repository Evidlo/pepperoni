#!/usr/bin/env python2

#Evan Widloski - 2014-05-12 - evan@evanw.org
#An IRC bot written in python-twisted

import sys
from twisted.internet import reactor, protocol
from twisted.words.protocols import irc
from random import choice
from ConfigParser import ConfigParser
import logging
import re
import modules


class Bot(irc.IRCClient):


	def _get_nickname(self):
		return self.factory.nickname
	nickname = property(_get_nickname)

	def signedOn(self):
		for channel in self.factory.channels:
			self.join(channel)
		logging.info("Signed on as %s." % self.nickname)
		self.loadModules()

	def loadModules(self):
		#reload module settings
		config.read('settings.ini')		
		#set up all the modules (ignore builtins)
		myclasses = {}
		execfile('modules.py',myclasses)
		self.mymodules = {name:myclass(config,self) for name,myclass in myclasses.items() if name.startswith('module_')}

	def joined(self, channel):
		logging.info("Joined %s." % channel)
	
	def kickedFrom(self, channel, kicker, message):
		logging.info('Kicked from '+channel+' by '+kicker+' with message: '+message)
		logging.info('Rejoining...')
		self.join(channel)

	def privmsg(self, user, channel, chat):
		self.user = user.split('!')[0]
		self.channel = channel
		self.chat = chat

		logging.debug("Private Message:"+chat)

		#check message against triggers for every module
		for module in self.mymodules.values():
			if module.enabled:
				for trigger in module.triggers:
					if re.search(trigger,chat):
						module.run()
						return
	
	def action(self, user, channel, chat):
		self.privmsg(user,channel,chat)

class BotFactory(protocol.ClientFactory):
	protocol = Bot

	def __init__(self, channels, nickname):
		self.channels = channels
		self.nickname = nickname

	def clientConnectionLost(self, connector, reason):
		logging.info("Connection lost. Reason: %s" % reason)
		connector.connect()

	def clientConnectionFailed(self, connector, reason):
		logging.info("Connection failed. Reason: %s" % reason)

if __name__ == "__main__":
		config = ConfigParser()
		config.read('settings.ini')		
		logging.basicConfig(filename='/tmp/peetsa.log',level=logging.DEBUG)
		
		#start up each instance of the bot, and join each channel/server with given nick
		instances = zip(config.get('bot','host').split(','),config.get('bot','channel').split(','),config.get('bot','nick').split(','))
		for instance in instances:
			print instance
			reactor.connectTCP(instance[0], 6667, BotFactory(instance[1].split(' '),instance[2]))
		reactor.run()
