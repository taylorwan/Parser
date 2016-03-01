import sys
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
        output = "{}-fold cross validation with {}\n".format(self.folds, self.classifier)
        for i, p in enumerate(self.performance):
            output += "Test Set {}: {:.{prec}f}%\n".format(i+1, p, prec=2)
        output += "Accuracy: {:.{prec}f} +- {:.{prec}f}".format(self.avgPerf, self.accuracy, prec=2)
        return output

    def __repr__(self):
        return self.__str__()

    ## parse through command line options
    def setOptions(self, opts):
        x = '-x'
        if x in opts:
            next = opts.index(x) + 1
            if next >= len(opts):
                raise SyntaxError("Missing argument")
            self.folds = int(opts[next])

    ## calculate the average for a list of values
    def avg(self, l):
        return sum(l) / float(len(l))

    ## calculate the standard variation for a list of values
    def std(self, l):
        avg = self.avg(l)
        var = sum([pow(x-avg, 2) for x in l])/float(len(l)-1)
        return math.sqrt(var)

    ## partition the training data randomly to create our test set
    def createTestSet(self, ds, offset=0):
        self.classifier.examples = DataSet(ds.getAttributes())
        self.classifier.instances = DataSet(ds.getAttributes())

        # use our seed to determine if the current example should
        # be partitioned into the training or test set
        for ex in ds.getExamples():
            i = int(ds.getSeed() * self.folds)

            # add to test set if the random number matches our "offset"
            if i % self.folds == offset:
                self.classifier.instances.addExample(ex)

            # otherwise, add it to our training set
            else:
                self.classifier.examples.addExample(ex)

            # choose a new random number
            ds.setSeed()

    ## evaluate the performance over our test sets
    def evaluate(self, ds, test=None):
        # if we don't have as many examples as the # of folds
        # currently set, reduce the # of folds until we have
        # at least one example per fold
        if len(ds.getExamples()) < self.folds:
            self.folds = len(ds.getExamples())

        # if we are given a test set, use the test set
        if test is not None:
            self.classifier.setExamples(ds)
            self.classifier.setInstances(test)
            self.performance.append(self.classifier.classifySet(ds).getAccuracy())

        # otherwise, randomly create combinations of test sets and
        # training sets until our test set is not empty
        else:
            for i in range(self.folds):
                self.createTestSet(ds, i)
                while (len(self.classifier.getInstances().getExamples()) < 1):
                    self.createTestSet(ds, i)
                self.performance.append(self.classifier.classifySet(ds).getAccuracy())

        # calculate and print our performance
        self.avgPerf = self.avg(self.performance)
        self.accuracy = self.std(self.performance)
        print self
