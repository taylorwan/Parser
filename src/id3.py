from classifier import *
from traintestsets import *


class ID3(Classifier):
    def __init__(self, e=DataSet(), i=DataSet(), root=Node(), p=.1):
        super(ID3, self).__init__(e, i)
        self.type = 'ID3'
        self.counts = []
        self.root = Node()

    def __str__(self):
        return super(ID3, self).__str__()

    def __repr__(self):
        return self.__str__()

    ##
    ## Train
    ##

    ## create decision tree
    def train(self, ds, node=None, attr=None, maj=None):
        classIndex = ds.attributes.getClassIndex()
        self.counts = self.countSet(ds, classIndex)

        if maj is not None:
            return Node(attr, maj)
        if self.isHomogenous():
            return Node(attr, self.getLabel(ds, classIndex))

        a = self.getBestSplittingAttribute(ds, classIndex)
        dSet = self.split(ds, a)
        n = Node(a.getName())
        children = []

        for d in dSet:

            # if this split has no examples, set its value to
            # the majority value of the current branch
            if len(d.examples.getExamples()) == 0:
                ch = d.train(ds, n, a, self.getMajorityLabelIndex())
                children.append(ch)
                continue

            ch = d.train(ds, n, a)
            children.append(ch)

        n.setChildren(children)

        return n

    ##
    ## Helpers
    ##

    # # split along a certain attribute
    def split(self, ds, a):
        if isinstance(a, NumericAttribute):
            raise RuntimeError(a.name + "is numeric. We do not currently handle splitting among numeric attributes.")
        dSet = []
        attrName = a.getName()
        for i, v in enumerate(a.getDomain()):
            dSet.append(ID3())
            di = ds.attributes.getIndex(attrName)

            for e in ds.examples:
                if e[di] == i:
                    dSet[i].examples.addExample(e)

        return dSet

    ## returns the information gain if we split along a specified
    ## attribute
    def gain(self, ds, a, classIndex):
        g = self.entropy(self.counts)  # start with entropy of the current set
        dSet = self.split(ds, a)  # split into children

        # subtract entropy of each child (multiplied by a proportion)
        for d in dSet:
            curCounts = d.countSet(ds, classIndex)
            ratio = sum(curCounts) * 1.0 / sum(self.counts)
            entropy = d.entropy(curCounts)
            g -= ratio * entropy
        return g

    ## calculate entropy of the current set
    def entropy(self, counts):
        total = sum(counts)  # total count
        res = 0  # stores result

        # calculate value for each label value
        for c in counts:
            if c == 0:
                continue
            ratio = c * 1.0 / total  # forces answer to be a float
            res -= ratio * math.log(ratio)/math.log(2)

        return res

    ## determine whether all examples are homogenous
    def isHomogenous(self):
        total = 0

        # add 1 for each non-zero count
        for i, c in enumerate(self.counts):
            if c > 0:
                total += 1

        return total <= 1

    ## return the label of the first example in our set
    ## helpful when the set is homogenous
    def getLabel(self, ds, classIndex):
        if len(self.examples) > 0:
            return self.examples[0][classIndex]

    ## return the index of the label with the most examples
    def getMajorityLabelIndex(self):
        v = max(self.counts)
        for i, c in enumerate(self.counts):
            if c == v:
                return i

    ## count the number of examples per class label in the current
    ## data set
    def countSet(self, ds, classIndex):
        domain = ds.attributes.getClassAttribute().getDomain()
        counts = [0 for x in range(len(domain))]

        # tally up the examples
        for e in ds.examples:
            counts[e[classIndex]] += 1

        return counts

    ## return the attribute that we should split on at a
    ## particular node
    def getBestSplittingAttribute(self, ds, classIndex):
        best = -1  # max gain
        bestAttr = -1  # best attribute

        # loop through all attributes (except class attr) to find
        # the one that produces max gain
        for i, a in enumerate(ds.attributes.getAttributes()):
            if i == classIndex:
                continue
            g = self.gain(ds, a, classIndex)
            if g > best:
                best = g
                bestAttr = a
        return bestAttr

    ##
    ## Classify
    ##

    ## classify our set, and return the performance
    def classifySet(self, ds):
        # root = ds.train()
        perf = 0
        for inst in self.instances.getExamples():
            self.vote = self.classify(inst, root)
            if self.vote == inst[-1]:
                perf += 1
        avgPerf = perf * 100.0 / len(self.instances.getExamples())
        return Performance(avgPerf)

    ## predict outcome of a single example (test)
    def classify(self, inst, root):
        c = root
        while len(c.children) > 0:
            attr = c.getAttribute()
            i = self.examples.getAttributes().getIndex(attr)
            c = c.getChildren()[i]
        return c.getLabel()
