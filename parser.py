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

import random
import sys


class Attribute(object):

    def __init__(self, name=None):
        self.name = name
        self.size = 0

    def __str__(self):
        return "{}".format(self.name)

    def __repr__(self):
        return self.__str__()

    def getSize(self):
        return self.size

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name


class NominalAttribute(Attribute):

    def __init__(self, name=None):
        super(NominalAttribute, self).__init__(name)
        self.domain = []

    def __str__(self):
        return "{} ['{}']".format(self.name, "', '".join(self.domain))

    def __repr__(self):
        return self.__str__()

    def getIndex(self, value):  # error if the value is illegal
        return self.domain.index(value)

    def getValue(self, index):  # error if the index is out of bounds
        return self.domain[index]

    def addValue(self, value):  # error if the value can not be added
        self.domain.append(value)
        self.size += 1

    def main(self):
        print
        print "NominalAttribute::main"
        self.addValue("hey")
        self.addValue("hello")
        print "self: {}".format(self)
        print "self.getSize(): {}".format(self.getSize())
        print "self.getValue(1): {}".format(self.getValue(1))
        print "self.getIndex(self.getValue(1)): {}".format(self.getIndex(self.getValue(1)))


class NumericAttribute(Attribute):

    def __init__(self, name=None):
        super(NumericAttribute, self).__init__(name)

    def __str__(self):
        return "{} (numeric)".format(self.name)

    def __repr__(self):
        return self.__str__()

    def main(self):
        print
        print "NumericAttribute::main"
        print "self: {}".format(self)
        print "self.getSize(): {}".format(self.getSize())


class Attributes(object):
    def __init__(self):
        self.attributes = []
        self.classIndex = 0
        self.hasNominalAttributes = False
        self.hasNumericAttributes = False

    def __str__(self):
        printout = "@attributes\n"
        if self.attributes:
            for a in self.attributes:
                printout += str(a) + "\n"
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
        return "Success"

    def main(self):
        print
        print "Attributes::main"
        print "self: {}".format(self)

        lines = "@attribute make trek bridgestone cannondale nishiki garyfisher\n@attribute tires knobby treads\n@attribute bars straight curved\n@attribute bottles y n\n@attribute weight numeric\n@attribute type mountain hybrid"
        for line in lines.split("\n"):
            print "self.parse(line): {}".format(self.parse(line))

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


class AttributeFactory(object):
    def __init__(self):
        pass

    def __str__(self):
        return

    def __repr__(self):
        return self.__str__()

    def make(self, scanner):
        l = scanner.split(" ")
        # l[0] is the attribute tag, so we don't need it
        name = l[1]
        if l[2] == 'numeric':
            return NumericAttribute(name)
        a = NominalAttribute(name)
        for i in range(2, len(l)):
            a.addValue(l[i])
        return a

    def main(self):
        print
        print "AttributeFactory::main"
        data = "@attribute weight numeric"
        print "data: {}".format(data)
        print "self.make(data): {}".format(self.make(data))
        data = "@attribute type mountain hybrid"
        print "data: {}".format(data)
        print "self.make(data): {}".format(self.make(data))


class Example(list):
    def __init__(self, n):
        self.n = n

    def add(self, val):
        if not isinstance(val, float) and not isinstance(val, int):
            raise TypeError("Val must be an int or float. Got {}".format(type(val)))
        self.append(val)

    def main(self):
        print
        print "Example::main"
        try:
            print "self.add('chars'):".format(self.add('chars'))
        except Exception as e:
            print e.args[0]

        print "self.add(3.3):".format(self.add(3.3))
        print "self.add(5.0):".format(self.add(5.0))
        print "self: {}".format(self)


class Examples(list):
    def __init__(self, attributes):
        self.attributes = attributes.attributes

    def __str__(self):
        chart = "@examples\n"
        if self:
            for a in self.attributes:
                chart += a.name + "\t\t"
            chart += "\n"
            for e in self:
                for val in e:
                    chart += str(val) + "\t\t"
                chart += "\n"
        else:
            chart += "Empty"
        return chart

    def __repr__(self):
        return self.__str__()

    def add(self, val):
        if not isinstance(val, Example):
            raise TypeError("Val must be an Example. Got {}".format(type(val)))
        self.append(val)
        return val

    def parse(self, scanner):
        attr = scanner.split(" ")
        ex = Example(len(attr))
        for i, a in enumerate(attr):
            curAttr = self.attributes[i]
            if isinstance(curAttr, NominalAttribute):
                ex.add(curAttr.getIndex(a))
            elif isinstance(curAttr, NumericAttribute):
                ex.add(float(a))
        self.add(ex)
        return "Success"

    def main(self):
        print
        print "Examples::main"
        ex = "trek knobby straight y 250.3 mountain\nbridgestone treads straight y 200 hybrid\ncannondale knobby curved n 222.9 mountain\nnishiki treads curved y 190.3 hybrid\ntrek treads straight y 196.8 hybrid"
        for line in ex.split("\n"):
            self.parse(line)
        print "self: {}".format(self)


class DataSet(object):
    def __init__(self, attributes=Attributes()):  # error if the examples can not be added because of type or memory problems
        self.name = None
        self.attributes = attributes
        self.examples = Examples(attributes)
        self.seed = -1
        self.random = random.random()
        self.mode = 0

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
        elif options[1] == '-t':
            self.mode = 1
        elif options[1] == '-T':
            self.mode = 2
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


class TrainTestSets(object):
    def __init__(self, options=[]):  # error if the examples can not be added because of type or memory problems
        self.test = DataSet(Attributes())
        self.train = DataSet(Attributes())
        self.mode = 0  # 1 if testing, 2 if training
        self.setOptions(options)

    def __str__(self):
        return "Training Set:\n{}\n\nTest Set:\n{}".format(self.train, self.test)

    def __repr__(self):
        return self.__str__()

    def getTestingSet(self):
        return self.test

    def getTrainingSet(self):
        return self.train

    def setOptions(self, options):  # error if an option is illegal
        if len(options) == 1:
            pass
        elif options[1] == '-t':
            self.mode = 1
        elif options[1] == '-T':
            self.mode = 2
        else:
            raise ValueError("Illegal option: " + " ".join(options[1:]))

    def setTestingSet(self, test):
        self.test.addDataset(test)
        return "Success"

    def setTrainingSet(self, train):  # error java.lang.Exception
        self.train.addDataset(train)
        return "Success"

    def main(self):  # error if the examples can not be added because of type or memory problems
        print
        print "TrainTestSets::main"
        print "self: {}".format(self)
        print "self.mode: {}".format(self.mode)
        g = DataSet(Attributes())
        g.main()
        print "self.setTrainingSet(g): {}".format(self.setTrainingSet(g))
        print "self.setTestingSet(DataSet(Attributes())): {}".format(self.setTestingSet(DataSet(Attributes())))


def test():
    a = NominalAttribute("hello")
    a.main()
    b = NumericAttribute("num")
    b.main()
    c = Attributes()
    c.main()
    d = AttributeFactory()
    d.main()
    e = Example(5)
    e.main()
    f = Examples(c)
    f.main()
    g = DataSet(Attributes())
    g.main()
    h = TrainTestSets(sys.argv)
    h.main()


def main():
    try:
        print "main: testing"
        test()
    except Exception as e:
        print e.args[0]

if __name__ == "__main__":
    main()
