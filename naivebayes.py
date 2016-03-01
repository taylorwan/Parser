from classifier import *
from traintestsets import *


class NaiveBayes(Classifier):
    def __init__(self, e=DataSet(), i=DataSet()):
        super(NaiveBayes, self).__init__(e, i)
        self.type = 'Naive Bayes'

    def __str__(self):
        return super(NaiveBayes, self).__str__()

    def __repr__(self):
        return self.__str__()

    ## determine probability for a single example (test)
    def classify(self, inst):

        # initialize helpers:
        # - attributes for the current data set
        # - domain of the class index of the current data set
        # - data structure to track tallies
        attrs = self.examples.getAttributes().getAttributes()
        domain = self.examples.getAttributes().getClassAttribute().getDomain()
        counts = []

        # iterate through observations
        for i, a in enumerate(attrs):
            # class index
            if i == len(attrs)-1:
                counts.append(self.countClass(domain))
            # nominal values
            elif isinstance(a, NominalAttribute):
                counts.append(self.countNominal(inst, i, domain))
            # ignore numeric values

        # calculate and return the index with the highest probability
        p = self.calcP(counts, domain)
        return self.calcVote(p)

    ## calculate probabilities based on tallied data
    def calcP(self, counts, d):

        # initial values for probability
        p = [1 for x in range(len(d))]

        # multiply each value by its corresponding probability
        for i, c in enumerate(counts):
            s = sum(c.values())
            for k in c:
                p[k] *= c[k]/float(s)

        # return normalized values
        return map(lambda x: x/float(sum(p)), p)

    ## find the index of the value with the highest probability
    def calcVote(self, p):
        return p.index(max(p))

    ## tally votes for one nominal attribute
    def countNominal(self, inst, i, d):

        # initialize values with add-one smoothing
        vals = {}
        for val in range(len(d)):
            vals[val] = 1

        # count values that match the current example's value
        for ex in self.examples.getExamples():
            if inst[i] == ex[i]:
                vals[ex[-1]] += 1
        return vals

    ## tally values for the class index
    def countClass(self, d):
        vals = {}
        for val in range(len(d)):
            vals[val] = 0
        for ex in self.examples.getExamples():
            vals[ex[-1]] += 1
        return vals


## initialize and evaluate
def main():
    try:
        ds = TrainTestSets(sys.argv)
        if len(ds.getTrainingSet().getExamples()) > 0:
            if len(ds.getTestingSet().getExamples()) > 0:
                Evaluator(NaiveBayes()).evaluate(ds.getTrainingSet(), ds.getTestingSet())
            else:
                Evaluator(NaiveBayes()).evaluate(ds.getTrainingSet())
    except Exception as e:
        if len(e.args) == 1:
            print e.args[0]
        else:
            print e.args[1]


if __name__ == "__main__":
    main()
