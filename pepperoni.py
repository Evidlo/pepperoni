#!/usr/bin/python

#Evan Widloski - 2014-05-12 - evan@evanw.org
#An IRC bot written in python-twisted

from twisted.internet import reactor, protocol
from twisted.words.protocols import irc
from ConfigParser import ConfigParser
import traceback
import logging
import re
import os



class Bot(irc.IRCClient):

    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        for channel in self.factory.channels:
            self.join(channel)
        self.factory.log.info("Signed on as %s." % self.nickname)
        self.factory.log.info("Identifying with password")
        self.msg('nickserv','identify %s' % self.factory.password)
        self.loadModules()

    def irc_ERR_PASSWDMISMATCH(self):
        self.factory.log.info("Password incorrect, not identified")

    #loads user written modules
    def loadModules(self):
        self.modules = [] 
        module_dir = 'modules'
        raw_modules = {}
        fail_count = 0

        self.factory.log.debug('Loading modules...')
        self.factory.log.debug('Using blacklist: '+self.factory.blacklist.__repr__())

        try:
            #reload module settings
            config.read('settings.ini')
        except Exception as e:
            self.factory.log.info("Error reading config")
            self.factory.log.debug(e)
        #load base modules for bot, note that execfile appends to dict
        execfile('basemodules.py',raw_modules)

        if os.path.isdir(module_dir):
            #get all the .py files from module_dir
            for file in os.listdir(module_dir):
                if file.endswith('.py'):
                    #import all data from each .py
                    try:
                        execfile(os.path.join(module_dir,file),raw_modules)
                    except:
                        fail_count+=1
                        self.factory.log.info("Failed to load module: {0}".format(file))
                        traceback.print_exc()
            for name,module in raw_modules.items():

                    #only load modules that start with 'module_' and aren't blacklisted for this server    
                if name.startswith('module_') and name not in self.factory.blacklist and config:
                    self.factory.log.debug('Loading module %s'%name)
                    self.modules.append(module(config,self))

            message = "Loaded {0}/{1}".format(len(raw_modules.items())-fail_count,len(raw_modules.items()))
            self.factory.log.info(message)

    def joined(self, channel):
        self.factory.log.info("Joined %s." % channel)
        self.factory.log.info("Identifying now")
    
    def kickedFrom(self, channel, kicker, message):
        self.factory.log.info('Kicked from '+channel+' by '+kicker+' with message: '+message)
        self.factory.log.info('Rejoining...')
        self.join(channel)

    def privmsg(self, user, channel, chat):
        self.user = user.split('!')[0]
        self.channel = channel
        self.chat = chat

        #check message against triggers for every module
        for module in self.modules:
            if module.enabled:
                for trigger in module.triggers:
                    if re.search(trigger,chat):
                        module.__run__()
                        return
    
    def action(self, user, channel, chat):
        self.privmsg(user,channel,chat)

class BotFactory(protocol.ClientFactory):
    protocol = Bot
    config = ConfigParser()
    config.read('settings.ini')        

    def __init__(self, channels, nickname,password, blacklist,log):
        self.channels = channels
        self.nickname = nickname
        self.blacklist = blacklist
        self.log = log
        self.password = password

    def clientConnectionLost(self, connector, reason):
        self.log.info("Connection lost. Reason: %s" % reason)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        self.log.info("Connection failed. Reason: %s" % reason)



if __name__ == "__main__":
    config = ConfigParser()
    config.read('settings.ini')        
    
    #start up each instance of the bot, and join each channel/server with given nick
    instances = [
        {
        'host':host,
        'channels':channels,
        'nick':nick,
        'blacklist':blacklist,
        'logfile':logfile,
        'password':password
        } 
        for host,channels,nick,blacklist,logfile,password in zip(
            config.get('bot','host').split(','),
            config.get('bot','channel').split(','),
            config.get('bot','nick').split(','),
            config.get('bot','blacklist').split(','),
            config.get('bot','logfile').split(','),
            config.get('bot','password').split(',')
            )
    ]
    for instance in instances:

        #set up logging for this instance
        loglevel = config.get('bot','loglevel')
        if loglevel.lower() == 'debug':
            logmode = logging.DEBUG
        else:
            logmode = logging.INFO
            
        log = logging.getLogger(instance['logfile'])
        log.setLevel(logmode)
        fh = logging.FileHandler(instance['logfile'])
        fh.setLevel(logmode)
        fh.setFormatter(logging.Formatter('%(asctime)s :: %(message)s'))
        log.addHandler(fh)
        log.info('Current log level: {0}'.format(log.getEffectiveLevel()))

        reactor.connectTCP(instance['host'], 6667, BotFactory(instance['channels'].split(' '),instance['nick'],instance['password'],instance['blacklist'].split(' '),log))
    reactor.run()
