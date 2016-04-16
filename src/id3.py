from classifier import *
from traintestsets import *


class ID3(Classifier):
    def __init__(self, e=DataSet(), i=DataSet(), root=Node(), p=.1):
        super(ID3, self).__init__(e, i)
        self.type = 'ID3'

    def __str__(self):
        return super(ID3, self).__str__()

    def __repr__(self):
        return self.__str__()

    ## classify our set, and return the performance
    def classifySet(self, ds):
        root = ds.train()
        perf = 0
        for inst in self.instances.getExamples():
            self.vote = self.classify(inst, root)
            if self.vote == inst[-1]:
                perf += 1
        avgPerf = perf * 100.0 / len(self.instances.getExamples())
        return Performance(avgPerf)

    ## predict outcome of a single example (test)
    def classify(self, inst, root):
        c = root
        while len(c.children) > 0:
            attr = c.getAttribute()
            i = self.examples.getAttributes().getIndex(attr)
            c = c.getChildren()[i]
        return c.getLabel()
