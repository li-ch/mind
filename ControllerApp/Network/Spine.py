__author__ = 'li'

class Spine(object):

    def __init__(self, ethList, ToRList):
        self.SpineEthList = ethList
        self.ToRList = ToRList
        self.connection = dict(zip(ethList,ToRList))
