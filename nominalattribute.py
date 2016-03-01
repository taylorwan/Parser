from attribute import *


class NominalAttribute(Attribute):

    def __init__(self, name=None):
        super(NominalAttribute, self).__init__(name)
        self.domain = []

    def __str__(self):
        return "{} {}".format(self.name, " ".join(self.domain))

    def __repr__(self):
        return self.__str__()

    def getIndex(self, value):  # error if the value is illegal
        return self.domain.index(value)

    def getValue(self, index):  # error if the index is out of bounds
        return self.domain[index]

    def getDomain(self):  # error if the index is out of bounds
        return self.domain

    # add a value to this attribute's domain
    def addValue(self, value):  # error if the value can not be added
        self.domain.append(value)
        self.size += 1
