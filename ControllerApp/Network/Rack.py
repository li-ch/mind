__author__ = 'li'

class Rack(object):
    def __init__(self, rid, serverList, ethList):
        self.id = rid
        self.ToREthList = ethList
        self.serverList = serverList
        self.connection = dict(zip(serverList, ethList))
