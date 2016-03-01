from dataset import *
from classifier import *
from evaluator import *
from knn import *
from naivebayes import *


class TrainTestSets(object):
    def __init__(self, options=[]):  # error if the examples can not be added because of type or memory problems
        self.test = DataSet(Attributes())
        self.train = DataSet(Attributes())
        self.mode = 0  # 1 if only training file, 2 if test file specified
        self.setOptions(options)

    def __str__(self):
        return "Training Set:\n{}\n\nTest Set:\n{}".format(self.train, self.test)

    def __repr__(self):
        return self.__str__()

    def getMode(self):
        return self.mode

    def getTestingSet(self):
        return self.test

    def getTrainingSet(self):
        return self.train

    def setTestingSet(self, test):
        self.test.addDataset(test)

    def setTrainingSet(self, train):  # error java.lang.Exception
        self.train.addDataset(train)

    ## parse through command line options
    def setOptions(self, opts):  # error if an option is illegal
        trainTag = '-t'
        testTag = '-T'
        trainInd = -1

        # if no sets are specified
        if len(opts) == 1:
            return

        # the training set is specified
        if trainTag in opts:
            self.mode = 1
            trainInd = opts.index(trainTag) + 1
            if trainInd >= len(opts):  # index is out of bounds
                self.loadOptionsError(opts, "Missing argument")
            self.train.load(opts[trainInd])

        # the test set is specified
        if testTag in opts:
            self.mode = 2
            next = opts.index(testTag) + 1
            if next >= len(opts):  # index is out of bounds
                self.loadOptionsError(opts, "Missing argument")
            self.test.load(opts[next])

            # if no training set is specified and we're in test mode,
            # something went wrong
            if trainInd == -1:
                self.loadOptionsError(opts, \
                    "Missing training set. Commands must be in the following syntax:")
            else:
                return

        # if no test set is specified, we're okay
        if self.mode == 1:
            return

        # if no other cases have matched, something's wrong
        self.loadOptionsError(opts)

    ## throw an error message with the correct syntax for options
    def loadOptionsError(self, opts, msg="Invalid Syntax"):
        base = " [-t <path> [-T <path>]] [-x folds]"
        knnSyntax = "./kNN" + base + " [-k neighbors]"
        nbSyntax = "./NaiveBayes" + base
        if './kNN' in opts:
            raise SyntaxError(msg + "\n" + knnSyntax)
        elif './NaiveBayes' in opts:
            raise SyntaxError(msg + "\n" + nbSyntax)
        else:
            raise SyntaxError(msg + "\n" + knnSyntax + "\n" + nbSyntax)
