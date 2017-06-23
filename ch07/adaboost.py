'''
Created on Jun 22 2017
AdaBoost example
@author: resema
'''
from numpy import *

def loadSimpData():
  datMat = matrix([[1., 2.1],
                   [2., 1.1],
                   [1.3, 1.],
                   [1., 1.],
                   [2., 1.]])
  classLabels = [1.0, 1.0, -1.0, -1.0, 1.0]
  return datMat, classLabels
  
def loadDataSet(fileName):
  numFeat = len(open(fileName).readline().split('\t'))
  dataMat = []; labelMat = []
  fr = open(fileName)
  for line in fr.readlines():
    lineArr = []
    curLine = line.strip().split('\t')
    for i in range(numFeat-1):
      lineArr.append(float(curLine[i]))
    dataMat.append(lineArr)
    labelMat.append(float(curLine[-1]))
  return dataMat, labelMat
  
def stumpClassify(dataMatrix, dimen, threshVal, thresIneq):
  retArray = ones((shape(dataMatrix)[0],1))
  if thresIneq == 'lt':
    retArray[dataMatrix[:,dimen] <= threshVal] = -1.0
  else:
    retArray[dataMatrix[:,dimen] > threshVal] = 1.0   #was -1.0 initially
  return retArray
  
def buildStump(dataArr, classLabels, D):
  dataMatrix = mat(dataArr); labelMat = mat(classLabels).T
  m,n = shape(dataMatrix)
  numSteps = 10.0; bestStump = {}; bestClasEst = mat(zeros((m,1)))
  minError = inf
  # loop over all features in our dataset
  for i in range(n):
    rangeMin = dataMatrix[:,i].min(); rangeMax = dataMatrix[:,i].max()
    stepSize = (rangeMax-rangeMin)/numSteps
    # loop over all steps
    for j in range(-1, int(numSteps)+1):
      # loop toogles between greater than and less than
      for inequal in ['lt', 'gt']:
        threshVal = (rangeMin + float(j) * stepSize)
        predictedVals = stumpClassify(dataMatrix, i, threshVal, inequal)
        errArr = mat(ones((m,1)))
        errArr[predictedVals == labelMat] = 0
        # 1: calculated weigthed error (D := weight vector)
        weightedError = D.T*errArr
        # print "split: dim % d, thresh %.2f, thresh inequal: %s, the weigthed error is %.3f" % \
               # (i, threshVal, inequal, weightedError)
        if weightedError < minError:
          minErrror = weightedError
          minError = weightedError
          bestClasEst = predictedVals.copy()
          bestStump['dim'] = i
          bestStump['thresh'] = threshVal
          bestStump['ineq'] = inequal
  return bestStump, minError, bestClasEst
  
# DS := decision stump
def adaBoostTrainDS(dataArr, classLabels, numIt=40):
  weakClassArr = []
  m = shape(dataArr)[0]
  # D holds the weight of each piece of data == probability distribution (sum of all elem == 1)
  # AdaBoost will increase the weight of the misclassified and decrease those of the properly classified data
  D = mat(ones((m,1))/m)
  # aggregte estimate of the clas for every data  
  aggClassEst = mat(zeros((m,1)))
  for i in range(numIt):
    bestStump, error, classEst = buildStump(dataArr, classLabels, D)
    print "D: ", D.T
    alpha = float(0.5*log((1.0-error)/max(error, 1e-16)))
    bestStump['alpha'] = alpha
    weakClassArr.append(bestStump)
    print "classEst: ", classEst.T
    # 1: calculate D for next iteration
    expon = multiply(-1*alpha*mat(classLabels).T,classEst)
    D = multiply(D, exp(expon))
    D = D/D.sum()
    # 2: aggregate error calculation
    aggClassEst += alpha*classEst
    print "aggClassEst: ", aggClassEst.T
    aggErrors = multiply(sign(aggClassEst) != mat(classLabels).T, ones((m,1)))
    errorRate = aggErrors.sum()/m
    print "total error: ", errorRate, "\n"
    if errorRate == 0.0:
      break
  return weakClassArr
 
def adaClassify(datToClass, classifierArr):
  dataMatrix = mat(datToClass)
  m = shape(dataMatrix)[0]
  aggClassEst = mat(zeros((m,1)))
  for i in range(len(classifierArr)):
    classEst = stumpClassify(dataMatrix, classifierArr[i]['dim'], \
                                         classifierArr[i]['thresh'], \
                                         classifierArr[i]['ineq'])
    aggClassEst += classifierArr[i]['alpha']*classEst
    print aggClassEst
  return sign(aggClassEst)
    








































