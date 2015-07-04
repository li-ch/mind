__author__ = 'li'

from random import choice, randint
from time import sleep

def main():
    ipbase = '192.168.100.'
    ippoolsize = 30
    iplast = range(1, ippoolsize+1)
    ippool = []
    for ipl in iplast:
        ippool.append(ipbase+str(ipl))

    flowCounter = choice(range(2000, 3000))
    portpool = range(8000,10000)

    while True:
        k = randint(1, 6)
        for i in range(k):
            print 'flow {} captured'.format(flowCounter)
            print 'srcIP = {}, dstIP = {}, srcPort = {}, dstPort = {}'.format(
                choice(ippool), choice(ippool), choice(portpool), choice(portpool)
            )
            sleep(0.1)
            print '========MindCtrl-Outputs========'
            print 'size = {}KB, coflow_id = {}, path = {}'.format(
                choice(range(10, 387)), -1, choice([0, 1]))
            print ''

        print '========Path-Status============='
        pkts = choice(range(67, 2382))
        print 'path 0 load: {} flows, {} packets, {} bytes'.format(
            randint(1, k), pkts, 1480*pkts
        )
        pkts = choice(range(67, 2382))
        print 'path 1 load: {} flows, {} packets, {} bytes'.format(
            randint(1, k), pkts, 1480*pkts
        )

        flowCounter += k
        sleep(3)

if __name__ == "__main__":
    main()