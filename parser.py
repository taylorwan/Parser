import random


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
        return "{}".format(self.name)

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
        l = []
        for a in self.attributes:
            l.append(str(a))
        return "['{}']".format("', '".join(l))

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
        try:
            for i, a in enumerate(self.attributes):
                if a.name == name:
                    return i
        except:
            print "value not in list"

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
        return s

    def main(self):
        try:
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
        except:
            print "an error has occured"


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
        try:
            print
            print "AttributeFactory::main"
            data = "@attribute weight numeric"
            print "data: {}".format(data)
            print "self.make(data): {}".format(self.make(data))
            data = "@attribute type mountain hybrid"
            print "data: {}".format(data)
            print "self.make(data): {}".format(self.make(data))
        except:
            print "an error has occured"


class Example(list):
    def __init__(self, n):
        self.n = n

    def add(self, val):
        if not isinstance(val, float):
            raise TypeError("Val must be a float. Got {}".format(type(val)))
        self.append(val)

    def main(self):
        print
        print "Example::main"
        try:
            print "self.add('chars'):".format(self.add('chars'))
        except Exception as e:
            print e.args[0]
        try:
            print "self.add(3.3):".format(self.add(3.3))
            print "self.add(5.0):".format(self.add(5.0))
            print "self: {}".format(self)
        except:
            print "an error has occured"


class Examples(list):
    def __init__(self, attributes):
        self.attributes = attributes.attributes

    def __str__(self):
        attr = []
        for a in self.attributes:
            attr.append(str(a))
        ex = []
        for e in self:
            ex.append(str(e))
        return "Attributes: ['{}']\nExamples: ['{}']".format("', '".join(attr), "', '".join(ex))

    def __repr__(self):
        return self.__str__()

    def add(self, val):
        if not isinstance(val, Example):
            raise TypeError("Val must be an Example. Got {}".format(type(val)))
        self.append(val)

    def parse(self, scanner):
        attr = scanner.split(" ")
        ex = Example(len(attr))
        for i, a in enumerate(attr):
            curAttr = self.attributes[i]
            if isinstance(curAttr, NominalAttribute):
                ex.add(float(curAttr.getIndex(a)))
            elif isinstance(curAttr, NumericAttribute):
                ex.add(float(a))
        self.add(ex)

    def main(self):
        try:
            print
            print "Examples::main"
            ex = "trek knobby straight y 250.3 mountain\nbridgestone treads straight y 200 hybrid\ncannondale knobby curved n 222.9 mountain\nnishiki treads curved y 190.3 hybrid\ntrek treads straight y 196.8 hybrid"
            for line in ex.split("\n"):
                self.parse(line)
            print "self: {}".format(self)
        except:
            print "an error has occured"


class DataSet(object):
    def __init__(self, attributes=Attributes()):  # error if the examples can not be added because of type or memory problems
        self.name = None
        self.attributes = attributes
        self.examples = Examples(attributes)
        self.seed = -1
        self.random = random.random()
        self.options = None

    def __str__(self):
        return "{}".format(self.name)

    def __repr__(self):
        return self.__str__()

    def addDataset(self, dataset):  # error if the examples can not be added because of type or memory problems
        for example in dataset.getExamples():
            self.add(example)

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
            self.parse(f.read())

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

    def setOptions(self, options):  # error if an option is illegal
        self.options = options

    def setSeed(self, seed):
        self.seed = seed

    def main(self):
        try:
            print
            print "DataSet::main"
            print self.getAttributes()
            print self.getExamples()
            print "self.load(bikes.mff): {}".format(self.load("bikes.mff"))
            print self
            print self.getAttributes()
            print self.getExamples()
        except:
            print "an error has occured"


class TrainTestSets(object):
    def __init__(self, options=[]):  # error if the examples can not be added because of type or memory problems
        self.test = None
        self.train = None
        self.options = options

    def __str__(self):
        return "Training Set: {}\n Test Set: {}".format(self.train, self.test)

    def __repr__(self):
        return self.__str__()

    def getTestingSet(self):
        return self.test

    def getTrainingSet(self):
        return self.train

    def setOptions(self, options):  # error if an option is illegal
        self.options = options

    def setTestingSet(self, test):
        self.test.addDataset(test)

    def setTrainingSet(self, train):  # error java.lang.Exception
        self.train.addDataset(train)

    def main(self):  # error if the examples can not be added because of type or memory problems
        print
        print "TrainTestSets::main"


def main():
    print "main: testing"
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
    # h = TrainTestSets()
    # h.main()

if __name__ == "__main__":
    main()
