from twisted.internet import reactor, defer
from twisted.web.client import getPage
from basemodules import botmodule

# bot responds to certain uses of action command
# e.g. `/me slaps pepperoni` makes pepperoni slap the person back
class module_action(botmodule):
    def run(self):
        args = self.bot.chat.split(' ')
        try:
            if len(args) >= 1:
                message = args.split(' ')[0]+' '+self.bot.user
                self.bot.msg(self.bot.channel,'\001ACTION %s\001' % message)
        except IndexError:
            pass
