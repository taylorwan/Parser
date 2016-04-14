#
# Taylor Wan
# tw476@georgetown.edu
# Platform: OS X
# Language/Environment: python
#
# In accordance with the class policies and Georgetown's Honor Code,
# I certify that, with the exceptions of the class resources and those
# items noted below, I have neither given nor received any assistance
# on this project.
#

from classifier import *
from traintestsets import *


class BP(Classifier):
    def __init__(self, e=DataSet(), i=DataSet()):
        super(BP, self).__init__(e, i)
        self.setOptions(sys.argv[1:])
        self.type = 'BP'

    def __str__(self):
        return super(BP, self).__str__()

    def __repr__(self):
        return self.__str__()

    ## parse through command line options
    def setOptions(self, opts):
        pass
        p = '-p'
        if p in opts:
            next = opts.index(p) + 1
            if next >= len(opts):
                loadOptionsError(opts, "Missing argument for -p")
            try:
                self.p = float(opts[next])
            except Exception as e:
                loadOptionsError(opts, "Invalid argument for -p")

    ## determine probability for a single example (test)
    def classify(self, inst):
        pass

    def train(self):
        pass


## initialize and evaluate
def main():
    try:
        ds = TrainTestSets(sys.argv)
        if len(ds.getTrainingSet().getExamples()) > 0:
            if len(ds.getTestingSet().getExamples()) > 0:
                Evaluator(BP()).evaluate(ds.getTrainingSet(), ds.getTestingSet())
            else:
                Evaluator(BP()).evaluate(ds.getTrainingSet())
    except Exception as e:
        if len(e.args) == 1:
            print e.args[0]
        else:
            print e.args[1]


if __name__ == "__main__":
    main()
