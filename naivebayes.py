from classifier import *


class NaiveBayes(Classifier):
    def __init__(self, e=DataSet(), i=DataSet()):
        super(NaiveBayes, self).__init__(e, i)
        self.name = 'Naive Bayes'

    def __str__(self):
        return super(NaiveBayes, self).__str__()

    def __repr__(self):
        return self.__str__()

    def classify(self, inst):
        attrs = self.examples.getAttributes().getAttributes()
        domain = self.examples.getAttributes().getClassAttribute().getDomain()
        counts = []
        for i, a in enumerate(attrs):
            if i == len(attrs)-1:
                counts.append(self.countClass(domain))
            elif isinstance(a, NominalAttribute):
                counts.append(self.countNominal(inst, i, domain))
            # else:
            #     print "numeric, skipping for now"
        p = self.calcP(counts, domain)
        return self.calcVote(p)

    def calcP(self, counts, d):
        p = [1 for x in range(len(d))]
        for i, c in enumerate(counts):

            # fix for zero-frequency
            if 0 in c.values():
                c = self.incrementVals(c)

            # multiply each value by its corresponding probability
            s = sum(c.values())
            for k in c:
                p[k] *= c[k]/float(s)

        # return normalized values
        return map(lambda x: x/float(sum(p)), p)

    def incrementVals(self, d):
        for k in d:
            d[k] += 1
        return d

    def calcVote(self, p):
        return p.index(max(p))

    def countNominal(self, inst, i, d):
        vals = {}
        for val in range(len(d)):
            vals[val] = 0
        for ex in self.examples.getExamples():
            if inst[i] == ex[i]:
                vals[ex[-1]] += 1
        return vals

    def countClass(self, d):
        vals = {}
        for val in range(len(d)):
            vals[val] = 0
        for ex in self.examples.getExamples():
            vals[ex[-1]] += 1
        return vals
