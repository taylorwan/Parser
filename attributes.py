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

    def getClassIndex(self):  # error if the class index is out of range
        return self.classIndex

    def setClassIndex(self, classIndex):  # error if the class index is out of bounds
        self.classIndex = classIndex

    def add(self, attribute):  # error if the attribute cannot be added because of type or memory problems
        self.attributes.append(attribute)
        if isinstance(attribute, NumericAttribute):
            self.hasNumericAttributes = True
        elif isinstance(attribute, NominalAttribute):
            self.hasNominalAttributes = True
        return attribute

    def parse(self, scanner):  # error if a parse error occurs
        m = AttributeFactory()
        s = m.make(scanner)
        self.attributes.append(s)
        self.setClassIndex(self.getSize()-1)

    def main(self):
        print
        print "Attributes::main"
        print "self: {}".format(self)

        lines = "@attribute make trek bridgestone cannondale nishiki garyfisher\n@attribute tires knobby treads\n@attribute bars straight curved\n@attribute bottles y n\n@attribute weight numeric\n@attribute type mountain hybrid"
        for line in lines.split("\n"):
            self.parse(line)

        print "self: {}".format(self)
        print "self.getSize(): {}".format(self.getSize())
        print "self.get(0): {}".format(self.get(0))
        print "self.getHasNominalAttributes(): {}".format(self.getHasNominalAttributes())
        print "self.getHasNumericAttributes(): {}".format(self.getHasNumericAttributes())
        print "self.getIndex(\"hey\"): {}".format(self.getIndex("hey"))
        print "self.getClassIndex(): {}".format(self.getClassIndex())
        print "self.get(getClassIndex()): {}".format(self.get(self.getClassIndex()))
        print "self.getClassAttribute(): {}".format(self.getClassAttribute())
        print "self.setClassIndex(0): {}".format(self.setClassIndex(0))
        print "self.add(NumericAttribute(\"num\")): {}".format(self.add(NumericAttribute("num")))
        print "self: {}".format(self)
        print "self.getIndex(\"num\")): {}".format(self.getIndex("num"))
        print "self.getHasNumericAttributes(): {}".format(self.getHasNumericAttributes())
