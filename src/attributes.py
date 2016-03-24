from nominalattribute import *
from numericattribute import *
from attributefactory import *


class Attributes(object):
    def __init__(self):
        self.attributes = []
        self.classIndex = 0
        self.hasNominalAttributes = False
        self.hasNumericAttributes = False

    def __str__(self):
        printout = ""
        if self.attributes:
            for a in self.attributes:
                printout += "@attribute " + str(a) + "\n"
        else:
            printout += "Empty"
        return printout

    def __repr__(self):
        return self.__str__()

    def getSize(self):
        return len(self.attributes)

    def get(self, i):  # error if the index is out of bounds
        return self.attributes[i]

    def getHasNominalAttributes(self):
        return self.hasNominalAttributes

    def getHasNumericAttributes(self):
        return self.hasNumericAttributes

    def getClassAttribute(self):  # error if the class index is out of bounds
        return self.attributes[self.classIndex]

    def getAttributes(self):
        return self.attributes

    def getIndex(self, name):  # error if the name is illegal
        for i, a in enumerate(self.attributes):
            if a.name == name:
                return i
        raise RuntimeError("Invalid Label " + name)

    def getClassIndex(self):  # error if the class index is out of range
        return self.classIndex

    def setClassIndex(self, classIndex):  # error if the class index is out of bounds
        self.classIndex = classIndex

    ## add an attribute to our attribute list, and update which values we have
    def add(self, attribute):  # error if the attribute cannot be added because of type or memory problems
        self.attributes.append(attribute)
        if isinstance(attribute, NumericAttribute):
            self.hasNumericAttributes = True
        elif isinstance(attribute, NominalAttribute):
            self.hasNominalAttributes = True
        return attribute

    ## parse through a list of attributes, create and add them our list
    def parse(self, scanner):  # error if a parse error occurs
        m = AttributeFactory()
        s = m.make(scanner)
        self.attributes.append(s)
        self.setClassIndex(self.getSize()-1)
