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
        # for s in scanner:
        #     print s
        #     self.add(s)
        # self.setClassIndex(self.getSize()-1)
        m = AttributeFactory()
        s = m.make(scanner)
        print s
        self.attributes.append(s)
        self.setClassIndex(self.getSize()-1)

    def main(self):
        print
        print "Attributes::main"
        lines = "@attribute make trek bridgestone cannondale nishiki garyfisher\n@attribute tires knobby treads\n@attribute bars straight curved\n@attribute bottles y n\n@attribute weight numeric\n@attribute type mountain hybrid"
        for line in lines.split("\n"):
            self.parse(line)
        print "self: {}".format(self)
        # b = NominalAttribute("hello")
        # b.addValue("greeting")
        # l = [b]
        # print "l: {}".format(l)
        # print "self.parse(l): {}".format(self.parse(l))
        # print "self: {}".format(self)
        # print "self.getSize(): {}".format(self.getSize())
        # print "self.get(0): {}".format(self.get(0))
        # print "self.getHasNominalAttributes(): {}".format(self.getHasNominalAttributes())
        # print "self.getHasNumericAttributes(): {}".format(self.getHasNumericAttributes())
        # print "self.getIndex(\"hey\"): {}".format(self.getIndex("hey"))
        # print "self.getClassIndex(): {}".format(self.getClassIndex())
        # print "self.get(getClassIndex()): {}".format(self.get(self.getClassIndex()))
        # print "self.getClassAttribute(): {}".format(self.getClassAttribute())
        # print "self.setClassIndex(0): {}".format(self.setClassIndex(0))
        # print "self.add(NumericAttribute(\"num\")): {}".format(self.add(NumericAttribute("num")))
        # print "self: {}".format(self)
        # print "self.getIndex(\"num\")): {}".format(self.getIndex("num"))
        # print "self.getHasNumericAttributes(): {}".format(self.getHasNumericAttributes())


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
        print "self.add(3.3):".format(self.add(3.3))
        print "self.add(5.0):".format(self.add(5.0))
        print "self: {}".format(self)


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
        lines = scanner.split("\n")
        for line in lines:
            attr = line.split(" ")
            ex = Example(len(line))
            for i, a in enumerate(attr):
                curAttr = self.attributes[i]
                if isinstance(curAttr, NominalAttribute):
                    ex.add(float(curAttr.getIndex(a)))
                elif isinstance(curAttr, NumericAttribute):
                    ex.add(float(a))
            self.add(ex)

    def main(self):
        print
        print "Examples::main"
        ex = "trek knobby straight y 250.3 mountain\nbridgestone treads straight y 200 hybrid\ncannondale knobby curved n 222.9 mountain\nnishiki treads curved y 190.3 hybrid\ntrek treads straight y 196.8 hybrid"
        # print ex
        self.parse(ex)
        print "self: {}".format(self)


def main():
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

if __name__ == "__main__":
    main()
