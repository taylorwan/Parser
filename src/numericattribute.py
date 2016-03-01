from attribute import *


class NumericAttribute(Attribute):

    def __init__(self, name=None):
        super(NumericAttribute, self).__init__(name)

    def __str__(self):
        return "{} numeric".format(self.name)

    def __repr__(self):
        return self.__str__()
