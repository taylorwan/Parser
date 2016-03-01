class Performance(object):

    def __init__(self, accuracy=-1, std=-1):
        self.accuracy = accuracy

    def __str__(self):
        return self.getAccuracy()

    def __repr__(self):
        return self.__str__()

    def getAccuracy(self):
        return self.accuracy

    def setAccuracy(self, a):
        self.accuracy = a
