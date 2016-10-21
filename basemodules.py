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
        self.config = config
        self.log = self.bot.factory.log
        triggers = config.get(self.name,'triggers')
        self.triggers = triggers.split('\n')
        #call user defined init function, if it exists
        if hasattr(self,'init'):
            self.init()

    def enable(self):
        self.enabled = True

    def __run__(self):
        #log a module getting called and its arguments
        self.log.info('Module {0} called by user {1}'.format(self.name,self.bot.user))
        params = self.bot.chat.split(' ')
        self.log.info('Arguments: {0}'.format(params))
        #disable the module and schedule a reenable after timeout period 'rate'
        self.enabled = False
        reactor.callLater(self.rate,lambda:self.enable())
        #call user defined run function, if it exists
        if hasattr(self,'run'):
            self.run()
        else:
            self.log.info('No "run" function found for this module. Ignoring')

#reloads this file on !reload command
class module_reload(botmodule):
    def init(self):
        self.owner = self.bot.factory.config.get('bot','owner')
    def run(self):
        params = self.bot.chat.split(' ')
        #only enable for owner
        if self.bot.user == self.owner:
            if 'pull' in params:
                self.log.info('Pulling from github')
                g = git.cmd.Git()
                g.pull()

            reload_success = self.bot.loadModules()
            self.bot.msg(self.bot.channel,':: Reloaded {0}/{1} modules'.format(reload_success[0],reload_success[1]))
        return

#lists currently loaded modules
class module_loaded(botmodule):
    def run(self):
        if self.bot.user == 'Evidlo':
                loaded_modules = ', '.join([module.name for module in self.bot.modules])
                self.bot.msg(self.bot.channel,':: Loaded modules: ' + loaded_modules)
        return
