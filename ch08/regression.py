'''
Created on Jun 26 2017
Linear Regression example
@author: resema
'''
from numpy import *

def loadDataSet(fileName):
  numFeat = len(open(fileName).readline().split('\t')) - 1
  dataMat = []; labelMat = []
  fr = open(fileName)
  for line in fr.readlines():
    lineArr = []
    curLine = line.strip().split('\t')
    for i in range(numFeat):
      lineArr.append(float(curLine[i]))
    dataMat.append(lineArr)
    labelMat.append(float(curLine[-1]))
  return dataMat,labelMat
  
def standRegres(xArr, yArr):
  xMat = mat(xArr); yMat = mat(yArr).T
  xTx = xMat.T*xMat
  if linalg.det(xTx) == 0.0:
    print "This matrix is singular, cannot do inverse"
    return
  ws = xTx.I * (xMat.T*yMat)
  return ws
  
def lwlr(testPoint, xArr, yArr, k=1.0):
  xMat = mat(xArr); yMat = mat(yArr).T
  m = shape(xMat)[0]
  # 1: create diagonal matrix
  weights = mat(eye((m)))
  for j in range(m):
    # 2: populate weights with exponentially decaying values
    diffMat = testPoint - xMat[j,:]
    weights[j,j] = exp(diffMat*diffMat.T/(-2.0*k**2))
  xTx = xMat.T * (weights * xMat)
  if linalg.det(xTx) == 0.0:
    print "This matrix is singular, cannot do inverse"
    return
  ws = xTx.I * (xMat.T * (weights * yMat))
  return testPoint * ws
  
def lwlrTest(testArr,xArr,yArr,k=1.0):
  m = shape(testArr)[0]
  yHat = zeros(m)
  for i in range(m):
    yHat[i] = lwlr(testArr[i],xArr,yArr,k)
  return yHat
  
def rssError(yArr, yHatArr):
  return ((yArr-yHatArr)**2).sum()

'''
Shrinking methods: 
  No1 -> ridge regression (better but difficult to compute the lasso)
  No2 -> forward stagewise regression (easy way to approximate the lasso)
'''

# ridge regression

'''
ridgeRegres calculates weights
'''
def ridgeRegres(xMat, yMat, lam=0.2):
  xTx = xMat.T*xMat
  denom = xTx + eye(shape(xMat)[1])*lam
  if linalg.det(denom) == 0.0:
    print "This matrix is singular, cannot do inverse"
    return
  ws = denom.I * (xMat.T*yMat)
  return ws
  
'''
test this over a number of lambda values
'''
def ridgeTest(xArr, yArr):
  xMat = mat(xArr); yMat = mat(yArr).T
  yMean = mean(yMat, 0)
  yMat = yMat - yMean
  xMeans = mean(xArr, 0)
  xVar = var(xMat, 0)
  xMat = (xMat - xMeans)/xVar
  numTestPts = 30
  wMat = zeros((numTestPts, shape(xMat)[1]))
  for i in range(numTestPts):
    ws = ridgeRegres(xMat, yMat, exp(i-10))
    wMat[i,:] = ws.T
  return wMat







































