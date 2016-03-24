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


class ID3(Classifier):
    def __init__(self, e=DataSet(), i=DataSet(), root=Node(), p=.1):
        super(ID3, self).__init__(e, i)
        self.setOptions(sys.argv[1:])
        self.type = 'ID3'
        self.p = p

    def __str__(self):
        return super(ID3, self).__str__()

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
    def classify(self, inst, root):
        c = root
        while len(c.children) > 0:
            attr = c.getAttribute()
            i = self.examples.getAttributes().getIndex(attr)
            c = c.getChildren()[i]
        return c.getLabel()


## initialize and evaluate
def main():
    try:
        ds = TrainTestSets(sys.argv)
        if len(ds.getTrainingSet().getExamples()) > 0:
            if len(ds.getTestingSet().getExamples()) > 0:
                Evaluator(ID3()).evaluate(ds.getTrainingSet(), ds.getTestingSet())
            else:
                Evaluator(ID3()).evaluate(ds.getTrainingSet())
    except Exception as e:
        if len(e.args) == 1:
            print e.args[0]
        else:
            print e.args[1]


if __name__ == "__main__":
    main()
