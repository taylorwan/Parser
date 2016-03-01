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

    ## add a single example to our list
    def add(self, val):
        if not isinstance(val, Example):
            raise TypeError("Val must be an Example. Got {}".format(type(val)))
        self.append(val)
        return val

    ## parse through examples and add them to our list
    def parse(self, scanner):
        attr = scanner.split(" ")
        ex = Example(len(attr))

        # for each attribute, add the value from our example
        for i, a in enumerate(attr):
            curAttr = self.attributes[i]

            # if the attribute is nominal, add the index
            if isinstance(curAttr, NominalAttribute):
                ex.add(curAttr.getIndex(a))

            # if the attribute is numeric, add the value
            elif isinstance(curAttr, NumericAttribute):
                ex.add(float(a))

        # adding to list
        self.add(ex)
