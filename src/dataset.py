import random
import math
from examples import *
from attributes import *
from node import *


class DataSet(object):
    def __init__(self, attributes=Attributes()):  # error if the examples can not be added because of type or memory problems
        self.name = ''
        self.attributes = attributes
        self.examples = Examples(attributes)
        self.seed = -1
        self.setSeed()
        self.counts = []

    def __str__(self):
        chart = "@dataset {}\n\n".format(self.name)
        chart += str(self.attributes) + "\n"
        chart += str(self.examples)
        return chart

    def __repr__(self):
        return self.__str__()

    def addDataset(self, dataset):  # error if the examples can not be added because of type or memory problems
        for example in dataset.getExamples():
            self.addExample(example)

    def addExample(self, example):  # error if the example can not be added because of type or memory problems
        self.examples.add(example)

    def getAttributes(self):
        return self.attributes

    def getExamples(self):
        return self.examples

    def getHasNominalAttributes(self):
        return self.attributes.getHasNominalAttributes()

    def getHasNumericAttributes(self):
        return self.attributes.getHasNumericAttributes()

    def getSeed(self):
        return self.seed

    def load(self, filename):  # error if the file is not found or if a parse error occurs
        with open(filename) as f:
            return self.parse(f.read())

    ## determine whether type a line in a dataset file is a:
    ## - dataset header
    ## - attribute declaration
    ## - example
    ## and parse accordingly
    def parse(self, scanner):  # error if a parse error occurs
        exampleSec = False
        for line in scanner.split("\n"):
            if line == '':
                continue
            words = line.split(" ")

            # parse an example line
            if exampleSec:
                self.examples.parse(line)
            # parse the dataset header
            elif words[0] == '@dataset':
                self.name = words[1]
            # parse an attribute line
            elif words[0] == '@attribute':
                self.attributes.parse(line)

            # if we encounter the word @examples, all
            # remaining lines are examples
            elif words[0] == '@examples':
                exampleSec = True

            # unknown case, the file does not follow correct .mff grammar
            else:
                raise RuntimeError("File does not follow correct .mff grammar")

    ## parse through command line options
    def setOptions(self, opts):  # error if an option is illegal
        if '-s' in opts:
            setSeed(random.random())

    ## generate a random number for our seed
    def setSeed(self):
        self.seed = random.random()

    ##
    ## ID3
    ##

    ## create decision tree
    def train(self, node=None, attr=None, maj=None):
        classIndex = self.attributes.getClassIndex()
        self.counts = self.countSet(classIndex)

        if maj is not None:
            return Node(attr, maj)
        if self.isHomogenous():
            return Node(attr, self.getLabel(classIndex))

        a = self.getBestSplittingAttribute(classIndex)
        ds = self.split(a)
        n = Node(a.getName())
        children = []

        for d in ds:

            # if this split has no examples, set its value to
            # the majority value of the current branch
            if len(d.getExamples()) == 0:
                ch = d.train(n, a, self.getMajorityLabelIndex())
                children.append(ch)
                continue

            ch = d.train(n, a)
            children.append(ch)

        n.setChildren(children)

        return n

    # # split along a certain attribute
    def split(self, a):
        if isinstance(a, NumericAttribute):
            raise RuntimeError(a.name + "is numeric. We do not currently handle splitting among numeric attributes.")
        ds = []
        attrName = a.getName()
        for i, v in enumerate(a.getDomain()):
            ds.append(DataSet(self.attributes))
            di = self.attributes.getIndex(attrName)

            for e in self.examples:
                if e[di] == i:
                    ds[i].addExample(e)

        return ds

    ## returns the information gain if we split along a specified
    ## attribute
    def gain(self, a, classIndex):
        g = self.entropy(self.counts)  # start with entropy of the current set
        ds = self.split(a)  # split into children

        # subtract entropy of each child (multiplied by a proportion)
        for d in ds:
            curCounts = d.countSet(classIndex)
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
    def getLabel(self, classIndex):
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
    def countSet(self, classIndex):
        domain = self.attributes.getClassAttribute().getDomain()
        counts = [0 for x in range(len(domain))]

        # tally up the examples
        for e in self.examples:
            counts[e[classIndex]] += 1

        return counts

    ## return the attribute that we should split on at a
    ## particular node
    def getBestSplittingAttribute(self, classIndex):
        best = -1  # max gain
        bestAttr = -1  # best attribute

        # loop through all attributes (except class attr) to find
        # the one that produces max gain
        for i, a in enumerate(self.attributes.getAttributes()):
            if i == classIndex:
                continue
            g = self.gain(a, classIndex)
            if g > best:
                best = g
                bestAttr = a
        return bestAttr

    ##
    ## BP
    ##

    ## translate the current attriutes to binary encoding
    def nominalToBinary(self):
        # print "nominalToBinary"
        ds = DataSet(Attributes())
        classAttr = self.attributes.getClassAttribute()
        self.convertAttr(ds, classAttr)
        for e in self.examples:
            self.convertExample(e, ds, classAttr)
        return ds

    ## reformats attributes
    def convertAttr(self, ds, classAttr):
        for a in self.attributes.attributes:
            if a == classAttr:
                ds.getAttributes().add(a)
                break

            # if a is numeric, append it to our list
            if isinstance(a, NumericAttribute):
                ds.getAttributes().add(a)
                continue

            # since a is nominal, get its domain
            d = a.getDomain()
            l = len(d)

            # if a is already binary, proceed
            if l <= 2:
                ds.getAttributes().add(a)
                continue

            # else, use binary encoding to create multiple buckets
            buckets = self.findSmallestBits(l)
            for i in range(buckets):
                b = NominalAttribute(a.name + str(i))
                b.addValue("0")
                b.addValue("1")
                ds.getAttributes().add(b)

        return ds.getAttributes()

    ## reformats a single example
    def convertExample(self, e, ds, classAttr):
        ex = Example(len(ds.getAttributes().getAttributes()))
        for i, a in enumerate(self.attributes.attributes):
            if a == classAttr:
                ex.append(e[i])
                continue

            # if a is numeric, append it to our list
            if isinstance(a, NumericAttribute):
                ex.append(e[i])
                continue

            # since a is nominal, get its domain
            d = a.getDomain()
            l = len(d)

            # if a is already binary, proceed
            if l <= 2:
                ex.append(e[i])
                continue

            # else, determine the binary value and append
            ind = self.processBin(e[i], self.findSmallestBits(l))
            for c in ind:
                ex.append(int(c))

        ds.addExample(ex)
        return ex

    ## find the smallest exp such that 2^exp > n
    def findSmallestBits(self, n):
        exp = 1
        while 2 ** exp < n:
            exp += 1
        return exp

    ## given numbers n and b, convert n to the string of a
    ## binary number
    def processBin(self, n, b):
        s = str(bin(n))[2:]
        while len(s) < b:
            s = "0" + s
        return s
