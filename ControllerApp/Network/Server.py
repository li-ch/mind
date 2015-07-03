__author__ = 'li'

class Server(object):
    def __init__(self,
                 rack,
                 ip='10.0.0.1',
                 ports=range(8000,8010),
                 eth='00:00:00:00:00:01'):
        self.ip = ip
        self.ports = ports
        self.eth = eth
        self.rack = rack
