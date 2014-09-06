from twisted.internet import reactor, defer
from twisted.web.client import getPage
import logging
import os
#module_reload
import git

#Module class which all modules inherit from
class botmodule(object):
	def __init__(self,config,bot):
		self.enabled = True
		#grab name of this module
		self.name = ''.join(self.__class__.__name__)
		self.rate = int(config.get(self.name,'rate',0))
		self.bot = bot
		self.log = self.bot.factory.log
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
		params = self.bot.chat.split(' ')
		#schedule this module to be reenabled after 'self.rate' seconds
		reactor.callLater(self.rate,lambda:self.enable())
		#only enable for user Evidlo
		if self.bot.user == 'Evidlo':
			if 'pull' in params:
				self.log.info('Pulling from github')
				g = git.cmd.Git()
				g.pull()
				self.bot.loadModules()
				self.bot.msg(self.bot.channel,':: Pulled and reloaded all modules ::')
			else:
				self.bot.loadModules()
				self.bot.msg(self.bot.channel,':: Reloaded all modules ::')
		return

#lists currently loaded modules
class module_loaded(botmodule):
	def run(self):
		self.enabled=False
		#schedule this module to be reenabled after 'self.rate' seconds
		reactor.callLater(self.rate,lambda:self.enable())
		if self.bot.user == 'Evidlo':
				loaded_modules = ', '.join([module.name for module in self.bot.modules])
				self.bot.msg(self.bot.channel,':: Loaded modules: ' + loaded_modules)
		return
