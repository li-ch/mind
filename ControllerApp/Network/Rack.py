__author__ = 'li'

class Rack(object):
    def __init__(self, serverList, ethList):
        self.ToREthList = ethList
        self.serverList = serverList
        self.connection = dict(zip(serverList, ethList))
