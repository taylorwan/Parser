import operator
import sys
from nominalattribute import *
from numericattribute import *
from performance import *
from dataset import *


class Classifier(object):

    def __init__(self, e=DataSet(), i=DataSet()):
        self.examples = e  # training set
        self.instances = i  # test set
        self.name = 'Classifier'

    def __str__(self):
        output = "------ATTRIBUTES------\n{}\n\n".format(self.examples.getAttributes())
        output += "------EXAMPLES------\n{}\n\n".format(self.examples.getExamples())
        output += "------INSTANCES-----\n{}\n".format(self.instances.getExamples())
        return output

    def __repr__(self):
        return self.__str__()

    def getName(self):
        return self.name

    def train(self, ds):
        self.examples = ds

    def setExamples(self, ds):
        self.examples = ds

    def setInstances(self, ds):
        self.instances = ds

    def classifySet(self, ds):
        perf = 0
        for inst in self.instances.getExamples():
            self.vote = self.classify(inst)
            if self.vote == inst[-1]:
                perf += 1
        avgPerf = perf * 100.0 / len(self.instances.getExamples())
        return Performance(avgPerf)
