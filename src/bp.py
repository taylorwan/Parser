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
        self.result = None

        self.i = -1
        self.j = 3  # 2 hidden nodes + bias node
        self.k = -1

        self.w = []
        self.v = []

        self.bias = -1
        self.e = 1.0
        self.n = 0.9
        self.emin = 0.1
        self.random = 0.3
        self.maxQ = 3000
        self.threshhold = 0.5

    def __str__(self):
        output = super(BP, self).__str__()
        if self.result is not None:
            output += ": " + self.result
        return output

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
            except Exception:
                loadOptionsError(opts, "Invalid argument for -p")

    ##
    ## Classify
    ##

    ## predict outcome of a single example (test)
    def classify(self, inst):
        y = self.calcY(inst)
        o = self.calcO(y)
        return self.interpretO(o)

    ##
    ## Train
    ##

    ## train our classifier with example set ds
    def train(self, ds=None):

        # initializing
        self.trainInit()
        q = 1  # epochs

        # keep running until E > Emin
        while (self.e > self.emin):
            self.e = 0

            # run on each example
            for ex in self.examples.getExamples():

                # make a deep copy of our example
                z = Example(ex.getN())
                for val in ex:
                    z.add(val)

                # train
                self.trainExample(z)

            # quit if we've run too many epochs
            if q > self.maxQ:
                raise RuntimeError("Failed to converge after {} epochs, with an error of {:.3f}".format(q, self.e))

            # increment
            q += 1

        self.result = "Set converted after {} epochs, with an error of {:.3f}".format(q, self.e)

    # initialize values (step #1)
    def trainInit(self):
        self.i = len(self.examples.attributes.attributes)
        self.k = len(self.examples.attributes.attributes[-1].getDomain())
        self.initWeights()

    # run a single epoch (steps #2-6)
    def trainExample(self, z):
        # swap out class label and replace it with our bias
        classAttr = z[-1]
        z[-1] = self.bias

        # step 2: compute
        y = self.calcY(z)  # calculate y
        o = self.calcO(y)  # calculate o
        d = self.encodeD(classAttr)  # linearly encode class attribute (d)

        # step 3: calculate error
        self.calcE(d, o)

        # step 4: calculate error signal vectors
        sigO = self.calcSigO(o, d)
        sigY = self.calcSigY(sigO, y)

        # step 5: adjust output layer weights
        self.adjW(sigO, y)

        # step 6: adjust hidden layer weights
        self.adjV(sigY, z)

    ##
    ## Helper Functions
    ##

    def randomize(self):
        # return 0.1
        return random.random()*self.random

    def sigmoid(self, n):
        return 1.0/(1 + math.e**(-n))

    # step 1
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

    # step 2
    def calcY(self, z):
        y = []
        for j_n in range(self.j-1):
            y_n = 0
            for i_n in range(self.i):
                y_n += z[i_n] * self.v[i_n][j_n]
            y.append(self.sigmoid(y_n))
        y.append(self.bias)
        return y

    def calcO(self, y):
        o = []
        for k_n in range(self.k):
            o_n = 0
            for j_n in range(self.j):
                o_n += y[j_n] * self.w[j_n][k_n]
            o.append(self.sigmoid(o_n))
        return o

    def encodeD(self, classAttr):
        d = []
        for k_n in range(self.k):
            if k_n == classAttr:
                d.append(1)
            else:
                d.append(0)
        return d

    # step 3
    def calcE(self, d, o):
        for k_n in range(self.k):
            self.e += 0.5 * (d[k_n] - o[k_n]) ** 2

    # step 4
    def calcSigO(self, o, d):
        sigO = []
        for k_n in range(self.k):
            ok = o[k_n]
            dk = d[k_n]
            sigO.append((dk-ok)*(1-ok)*ok)
        return sigO

    def calcSigY(self, sigO, y):
        sigY = []
        for j_n in range(self.j):
            kSum = 0
            for k_n in range(self.k):
                kSum += sigO[k_n] * self.w[j_n][k_n]
            yj = y[j_n]
            sigY.append(yj*(1-yj)*kSum)
        return sigY

    # step 5
    def adjW(self, sigO, y):
        for j_n in range(self.j):
            for k_n in range(self.k):
                self.w[j_n][k_n] += self.n * sigO[k_n] * y[j_n]

    # step 6
    def adjV(self, sigY, z):
        for i_n in range(self.i):
            for j_n in range(self.j):
                self.v[i_n][j_n] += self.n * sigY[j_n] * z[i_n]

    def interpretO(self, o):
        maxV = 0
        maxVInd = -1
        for i, v in enumerate(o):
            if v > maxV:
                maxV = v
                maxVInd = i
        return maxVInd


##
## Main
##

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
