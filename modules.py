from random import choice

class shesaid(object):
  def __init__(self,quotesFile,triggers):
    self.triggers = triggers.split('\n')
    with open(quotesFile) as quotesFileObj:
      self.quotes = quotesFileObj.readlines()

  def run(self,user,msg):
    return choice(self.quotes)

