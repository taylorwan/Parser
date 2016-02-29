import random
from examples import *
from attributes import *


class DataSet(object):
    def __init__(self, attributes=Attributes()):  # error if the examples can not be added because of type or memory problems
        self.name = 'Unnamed'
        self.attributes = attributes
        self.examples = Examples(attributes)
        self.seed = -1
        self.random = random.random()

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

    def parse(self, scanner):  # error if a parse error occurs
        exampleSec = False
        for line in scanner.split("\n"):
            if line == '':
                continue

            words = line.split(" ")
            if exampleSec:
                self.examples.parse(line)
            elif words[0] == '@dataset':
                self.name = words[1]
            elif words[0] == '@attribute':
                self.attributes.parse(line)
            elif words[0] == '@examples':
                exampleSec = True
        return "Success"

    def setOptions(self, options):  # error if an option is illegal
        if len(options) == 1:
            pass
        elif options[1] == '-s':
            setSeed(random.random())
        else:
            raise ValueError("Illegal option: " + " ".join(options[1:]))

    def setSeed(self, seed):
        self.seed = seed

    def main(self):
        print
        print "DataSet::main"
        print self.getAttributes()
        print self.getExamples()
        print "self.load(bikes.mff): {}".format(self.load("bikes.mff"))
        print self
        print self.getAttributes()
        print self.getExamples()
