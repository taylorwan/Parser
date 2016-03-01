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
