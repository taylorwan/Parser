# [Parser](https://github.com/taylorwan/Parser)
Read, parse, store, and output examples in Mark's File Format (mff).

Project for COSC 288: Introduction to Machine Learning

## Running k-NN

```python
./kNN [-t <path> [-T <path>]] [-x folds] [-k neighbors]
```

## Running Naive Bayes

```python
./NaiveBayes [-t <path> [-T <path>]] [-x folds]
```

### Options

`-t` is an option in TrainTestSets

* Requires one argument: <path>, which specifies the path to a training file

`-T` is an option in TrainTestSets

* Requires one argument: <path>, which specifies the path to a test file

`-x` is an option in Evaluator

* Requires one argument: folds, which specifies the # of folds to partition the training set when evaluating performance

`-k` is an option in kNN

* Requires one argument: k, which specifies the # of closest neighbors to be used in making predictions

`-s` is an option in DataSet

* Generates a new seed

### Testing

You can use `test/votes.mff` and `test/mushroom.mff` as test data

