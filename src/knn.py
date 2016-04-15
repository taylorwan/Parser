#
# Taylor Wan
# tw476@georgetown.edu
# Platform: OS X
# Language/Environment: python
#
# In accordance with the class policies and Georgetown's Honor Code,
# I certify that, with the exceptions of the class resources and those
# items noted below, I have neither given nor received any assistance
# on this project.
#

import operator
from classifier import *
from traintestsets import *


class kNN(Classifier):
    def __init__(self, e=DataSet(), i=DataSet(), k=3):
        super(kNN, self).__init__(e, i)
        self.k = k
        self.setOptions(sys.argv[1:])
        self.type = 'k-NN'

    def __str__(self):
        return super(kNN, self).__str__() + " (k={})".format(self.k)

    def __repr__(self):
        return self.__str__()

    ## parse through command line options
    def setOptions(self, opts):
        k = '-k'
        if k in opts:
            next = opts.index(k) + 1
            if next >= len(opts):
                loadOptionsError(opts, "Missing argument for -k")
            self.k = int(opts[next])

    ## calculate the distance between two examples
    def calcDist(self, inst, ex):
        dist = 0
        for i in range(len(inst)-1):
            if inst[i] != ex[i]:
                dist += 1
        return dist

    ## return the closest k values given an array with
    ## format [[distance1, C1], [distance2, C2], ... ]
    def closestK(self, l):
        l.sort()
        return l[:self.k]

    ## given a list of k closest neighbors with the format
    ## [[distance1, C1], [distance2, C2], ... ]
    ## determine the most comon class index, and return it
    def calcVote(self, l):
        if len(l) < 1:
            raise RuntimeError("Empty list")
        votes = {}
        for t in l:
            if t[1] in votes:
                votes[t[1]] += 1
            else:
                votes[t[1]] = 1
        self.vote = self.getMaxValueKey(votes)
        return self.vote

    ## return the key with the highest value in a dictionary
    def getMaxValueKey(self, v):
        return max(v.iteritems(), key=operator.itemgetter(1))[0]

    ## predict outcome of a single example (test)
    def classify(self, inst):
        results = []
        # create list of indicies [distance, classIndex] for each example
        for ex in self.examples.getExamples():
            results.append([self.calcDist(inst, ex), ex[-1]])
        neighbors = self.closestK(results)
        return self.calcVote(neighbors)


## initialize and evaluate
def main():
    try:
        ds = TrainTestSets(sys.argv)
        if len(ds.getTrainingSet().getExamples()) > 0:
            if len(ds.getTestingSet().getExamples()) > 0:
                Evaluator(kNN()).evaluate(ds.getTrainingSet(), ds.getTestingSet())
            else:
                Evaluator(kNN()).evaluate(ds.getTrainingSet())
    except Exception as e:
        if len(e.args) == 1:
            print e.args[0]
        else:
            print e.args[1]


if __name__ == "__main__":
    main()
