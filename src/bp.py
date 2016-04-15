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
        self.i = -1
        self.j = 3
        self.k = -1
        self.w = []
        self.v = []
        self.n = 0.9
        self.e = 1.0
        self.emin = 0.1
        self.random = 0.3
        self.decimal = 3

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
        print self.examples
        print self.instances

    def train(self, ds):
        # initializing
        self.trainInit(ds)

        q = 1  # epochs
        while (self.e > self.emin):
            self.e = 0
            for z in ds.getExamples():
                self.trainExample(ds, z)
            q += 1
        print self.e

    def trainInit(self, ds):
        self.i = len(ds.attributes.attributes)
        self.k = len(ds.attributes.attributes[-1].getDomain())
        self.initWeights()

    def trainExample(self, ds, z):
        ##
        # step 2: compute
        ##

        y = []
        o = []
        d = []

        bias = -1
        d_holder = z[-1]
        z[-1] = bias  # setting class label to our bias

        # calculate y
        for j_n in range(self.j-1):
            y_n = 0
            for i_n in range(self.i):
                y_n += z[i_n] * self.v[i_n][j_n]
            y.append(self.sigmoid(y_n))
        y.append(bias)
        # print "y is:", y

        # calculate o
        for k_n in range(self.k):
            o_n = 0
            for j_n in range(self.j):
                o_n += y[j_n] * self.w[j_n][k_n]
            o.append(self.sigmoid(o_n))
        # print "o is:", o

        # linearly encode class attribute (d)
        for k_n in range(self.k):
            if k_n == d_holder:
                d.append(1)
                continue
            d.append(0)

        ##
        # step 3: calculate error
        ##

        for k_n in range(self.k):
            self.e += 0.5 * (d[k_n] - o[k_n]) ** 2
        # print "e is:", self.e

        ##
        # step 4: calculate error signal vectors
        ##

        sigO = []
        sigY = []

        for k_n in range(self.k):
            ok = o[k_n]
            dk = d[k_n]
            sigO.append(round((dk-ok)*(1-ok)*ok, self.decimal))

        # print "sigO is:", sigO

        for j_n in range(self.j):
            kSum = 0
            for k_n in range(self.k):
                kSum += sigO[k_n] * self.w[j_n][k_n]
            yj = y[j_n]
            sigY.append(round(yj*(1-yj)*kSum, self.decimal))

        # print "sigY is:", sigY

        ##
        # step 5: adjust output layer weights
        ##

        for j_n in range(self.j):
            for k_n in range(self.k):
                self.w[j_n][k_n] = round(self.w[j_n][k_n] + self.n * sigO[k_n] * y[j_n], self.decimal)
        # print "adjusted w:", self.w

        ##
        # step 6: adjust hidden layer weights
        ##

        for i_n in range(self.i):
            for j_n in range(self.j):
                self.v[i_n][j_n] = round(self.v[i_n][j_n] + self.n * sigY[j_n] * z[i_n], self.decimal)
        # print "adjusted v:", self.v

    def sigmoid(self, n):
        return round(1.0/(1 + math.e**(-n)), self.decimal)

    def initWeights(self):
        self.initV()
        self.initW()

    def initV(self):
        self.v = []
        for i_n in range(self.i):
            r = []
            for j_n in range(self.j):
                r.append(self.randomize())
            self.v.append(r)
        return self.v

    def initW(self):
        self.w = []
        for j_n in range(self.j):
            r = []
            for k_n in range(self.k):
                r.append(self.randomize())
            self.w.append(r)
        return self.w

    def randomize(self):
        return round(random.random()*self.random, self.decimal)


## initialize and evaluate
def main():
    # try:
        ds = TrainTestSets(sys.argv)
        if len(ds.getTrainingSet().getExamples()) > 0:
            if len(ds.getTestingSet().getExamples()) > 0:
                Evaluator(BP()).evaluate(ds.getTrainingSet(), ds.getTestingSet())
            else:
                Evaluator(BP()).evaluate(ds.getTrainingSet())
    # except Exception as e:
    #     if len(e.args) == 1:
    #         print e.args[0]
    #     else:
    #         print e.args[1]


if __name__ == "__main__":
    main()
