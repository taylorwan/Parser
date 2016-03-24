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
        root = ds.train()
        perf = 0
        for inst in self.instances.getExamples():
            self.vote = self.classify(inst, root)
            if self.vote == inst[-1]:
                perf += 1
        avgPerf = perf * 100.0 / len(self.instances.getExamples())
        return Performance(avgPerf)


## throw an error message with the correct syntax for options
def loadOptionsError(self, opts, msg="Invalid Syntax"):
    base = " [-t <path> [-T <path>]] [-x folds]"
    knnSyntax = "kNN" + base + " [-k neighbors]"
    nbSyntax = "NaiveBayes" + base
    id3Syntax = "id3" + base + " [-p proportion]"
    if './kNN' in opts or 'knn.py' in opts:
        raise SyntaxError(msg + "\n" + knnSyntax)
    elif './NaiveBayes' in opts or 'naivebayes.py' in opts:
        raise SyntaxError(msg + "\n" + nbSyntax)
    elif './ID3' in opts or 'id3.py' in opts:
        raise SyntaxError(msg + "\n" + id3Syntax)
    else:
        raise SyntaxError(msg + "\n" + knnSyntax + "\n" + nbSyntax + "\n" + id3Syntax)
