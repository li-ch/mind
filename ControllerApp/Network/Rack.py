__author__ = 'li'

NUMPORT = 48

class Rack(object):
    def __init__(self, rid, serverList):
        self.id = rid
        self.ToREthList = range(48)
        self.serverList = serverList
        self.connection = dict(zip(serverList, ethList))
