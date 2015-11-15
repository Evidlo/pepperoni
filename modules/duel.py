from twisted.internet import reactor, defer
from basemodules import botmodule
import random

#duel a user in the chat
class module_duel(botmodule):
    def init(self):
        self.difficulties = {'easy':1,'medium':.5,'hard':.35,'clinteastwood':.1}
        self.reset()

    #reset game
    def reset(self):
        self.opponent = None
        self.fireCallback = None
        self.drawCallback = None
        self.difficulty = ('easy',self.difficulties['easy'])

    def draw(self):
        # self.bot.msg(self.bot.channel,'\001ACTION %s\001' % "DRAW")
        self.bot.msg(self.bot.channel, "DRAW")
        self.fireCallback = reactor.callLater(self.difficulty[1],lambda:self.fire())

    #the bot fires
    def fire(self):
        # self.bot.msg(self.bot.channel,'\001ACTION %s\001' % "*bang*")
        self.bot.msg(self.bot.channel, "*bang*")
        self.bot.msg(self.bot.channel,'Nobody messes with Dirty Dan... (Game Over)')
        self.reset()

    def run(self):
        params = self.bot.chat.split(' ')

        #start the game
        if '!duel' in params and self.opponent == None:
            #set the difficulty if specified
            if len(params) >= 2 and params[1].lower() in self.difficulties:
                self.difficulty = (params[1], self.difficulties[params[1].lower()])

            self.opponent = self.bot.user
            print self.difficulty[0]
            self.bot.msg(self.bot.channel,
                         '{0}: This town aint big enuf fer th\' two of us. (difficulty:{1})'.format(self.bot.user,self.difficulty[0].capitalize()))
            drawtime = random.randint(5,20)
            self.drawCallback = reactor.callLater(drawtime,lambda:self.draw())

        #handle fire from opponent
        elif '!fire' in params and self.bot.user == self.opponent:
            #if the opponent fires after the draw but before we fire
            if self.fireCallback:
                self.bot.msg(self.bot.channel,'I am defeated! (You Win)')
                self.opponent = None
                self.fireCallback.cancel()
                self.reset()
            #if the opponent fires before the draw
            else:
                self.bot.msg(self.bot.channel,'You dishonor family (Game Over)')
                self.opponent = None
                self.drawCallback.cancel()
                self.reset()






