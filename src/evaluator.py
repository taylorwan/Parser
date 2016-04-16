import sys
import math
from performance import *
from classifier import *


class Evaluator(object):
    def __init__(self, c):
        self.classifier = c
        self.folds = 10
        self.p = 0.3
        self.performance = []
        self.avgPerf = -1
        self.accuracy = -1
        self.setOptions(sys.argv)

    def __str__(self):
        # if just one performance result
        if len(self.performance) == 1:
            return "{}\nAccuracy: {:.2f}%".format(self.classifier, self.avgPerf, prec=2)

        output = "{}-fold cross validation with {}\n".format(self.folds, self.classifier)
        for i, p in enumerate(self.performance):
            output += "Test Set {}: {:.{prec}f}%\n".format(i+1, p, prec=2)
        output += "Accuracy: {:.{prec}f} +- {:.{prec}f}".format(self.avgPerf, self.accuracy, prec=2)
        return output

    def __repr__(self):
        return self.__str__()

    ## parse through command line options
    def setOptions(self, opts):
        nextVal = getNextAsInt(validOption('-x', opts))
        if nextVal:
            self.folds = nextVal

        nextVal = getNextAsFloat(validOption('-p', opts))
        if nextVal:
            self.p = nextVal

    ##
    ## Dataset Splitting
    ##

    ## partition the training data randomly to create our test set
    def createCrossValidateTestSet(self, ds, offset=0):
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

    ## partition the training data and randomly hold out data
    def createHoldOutTestSet(self, ds):
        self.classifier.examples = DataSet(ds.getAttributes())
        self.classifier.instances = DataSet(ds.getAttributes())

        # use our seed to determine if the current example should
        # be partitioned into the training or test set
        for ex in ds.getExamples():
            i = ds.getSeed()

            if i > self.p:  # add to training set
                self.classifier.examples.addExample(ex)
            else:  # add to test set
                self.classifier.instances.addExample(ex)

            # choose a new random number
            ds.setSeed()

    ##
    ## Evaluate
    ##

    def evaluate(self, ds, test=None):
        if self.classifier.type == 'Naive Bayes' or self.classifier.type == 'k-NN':
            self.crossValidateEvaluate(ds, test)
        elif self.classifier.type == 'ID3' or self.classifier.type == 'BP':
            self.holdOutEvaluate(ds, test)
        else:
            raise RuntimeError('Invalid classifier: ' + self.classifier.type)

    ## evaluate the performance over our test sets using hold-out
    def holdOutEvaluate(self, ds, test=None):
        # if we are given a test set, use the test set
        if test is not None:
            self.classifier.setExamples(ds)
            self.classifier.setInstances(test)

        # otherwise, randomly create combinations of test sets and
        # training sets until our test set is not empty
        else:
            self.createHoldOutTestSet(ds)
            while (len(self.classifier.getInstances().getExamples()) < 1):
                self.createHoldOutTestSet(ds)

        # train and get performance
        self.classifier.train(ds)
        self.performance.append(self.classifier.classifySet(ds).getAccuracy())

        # # calculate and print our performance
        self.avgPerf = self.avg(self.performance)
        print self

    ## evaluate the performance over our test sets using cross validation
    def crossValidateEvaluate(self, ds, test=None):
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
                self.createCrossValidateTestSet(ds, i)
                while (len(self.classifier.getInstances().getExamples()) < 1):
                    self.createCrossValidateTestSet(ds, i)
                self.performance.append(self.classifier.classifySet(ds).getAccuracy())

        # calculate and print our performance
        self.avgPerf = self.avg(self.performance)
        self.accuracy = self.std(self.performance)
        print self

    ##
    ## Helpers
    ##

    ## calculate the average for a list of values
    def avg(self, l):
        return sum(l) / float(len(l))

    ## calculate the standard variation for a list of values
    def std(self, l):
        avg = self.avg(l)
        var = sum([pow(x-avg, 2) for x in l])/float(len(l))
        return math.sqrt(var)
