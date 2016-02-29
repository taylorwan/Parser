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


class KNN(Classifier):
    def __init__(self, e=DataSet(), i=DataSet(), k=3):
        super(KNN, self).__init__(e, i)
        self.k = k
        self.setOptions(sys.argv[1:])
        self.name = 'KNN'

    def __str__(self):
        output = super(KNN, self).__str__()
        output += "------K-----\n{} nearest neighbors\n".format(self.k)
        return output

    def __repr__(self):
        return self.__str__()

    def setOptions(self, opts):
        k = '-k'
        if k in opts:
            next = opts.index(k) + 1
            self.k = int(opts[next])

    def calcDist(self, inst, ex):
        dist = 0
        for i in range(len(inst)-1):
            if inst[i] != ex[i]:
                dist += 1
        return dist

    def closestK(self, l):
        l.sort()
        return l[:self.k]

    def calcVote(self, l):
        votes = {}
        for t in l:
            if t[1] in votes:
                votes[t[1]] += 1
            else:
                votes[t[1]] = 1
        self.vote = self.getMaxValueKey(votes)
        return self.vote

    def getMaxValueKey(self, v):
        return max(v.iteritems(), key=operator.itemgetter(1))[0]

    def classify(self, inst):
        results = []
        # create list of indicies [distance, classIndex] for each example
        for ex in self.examples.getExamples():
            results.append([self.calcDist(inst, ex), ex[-1]])
        neighbors = self.closestK(results)
        return self.calcVote(neighbors)


def main():
    try:
        ds = TrainTestSets(sys.argv)
        Evaluator(KNN()).evaluate(ds.getTrainingSet())
    except Exception as e:
        print e.args[0]


if __name__ == "__main__":
    main()
