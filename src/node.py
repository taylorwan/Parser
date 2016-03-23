class Node(object):

    def __init__(self, children=[], label=-1, attribute=-1):
        self.children = children
        self.label = label
        self.attribute = attribute

    def __str__(self):
        return "{}: {}".format(self.attribute, self.label)

    def __repr__(self):
        return self.__str__()

    def getChildren(self):
        return self.children if self.children > -1 else "No children set"

    def getLabel(self):
        return self.label if self.label > -1 else "No label set"

    def getAttribute(self):
        return self.attribute if self.attribute > -1 else "No attribute set"

    def setChildren(self, c):
        self.children = c

    def setLabel(self, l):
        self.label = l

    def setAttribute(self, a):
        self.attribute = a
