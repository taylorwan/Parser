class Example(list):
    def __init__(self, n):
        self.n = n

    def getN(self):
        return self.n

    ## add an example to our list
    def add(self, val):
        if not isinstance(val, float) and not isinstance(val, int):
            raise TypeError("Val must be an int or float. Got {}".format(type(val)))
        self.append(val)
