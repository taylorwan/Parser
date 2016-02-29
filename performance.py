class Performance(object):

    def __init__(self, accuracy=-1, std=-1):
        self.accuracy = accuracy
        # self.std = std

    def __str__(self):
        return self.getAccuracy()
        # return "Accuracy: {:.{prec}f} +- {:.{prec}f}" \
            # .format(self.accuracy, self.std, prec=2)

    def __repr__(self):
        return self.__str__()

    def getAccuracy(self):
        return self.accuracy

    def getSTD(self):
        return self.std

    def setAccuracy(self, a):
        self.accuracy = a

    def setSTD(self, s):
        self.std = s
