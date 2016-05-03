from classifier import *
from traintestsets import *
from operator import *
from id3 import *


class Forest(Classifier):
    def __init__(self, e=DataSet(), i=DataSet(), trees=[], m=3, sz=10):
        super(Forest, self).__init__(e, i)
        self.trees = trees
        self.m = m
        self.sz = sz
        self.type = 'Random Forest'

    def __str__(self):
        return super(Forest, self).__str__()

    def __repr__(self):
        return self.__str__()

    ## parse through command line options
    def setOptions(self, opts):
        nextVal = getNextAsInt(validOption('-m', opts))
        if nextVal:
            # make sure m isn't even
            if nextVal % 2 != 0:
                self.m = nextVal
            else:
                self.m = nextVal + 1

    # create m trees
    def train(self, ds):
        for i in range(self.m):
            self.createTree(ds)

    # generate a random tree
    def createTree(self, ds):
        self.sz = self.initSize(ds)
        d = self.createSubSet(ds)
        self.trees.append(ID3(d).train())

    # generate a random size, with an upper bound of 0.6 the size of ds
    def initSize(self, ds):
        rand = self.random(ds)
        return int(len(ds.getExamples())*0.2 + rand*0.6)

    # creates a random subset
    def createSubSet(self, ds):
        data = DataSet(ds.getAttributes())
        exs = ds.getExamples()

        # fill subset up to that size
        for i in range(self.sz):
            randInd = self.random(ds)
            data.addExample(exs[randInd])

        # if we haven't added any examples, try again
        if data.isEmpty():
            return self.createSubSet(ds)

        # otherwise, return our subset
        return data

    # if ds is defined, returns a random # < # of examples in ds
    # otherwise, randomly returns false 2/3 of the time
    def random(self, ds=None):
        if ds:
            return int(random.random() * len(ds.examples))
        return int(random.random() * 3) == 0

    def getMaxValueKey(self, v):
        return max(v.iteritems(), key=operator.itemgetter(1))[0]

    def initVotes(self):
        votes = {}
        classAttrDomain = self.examples.getAttributes().getClassAttribute().getDomain()
        for val in range(len(classAttrDomain)):
            votes[val] = 0
        return votes

    ## classify our set, and return the performance
    def classifySet(self, ds):
        perf = 0
        for inst in self.instances.getExamples():
            self.vote = self.classify(inst)
            if self.vote == inst[-1]:
                perf += 1
        avgPerf = perf * 100.0 / len(self.instances.getExamples())
        return Performance(avgPerf)

    ## predict outcome of a single example (test)
    def classify(self, inst):
        votes = self.initVotes()
        for t in self.trees:
            c = t
            while len(c.children) > 0:
                attr = c.getAttribute()
                attrInd = self.examples.getAttributes().getIndex(attr)
                i = inst[attrInd]
                c = c.getChildren()[i]
            vote = c.getLabel()
            votes[vote] += 1

        return self.getMaxValueKey(votes)
