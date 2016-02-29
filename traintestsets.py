from dataset import *
from classifier import *
from evaluator import *
from knn import *
from naivebayes import *


class TrainTestSets(object):
    def __init__(self, options=[]):  # error if the examples can not be added because of type or memory problems
        self.test = DataSet(Attributes())
        self.train = DataSet(Attributes())
        self.mode = 0  # 1 if testing, 2 if training
        self.setOptions(options[1:])

    def __str__(self):
        return "Training Set:\n{}\n\nTest Set:\n{}".format(self.train, self.test)

    def __repr__(self):
        return self.__str__()

    def getTestingSet(self):
        return self.test

    def getTrainingSet(self):
        return self.train

    def setOptions(self, opts):  # error if an option is illegal
        trainTag = '-t'
        testTag = '-T'
        if len(opts) == 0:
            return
        elif trainTag in opts:
            self.mode = 1
            next = opts.index(trainTag) + 1
            self.train.load(opts[next])
        elif testTag in opts:
            self.mode = 2
            next = opts.index(testTag) + 1
            self.test.load(opts[next])

        # if 'knn' in opts:
        #     c = KNN()
        #     Evaluator(c).evaluate(self.train)

        # elif 'nb' in opts or 'naivebayes' in opts:
        #     c = NaiveBayes()
        #     Evaluator(c).evaluate(self.train)

    def setTestingSet(self, test):
        self.test.addDataset(test)
        return "Success"

    def setTrainingSet(self, train):  # error java.lang.Exception
        self.train.addDataset(train)
        return "Success"

    def main(self):  # error if the examples can not be added because of type or memory problems
        print
        print "TrainTestSets::main"
        print "self: {}".format(self)
        print "self.mode: {}".format(self.mode)
        g = DataSet(Attributes())
        g.main()
        print "self.setTrainingSet(g): {}".format(self.setTrainingSet(g))
        print "self.setTestingSet(DataSet(Attributes())): {}".format(self.setTestingSet(DataSet(Attributes())))
