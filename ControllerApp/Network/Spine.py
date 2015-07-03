__author__ = 'li'

class Spine(object):
    def __init__(self, sid, ethList, ToRList):
        self.id = sid
        self.SpineEthList = ethList
        self.ToRList = ToRList
        self.connection = dict(zip(ethList,ToRList))
