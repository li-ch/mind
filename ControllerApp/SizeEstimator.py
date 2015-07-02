__author__ = 'li'

from flowsizepred import GPRFlowEstimator
import datetime


class SizeEstimator(object):
    def __init__(self):
        self.model = GPRFlowEstimator.GPRModel()
        self.model.load('GPR_model.txt')

    def estimate(self, flowdb):
        for f in flowdb:
            size = self.flowSizeEstimator(f)
            flowdb.setFlowSize(f['id'], size)
        return flowdb

    def flowSizeEstimator(self, flow):
        # this method does not modify flowdb
        size = self.gflowestm_predict(flow)
        # interface with size estimation
        return size

    def gflowestm_train(self, trainingset='univ_1_1.csv', modelpath='model.txt'):
        samples = trainingset  # input sample file
        target_name = 'Payload_Bytes'
        feature_name = 'Server_IP_1:Server_IP_2:Server_IP_3:Server_IP_4:Client_IP_1:Client_IP_2:Client_IP_3:Client_IP_4:Server_Port:Client_Port'
        # Server_IP_1 ~ Server_IP_4 are the four bytes from an IP address
        feature_type = 'IP:IP:IP:IP:IP:IP:IP:IP:Port:Port'
        feature_weight = '0.2:0.1:0.1:0.1:0.1:0.1'
        # the current algorithm doesn't use this parameter, simply input a string like that
        start = 0
        length = 400
        # train a model
        gpr = GPRFlowEstimator.GPRFlowEstimator()
        model = gpr.train(samples, target_name, feature_name, feature_type, feature_weight,
                          start, length, model_path=modelpath)
        return model

    def gflowestm_predict(self, flow):
        srcIP = flow['srcIP'].replace('.', ':')
        dstIP = flow['dstIP'].replace('.', ':')
        srcPort = flow['srcPort'].replace('.', ':')
        dstPort = flow['dstPort'].replace('.', ':')
        flowsample = srcIP + ':' + dstIP + ':' + srcPort + ':' + dstPort
        fs = self.model.predictSingle_2(flowsample, 0)
        return fs

    def gflowestm_update(self, flow):
        # do this whenever a flow finishes routing and the flow info. is collected.
        srcIP = flow['srcIP'].replace('.', ':')
        dstIP = flow['dstIP'].replace('.', ':')
        srcPort = flow['srcPort'].replace('.', ':')
        dstPort = flow['dstPort'].replace('.', ':')
        flowsample = srcIP + ':' + dstIP + ':' + srcPort + ':' + dstPort
        fs_update = datetime.datetime.now() - flow['stime']
        fs_update = fs_update.total_seconds()
        self.model.update_online(flowsample, fs_update)

    # TODO: Add nwflowestimator


def main():
    estm = SizeEstimator()
    estm.gflowestm_train()
    estm.gflowestm_predict()


if __name__ == "__main__":
    main()
