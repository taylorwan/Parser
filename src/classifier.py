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


## throw an error message with the correct syntax for options
def loadOptionsError(opts, msg="Invalid Syntax. Valid commands:"):
    base = "main.py "
    options = " [-t <path> [-T <path>]]"
    knnSyntax = base + "kNN" + options + " [-k neighbors] [-x folds]"
    nbSyntax = base + "NaiveBayes" + options + " [-x folds]"
    id3Syntax = base + "ID3" + options + " [-p proportion]"
    bpSyntax = base + "BP" + options + " [-j hiddenNodes] [-p proportion] [-n learningRate]"
    if 'kNN' in opts or 'knn' in opts:
        raise SyntaxError(msg + "\n" + knnSyntax)
    elif 'NaiveBayes' in opts or 'naivebayes' in opts:
        raise SyntaxError(msg + "\n" + nbSyntax)
    elif 'ID3' in opts or 'id3' in opts:
        raise SyntaxError(msg + "\n" + id3Syntax)
    elif 'BP' in opts or 'bp' in opts:
        raise SyntaxError(msg + "\n" + bpSyntax)
    else:
        raise SyntaxError(msg + "\n" + knnSyntax + "\n" + nbSyntax + "\n" + id3Syntax + "\n" + bpSyntax)


# check if option is valid
def validOption(o, opts):
    if o in opts:
        next = opts.index(o) + 1
        if next >= len(opts):
            loadOptionsError(opts, "Missing argument for " + o)
        return [next, o, opts]
    return [-1, o, opts]


# get the value in the next index of opts as an int
def getNextAsInt(next):
    if next[0] > -1:
        try:
            return int(next[2][next[0]])
        except:
            loadOptionsError(opts, "Invalid argument for " + next[1])


# get the value in the next index of opts as a float
def getNextAsFloat(next):
    if next[0] > -1:
        try:
            return float(next[2][next[0]])
        except:
            loadOptionsError(opts, "Invalid argument for " + next[1])
