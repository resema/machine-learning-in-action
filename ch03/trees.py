import operator
from math import log

def calcShannonEnt(dataSet):
  numEntries = len(dataSet)
  labelCounts = {}
  # Create dictionary of all possible classes
  for featVec in dataSet:
    currentLabel = featVec[-1]
    if currentLabel not in labelCounts.keys():
      labelCounts[currentLabel] = 0
    labelCounts[currentLabel] += 1
  shannonEnt = 0.0
  for key in labelCounts:
    prob = float(labelCounts[key])/numEntries
    # logarithm base 2
    shannonEnt -= prob * log(prob, 2)
  return shannonEnt

def createDataSet():
  dataSet = [[1,1,'yes'],
             [1,1,'yes'],
             [1,0,'no'],
             [0,1,'no'],
             [0,1,'no']]
  labels = ['no surfacing', 'flippers']
  return dataSet, labels
  
def splitDataSet(dataSet, axis, value):
  # create separate list
  retDataSet = []
  for featVec in dataSet:
    if featVec[axis] == value:
      # cut out the feature split on
      reducedFeatVec = featVec[:axis]
      reducedFeatVec.extend(featVec[axis+1:])
      retDataSet.append(reducedFeatVec)
  return retDataSet
  
def chooseBestFeatureToSplit(dataSet):
  numFeatures = len(dataSet[0]) - 1
  baseEntropy = calcShannonEnt(dataSet)
  bestInfoGain = 0.0; bestFeature = -1
  for i in range(numFeatures):
    # create unique list of class labels
    featList = [example[i] for example in dataSet]
    uniqueVals = set(featList)
    newEntropy = 0.0
    # calculate entropy for each split
    for value in uniqueVals:
      subDataSet = splitDataSet(dataSet, i, value)
      prob = len(subDataSet)/float(len(dataSet))
      newEntropy += prob * calcShannonEnt(subDataSet)
    infoGain = baseEntropy - newEntropy
    if (infoGain > bestInfoGain):
      # find the best information gain
      bestInfoGain = infoGain
      bestFeature = i
  return bestFeature
  
def majorityCnt(classList):
  classCount = {}
  for vote in classList:
    if vot not in classCount.keys():
      classCount[vote] = 0
    classCount[vote] += 1
  sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
  return sortedClassCount
  
def createTree(dataSet, labels):
  # create a list of all the class labels in dataset 
  classList = [example[-1] for example in dataSet]
  # stop when all classes are equal
  if classList.count(classList[0]) == len(classList):
    return classList[0]
  # when no more features, return majority
  if len(dataSet[0]) == 1:
    return majorityCnt(classList)
  bestFeat = chooseBestFeatureToSplit(dataSet)
  bestFeatLabel = labels[bestFeat]
  myTree = {bestFeatLabel:{}}
  # get list of unique values
  del(labels[bestFeat])
  featValues = [example[bestFeat] for example in dataSet]
  uniqueVals = set(featValues)
  for value in uniqueVals:
    subLabels = labels[:]     # makes a copy of labels and places it in a newlist
    myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
  return myTree
  
def classify(inputTree, featLabels, testVec):
  firstStr = inputTree.keys()[0]
  secondDict = inputTree[firstStr]
  featIndex = featLabels.index(firstStr)
  for key in secondDict.keys():
    if testVec[featIndex] == key:
      if type(secondDict[key]).__name__ == 'dict':
        classLabel = classify(secondDict[key], featLabels, testVec)
      else:
        classLabel = secondDict[key]
  return classLabel
  
def storeTree(inputTree, filename):
  import pickle
  fw = open(filename, 'w')
  pickle.dump(inputTree, fw)
  fw.close()
  
def grabTree(filename):
  import pickle
  fr = open(filename)
  return pickle.load(fr)
  

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  