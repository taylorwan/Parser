class Example(list):
    def __init__(self, n):
        self.n = n

    ## add an example to our list
    def add(self, val):
        if not isinstance(val, float) and not isinstance(val, int):
            raise TypeError("Val must be an int or float. Got {}".format(type(val)))
        self.append(val)

    def main(self):
        print
        print "Example::main"
        try:
            print "self.add('chars'):".format(self.add('chars'))
        except Exception as e:
            print e.args[0]

        print "self.add(3.3):".format(self.add(3.3))
        print "self.add(5.0):".format(self.add(5.0))
        print "self: {}".format(self)
