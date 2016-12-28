from twisted.internet import reactor, defer
from basemodules import botmodule
import random


#duel a user in the chat
class module_duel(botmodule):
    # load ping timeout and difficulty times from config
    def init(self):
        self.timeout = float(self.config.get(self.name,'timeout'))

        # easy = float(self.config.get(self.name,'easy'))
        easy = 1
        medium = float(self.config.get(self.name,'medium'))
        hard = float(self.config.get(self.name,'hard'))
        clint = float(self.config.get(self.name,'clinteastwood'))
        self.difficulties = {'easy':easy,'medium':medium,'hard':hard,'clinteastwood':clint}
        self.opponent = None
        self.difficulty = ('easy',self.difficulties['easy'])

    # handle pong
    def pong(self,user=None,latency=None):
        self.pingtimeoutCallback.cancel()
        self.latency = latency
        self.log.debug('Pong called with user={0}, time={1}'.format(user,self.latency))
        self.bot.msg(self.bot.channel, "PONG")
        self.fireCallback = reactor.callLater(self.difficulty[1],lambda:self.fire(self.latency))

    # if the ping is never answered, reset the game
    def ping_timeout(self):
        self.bot.msg(self.bot.channel,'\001ACTION walks away, coolly.\001')
        self.reset()

    #reset game
    def reset(self):
        self.opponent = None
        # self.fireCallback = None
        # self.drawCallback = None
        for callback in (self.fireCallback, self.drawCallback, self.pingtimeoutCallback):
            if not callback.cancelled and not callback.called:
                callback.cancel()
        self.difficulty = ('easy',self.difficulties['easy'])

    def draw(self):
        # self.bot.msg(self.bot.channel,'\001ACTION %s\001' % "DRAW")
        self.bot.msg(self.bot.channel, "DRAW")
        self.log.debug('draw')
        self.bot.ping('Evidlo')
        self.pingtimeoutCallback = reactor.callLater(self.timeout,lambda:self.ping_timeout())

    #the bot fires
    def fire(self, latency):
        # self.bot.msg(self.bot.channel,'\001ACTION %s\001' % "*bang*")
        self.bot.msg(self.bot.channel, "*bang*")
        self.log.debug('fire')
        self.bot.msg(self.bot.channel,'Nobody messes with Dirty Dan... (Game Over)')
        self.reset()

    def run(self):
        params = self.bot.chat.split(' ')
        #start the game
        if '!duel' in params and self.opponent == None:
            #set the difficulty if specified
            if len(params) >= 2 and params[1].lower() in self.difficulties:
                self.difficulty = (params[1], self.difficulties[params[1].lower()])
            self.bot.append_ping_queue('Evidlo', self.pong)
            self.bot.msg(self.bot.channel,'\001ACTION sizes up {0}. \001'.format(self.bot.user))
            self.opponent = self.bot.user
            self.bot.msg(self.bot.channel,
                        '{0}: This town ain\'t big enuf fer th\' two of us. (difficulty:{1})'.format(self.bot.user, self.difficulty[0].capitalize()))
            # drawtime = random.randint(5,20)
            drawtime = 3
            self.drawCallback = reactor.callLater(drawtime,lambda:self.draw())

        #handle fire from opponent
        elif '!fire' in params and self.bot.user == self.opponent:
            #if the opponent fires after the draw but before we fire
            if self.drawCallback.called and not self.fireCallback.called:
                self.bot.msg(self.bot.channel,'I am defeated! (You Win. latency:{0})'.format(self.latency))
                self.reset()
            #if the opponent fires before the draw
            else:
                self.bot.msg(self.bot.channel,'You dishonor family (Game Over)')
                self.reset()
