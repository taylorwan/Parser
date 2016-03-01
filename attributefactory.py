from nominalattribute import *
from numericattribute import *


class AttributeFactory(object):
    def __init__(self):
        pass

    def __str__(self):
        return

    def __repr__(self):
        return self.__str__()

    ## parse an attribute descriptor, and create the
    ## object accordingly
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
