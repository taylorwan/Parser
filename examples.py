from nominalattribute import *
from numericattribute import *
from example import *


class Examples(list):
    def __init__(self, attributes):
        self.attributes = attributes.attributes

    def __str__(self):
        chart = "@examples\n\n"
        if self:
            for e in self:
                for i, val in enumerate(e):
                    if isinstance(val, float):
                        chart += str(val) + " "
                    else:
                        chart += self.attributes[i].getValue(val) + " "
                chart = chart[:-1]  # remove trailing space (fence-post)
                chart += "\n"
        else:
            chart += "Empty"
        return chart

    def __repr__(self):
        return self.__str__()

    def getAttributes(self):
        return self.attributes

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
