from os import listdir
from numpy import *
import operator

def createDataSet():
  group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
  labels = ['A','A','B','B']
  return group, labels
  
  
def classify0(inX, dataSet, labels, k):
  dataSetSize = dataSet.shape[0]
  # distance calculation
  diffMat = tile(inX, (dataSetSize,1)) - dataSet
  sqDiffMat = diffMat**2
  sqDistances = sqDiffMat.sum(axis=1)
  distances = sqDistances**0.5  
  sortedDistIndices = distances.argsort()
  classCount = {}
  # voting with lowest k distances
  for i in range(k):
    voteIlabel = labels[sortedDistIndices[i]]
    classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
  # sort dictionary
  sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True) 
  return sortedClassCount[0][0]
 
def file2matrix(filename):
  fr = open(filename)
  # get number of lines in files
  numberOfLines = len(fr.readlines())
  # create NumPy matrix to return
  returnMat = zeros((numberOfLines, 3))
  classLabelVector = []
  fr = open(filename)
  index = 0
  # parse line to a list
  for line in fr.readlines():
    line = line.strip()
    listFromLine = line.split('\t')
    returnMat[index, :] = listFromLine[0:3]
    classLabelVector.append(int(listFromLine[-1]))
    index += 1
  return returnMat, classLabelVector
  
def autoNorm(dataSet):
  minVals = dataSet.min(0)
  maxVals = dataSet.max(0)
  ranges = maxVals - minVals
  normDataSet = zeros(shape(dataSet))
  m = dataSet.shape[0]
  normDataSet = dataSet - tile(minVals, (m,1))
  normDataSet = normDataSet/tile(ranges, (m,1))
  return normDataSet, ranges, minVals
  
def datingClassTest(hr, k):
  hoRatio = hr
  datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
  normMat, ranges, minVals = autoNorm(datingDataMat)
  m = normMat.shape[0]
  numTestVecs = int(m*hoRatio)
  errorCount = 0.0
  for i in range(numTestVecs):
    classifierResult = classify0(normMat[i,:], normMat[numTestVecs:m, :], datingLabels[numTestVecs:m], k)
    print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, datingLabels[i])
    if (classifierResult != datingLabels[i]):
      errorCount += 1.0
  print "the total error rate is: %f" % (errorCount / float(numTestVecs))
  
def classifyPerson():
  resultList = ['not at all', 'in small doses', 'in large doses']
  percentTats = float(raw_input("percentage of time spent playing video games? "))
  ffMiles = float(raw_input("frequent flier miles earned per year? "))
  iceCream = float(raw_input("liters of ice cream consumed per year? "))
  
  datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
  normMat, ranges, minVals = autoNorm(datingDataMat)
  inArr = array([ffMiles, percentTats, iceCream])
  classifierResult = classify0((inArr-minVals)/ranges, normMat, datingLabels, 3)
  print "You will probably like this person:", resultList[classifierResult-1]
  
def img2vector(filename):
  returnVect = zeros((1, 1024))
  fr = open(filename)
  for i in range(32):
    lineStr = fr.readline()
    for j in range(32):
      returnVect[0,32*i+j] = int(lineStr[j])
  return returnVect
  
def handwritingClassTest():
  hwLabels = []
  # get contents of directory
  trainingFileList = listdir('trainingDigits')
  m = len(trainingFileList)
  trainingMat = zeros((m, 1024))
  for i in range(m):
    # process class num from filename
    fileNameStr = trainingFileList[i]
    fileStr = fileNameStr.split('.')[0]
    classNumStr = int(fileStr.split('_')[0])
    hwLabels.append(classNumStr)
    trainingMat[i,:] = img2vector('trainingDigits/%s' % fileNameStr)
  # get contents of directory
  testFileList = listdir('testDigits')
  errorCount = 0.0
  mTest = len(testFileList)
  for i in range(mTest):
    fileNameStr = testFileList[i]
    fileStr = fileNameStr.split('.')[0]
    classNumStr = int(fileStr.split('_')[0])
    vectorUnderTest = img2vector('testDigits/%s' % fileNameStr)
    classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
    print "%s: the classifier came back with: %d, the real answer is: %d" % (fileStr, classifierResult, classNumStr)
    if (classifierResult != classNumStr): 
      errorCount += 1.0
  print "\nthe total number of errors is: %d" % errorCount
  print "\nthe total error rate is: %f" % (errorCount / float(mTest))
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  