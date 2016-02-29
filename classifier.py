from nominalattribute import *
from numericattribute import *
from performance import *
from dataset import *


class Classifier(object):

    def __init__(self, e=DataSet(), i=DataSet()):
        self.examples = e  # training set
        self.instances = i  # test set
        self.type = 'Classifier'

    def __str__(self):
        return "{}".format(self.type)

    def __repr__(self):
        return self.__str__()

    def getType(self):
        return self.type

    def train(self, ds):
        self.setExamples(ds)

    def getExamples(self):
        return self.examples

    def getInstances(self):
        return self.instances

    def setExamples(self, ds):
        self.examples = ds

    def setInstances(self, ds):
        self.instances = ds

    ## determine values and return the average performance
    ## for all examples (our test set)
    def classifySet(self, ds):
        perf = 0
        for inst in self.instances.getExamples():
            self.vote = self.classify(inst)
            if self.vote == inst[-1]:
                perf += 1
        avgPerf = perf * 100.0 / len(self.instances.getExamples())
        return Performance(avgPerf)
