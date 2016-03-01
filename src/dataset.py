import random
from examples import *
from attributes import *


class DataSet(object):
    def __init__(self, attributes=Attributes()):  # error if the examples can not be added because of type or memory problems
        self.name = 'Unnamed'
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
