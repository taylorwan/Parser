import math
from performance import *
from classifier import *


class Evaluator(object):
    def __init__(self, c, f=10):
        self.classifier = c
        self.folds = f
        self.performance = []
        self.avgPerf = -1
        self.accuracy = -1
        self.setOptions(sys.argv)

    def __str__(self):
        output = "{}-fold cross validation with {}\n".format(self.folds, self.classifier.getName())
        for i, p in enumerate(self.performance):
            output += "Test Set {}: {:.{prec}f}%\n".format(i+1, p, prec=2)
        output += "Accuracy: {:.{prec}f} +- {:.{prec}f}".format(self.avgPerf, self.accuracy, prec=2)
        return output

    def __repr__(self):
        return self.__str__()

    def setOptions(self, opts):
        x = '-x'
        if x in opts:
            next = opts.index(x) + 1
            if int(opts[next]) > 1:
                self.folds = int(opts[next])

    def avg(self, l):
        return sum(l) / float(len(l))

    def std(self, l):
        avg = self.avg(l)
        var = sum([pow(x-avg, 2) for x in l])/float(len(l)-1)
        return math.sqrt(var)

    def createTestSet(self, ds, offset=0):
        self.classifier.examples = DataSet(ds.getAttributes())
        self.classifier.instances = DataSet(ds.getAttributes())
        for i, ex in enumerate(ds.getExamples()):
            if i % self.folds == offset:
                self.classifier.instances.addExample(ex)
            else:
                self.classifier.examples.addExample(ex)

    def evaluate(self, ds):
        if len(ds.getExamples()) < self.folds:
            self.folds = len(ds.getExamples())
        for i in range(self.folds):
            self.createTestSet(ds, i)
            self.performance.append(self.classifier.classifySet(ds).getAccuracy())
        self.avgPerf = self.avg(self.performance)
        self.accuracy = self.std(self.performance)
        print self
