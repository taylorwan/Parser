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
    ## BP
    ##

    ## translate the current attriutes to binary encoding
    def nominalToBinary(self):
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
