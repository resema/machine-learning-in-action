from numpy import *

def loadDataSet():
  postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
  classVec = [0,1,0,1,0,1]    #1 is abusive, 0 not
  return postingList, classVec
  
def createVocabList(dataSet):
  # create an empty set
  vocabSet = set([])
  for document in dataSet:
    # create the union of two sets
    vocabSet = vocabSet | set(document)
  return list(vocabSet)
  
def setOfWords2Vec(vocabList, inputSet):
  # create a vector of all 0s
  returnVec = [0] * len(vocabList)
  for word in inputSet:
    if word in vocabList:
      returnVec[vocabList.index(word)] = 1
    else:
      print "the word: %s is not in my Vocabulary!" % word
  return returnVec
  
def bagOfWords2VecMN(vocabList, inputSet):
  returnVec = [0] * len(vocabList)
  for word in inputSet:
    if word in vocabList:
      returnVec[vocabList.index(word)] += 1
  return returnVec
  
def trainNB0(trainMatrix, trainCategory):
  numTrainDocs = len(trainMatrix)
  numWords = len(trainMatrix[0])
  # inialize probabilities
  pAbusive = sum(trainCategory)/float(numTrainDocs)
  p0Num = ones(numWords)
  p1Num = ones(numWords)
  p0Denom = 2.0
  p1Denom = 2.0
  for i in range(numTrainDocs):
    # vector addition
    if trainCategory[i] == 1:
      p1Num += trainMatrix[i]
      p1Denom += sum(trainMatrix[i])
    else:
      p0Num += trainMatrix[i]
      p0Denom += sum(trainMatrix[i])
  # element-wise division
  p1Vect = log(p1Num/p1Denom)    #change to log()
  p0Vect = log(p0Num/p0Denom)    #change to log()
  return p0Vect, p1Vect, pAbusive

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
  # element-wise multiplication
  p1 = sum(vec2Classify * p1Vec) + log(pClass1)
  p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
  if p1 > p0:
    return 1
  else:
    return 0
    
def testingNB():
  listOPosts, listClasses = loadDataSet()
  myVocabList = createVocabList(listOPosts)
  trainMat = []
  for postinDoc in listOPosts:
    trainMat.append(bagOfWords2VecMN(myVocabList, postinDoc))
  p0V, p1V, pAb = trainNB0(array(trainMat), array(listClasses))
  testEntry = ['love', 'my', 'dalmation']
  thisDoc = array(bagOfWords2VecMN(myVocabList, testEntry))
  print testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb)
  testEntry = ['stupid', 'garbage']
  thisDoc = array(bagOfWords2VecMN(myVocabList, testEntry))
  print testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb)

def textParse(bigString):
  import re
  listOfTokens = re.split(r'\W*', bigString)
  return [tok.lower() for tok in listOfTokens if len(tok) > 2]
  
def spamTest():
  docList = []; classList = []; fullText = []
  for i in range(1,26):
    # load and parse text files
    wordList = textParse(open('email/spam/%d.txt' % i).read())
    docList.append(wordList)
    fullText.extend(wordList)
    classList.append(1)
    wordList = textParse(open('email/ham/%d.txt' % i).read())
    docList.append(wordList)
    fullText.extend(wordList)
    classList.append(0)
  vocabList = createVocabList(docList)
  trainingSet = range(50); testSet = []
  # randomly create the training set
  for i in range(10):
    randIndex = int(random.uniform(0, len(trainingSet)))
    testSet.append(traingingSet[randIndex])
    del(trainingSet[randIndex])
  trainMat = []; trainClasses = []
  for docIndex in trainingSet:
    trainMat.append(setOfWords2Vec(vocabList, docList[docIndex]))
    trainClasses.append(classList[docList])
  p0V, p1V, pSpam = trainNB0(array(trainMat), array(trainClasses))
  errorCount = 0
  # classify the test set
  for docIndex in testSet:
    wordVector = setOfWords2Vec(vocabList, docList[docIndex])
    if classifyNB(array(wordVector), p0V, p1V, pSpam) != classList[docIndex]:
      errorCount += 1
  print 'the error rate is: ', float(errorCount)/len(testSet)



  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
