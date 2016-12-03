#!/usr/bin/python

# Evan Widloski - 2014-05-12 - evan@evanw.org
# An IRC bot written in python-twisted

from twisted.internet import reactor, protocol
from twisted.words.protocols import irc
from ConfigParser import ConfigParser
import traceback
import logging
import re
import os
import sys
from datetime import datetime, timedelta


class Bot(irc.IRCClient):


    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        for channel in self.factory.channels:
            self.join(channel)
        # self.factory.log.info("Signed on as %s." % self.factory.nickname)
        self.factory.log.info("Signed on as %s." % self.nickname)
        self.factory.log.info("Identifying with password")
        self.msg('nickserv','identify %s' % self.factory.password)
        self.setModes()
        self.loadModules()

    def irc_ERR_PASSWDMISMATCH(self):
        self.factory.log.info("Password incorrect, not identified")

    # set user modes for bot
    def setModes(self):
        self.factory.log.debug('Setting modes:{0}'.format(self.factory.modes))
        # self.mode(self,set=True,user=self.factory.nickname,modes=self.factory.modes)
        self.mode(self, set=True, user=self.nickname, modes=self.factory.modes)

    # loads user written modules
    def loadModules(self):
        self.modules = []
        module_dir = 'modules'
        raw_modules = {}
        fail_count = 0

        self.factory.log.debug('Loading modules...')
        self.factory.log.debug('Using blacklist: ' +
                               self.factory.blacklist.__repr__())

        try:
            # reload module settings
            config.read('settings.ini')
        except Exception as e:
            self.factory.log.info("Error reading config")
            self.factory.log.debug(e)
        # load base modules for bot, note that execfile appends to dict
        execfile('basemodules.py', raw_modules)

        if os.path.isdir(module_dir):
            # get all the .py files from module_dir
            for file in os.listdir(module_dir):
                if file.endswith('.py'):
                    # import all data from each .py
                    try:
                        execfile(os.path.join(module_dir, file), raw_modules)
                    except:
                        fail_count+=1
                        self.factory.log.info("Failed to load module: {0}".format(file))
                        traceback.print_exc()
            for name,module in raw_modules.items():
                # only load modules that start with 'module_'
                # and aren't blacklisted for this server
                if (
                    name.startswith('module_') and
                    name not in self.factory.blacklist and config
                    ):
                    self.factory.log.debug('Loading module %s'%name)
                    self.modules.append(module(config, self))

            load_status = (len(raw_modules.items())-fail_count, len(raw_modules.items()))
            message = "Loaded {0}/{1}".format(load_status[0], load_status[1])
            self.factory.log.info(message)
            return load_status

    # handle joining channel
    def joined(self, channel):
        self.factory.log.info("Joined %s." % channel)
        self.factory.log.info("Identifying now")

    # handle being kicked from channel
    def kickedFrom(self, channel, kicker, message):
        self.factory.log.info('Kicked from '+channel+' by '+kicker+' with message: '+message)
        self.factory.log.info('Rejoining...')
        self.join(channel)

    # handle private messages seen in channel
    def privmsg(self, user, channel, chat):
        self.user = user.split('!')[0]
        self.channel = channel
        self.chat = chat

        # check message against triggers for every module
        for module in self.modules:
            if module.enabled:
                for trigger in module.triggers:
                    if re.search(trigger, chat):
                        module.__run__()
                        return

    def action(self, user, channel, chat):
        self.privmsg(user, channel, chat)

    # queue of in-flight pings and what module to call when they arrive
    # ping_queue = [{'user':foo_user,'module':module_foo.pong,'time':datetime_object}]
    ping_queue = []
    def append_ping_queue(self,user,pong_function):
        self.ping_queue.append({'user':user,'function':pong_function,'time':datetime.now()})
        # remove old entries from ping_queue
        self.ping_queue = [ping for ping in self.ping_queue if (datetime.now() - ping['time']) < timedelta(seconds = 30)]

    # call respective module pong functions when a pong is received
    def pong(self, user, secs, text=None):
        self.factory.log.debug('Received pong from {0}: {1}s'.format(user, secs))
        user = user.split('!')[0]
        # delete from ping_queue and call function
        for index,ping in enumerate(self.ping_queue):
            if ping['user'] == user:
               function = ping['function']
               self.factory.log.debug('Found a record for {0} in ping_queue.  Calling function {1}'.format(user, function))
               del self.ping_queue[index]
               function(user=user,latency=secs)
               break


class BotFactory(protocol.ClientFactory):
    protocol = Bot
    config = ConfigParser()
    config.read('settings.ini')

    def __init__(self, channels, nickname, password, blacklist, log, modes):
        self.channels = channels
        self.nickname = nickname
        self.blacklist = blacklist
        self.log = log
        self.password = password
        self.modes = modes

    def clientConnectionLost(self, connector, reason):
        self.log.info("Connection lost. Reason: %s" % reason)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        self.log.info("Connection failed. Reason: %s" % reason)


if __name__ == "__main__":
    config = ConfigParser()
    config.read('settings.ini')

    # start up each instance of the bot,
    # and join each channel/server with given nick
    instances = [
            {
            'host':host,
            'channels':channels,
            'nick':nick,
            'blacklist':blacklist,
            'logfile':logfile,
            'password':password,
            'modes':modes
            }
            for host, channels, nick, blacklist, logfile, password, modes in zip(
                config.get('bot', 'host').split(','),
                config.get('bot', 'channel').split(','),
                config.get('bot', 'nick').split(','),
                config.get('bot', 'blacklist').split(','),
                config.get('bot', 'logfile').split(','),
                config.get('bot', 'password').split(','),
                config.get('bot', 'modes').split(',')
                )
        ]

    # create a bot instance for each server
    for instance in instances:

        # set up logging for this instance
        loglevel = config.get('bot', 'loglevel')
        if loglevel.lower() == 'debug':
            logmode = logging.DEBUG
        else:
            logmode = logging.INFO

        # get port from `host`
        split_host = host.split(':')
        if len(split_host) == 2:
            port = split_host[1]
        else:
            port = 6667

        # set log file
        log = logging.getLogger(instance['logfile'])
        log.setLevel(logmode)
        # support stdout or file logging
        if instance['logfile'] == 'stdout':
            fh = logging.StreamHandler(sys.stdout)
        else:
            fh = logging.FileHandler(instance['logfile'])
        fh.setLevel(logmode)
        fh.setFormatter(logging.Formatter('%(asctime)s :: %(message)s'))
        log.addHandler(fh)
        log.info('Current log level: {0}'.format(log.getEffectiveLevel()))

        # create bot instance
        reactor.connectTCP(instance['host'],
                           port,
                           BotFactory(instance['channels'].split(' '),
                                      instance['nick'],
                                      instance['password'],
                                      instance['blacklist'].split(' '),
                                      log,
                                      instance['modes'],
                                      ))
    reactor.run()
