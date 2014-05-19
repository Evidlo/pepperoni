#!/usr/bin/env python2

"""
	todo:
		create an ini with settings - tag for module,triggers
		associate triggers to objects using list
		profit
"""

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
		self.join(self.factory.channel)
		logging.info("Signed on as %s." % self.nickname)
		#set up all the modules (ignore builtins)
		myclasses = {}
		execfile('modules.py',myclasses)
		for a,b in myclasses.items():
			print a+":"+str(type(b))
		sys.exit(0)
		self.mymodules = {name:myclass(config) for name,myclass in myclasses.items() if type(myclass) == type}

	def joined(self, channel):
		logging.info("Joined %s." % channel)

	def privmsg(self, user, channel, msg):

		logging.debug("Private Message:",msg)

		#check message against triggers for every module
		for module in self.mymodules.values():
			if module.enabled:
				print 'module enabled'
				for trigger in module.triggers:
					if re.search(trigger,msg):
						self.msg(channel,module.run(user,msg))
						return

class BotFactory(protocol.ClientFactory):
	protocol = Bot

	def __init__(self, channel, nickname):
		self.channel = channel
		self.nickname = nickname

	def clientConnectionLost(self, connector, reason):
		logging.info("Connection lost. Reason: %s" % reason)
		connector.connect()

	def clientConnectionFailed(self, connector, reason):
		logging.info("Connection failed. Reason: %s" % reason)

if __name__ == "__main__":
		config = ConfigParser()
		config.read('settings.ini')		
		chan = config.get('bot','channel',0)
		host = config.get('bot','host',0)
		nick = config.get('bot','nick',0)
		reactor.connectTCP(host, 6667, BotFactory(chan,nick))
		reactor.run()
