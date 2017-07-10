'''
Created on Jul 06 2017
CART - Classification And Regression Trees

  Characteristics:  well-known and well-documented tree-building algoritm that
                    that makes binary splits and handles continous variables

@author: resema
'''

from numpy import *

def loadDataSet(fileName):
  dataMat = []
  fr = open(fileName)
  for line in fr.readlines():
    curLine = line.strip().split('\t')
    # 1: Map everything to float()
    fltLine = map(float, curLine)
    dataMat.append(fltLine)
  return dataMat
  
def binSplitDataSet(dataSet, feature, value):
  mat0 = dataSet[nonzero(dataSet[:,feature] > value)[0],:][0]
  mat1 = dataSet[nonzero(dataSet[:,feature] <= value)[0],:][0]
  return mat0, mat1
  
def regLeaf(dataSet):#returns the value used for each leaf
    return mean(dataSet[:,-1])

def regErr(dataSet):
    return var(dataSet[:,-1]) * shape(dataSet)[0]
    
'''
finds the best place to split the dataset
'''
def chooseBestSplit(dataSet, leafType=regLeaf, errType=regErr, ops=(1,4)):
  tolS = ops[0]; tolN = ops[1]
  # 1: exit if all values are equal
  if len(set(dataSet[:,-1].T.tolist()[0])) == 1:
    return None, leafType(dataSet)
  m,n = shape(dataSet)
  S = errType(dataSet)
  bestS = inf; bestIndex = 0; bestValue = 0
  for featIndex in range(n-1):
    for splitVal in set(dataSet[:,featIndex]):
      mat0, mat1 = binSplitDataSet(dataSet, featIndex, splitVal)
      if (shape(mat0)[0] < tolN) or (shape(mat1)[0] < tolN):
        continue
      newS = errType(mat0) + errType(mat1)
      if newS < bestS:
        bestIndex = featIndex
        bestValue = splitVal
        bestS = newS
  # 2: exit if low error reduction
  if (S - bestS) < tolS:
    return None, leafType(dataSet)
  mat0, mat1 = binSplitDataSet(dataSet, bestIndex, bestValue)
  # 3: exit if split creates small dataset
  if (shape(mat0)[0] < tolN) or (shape(mat1)[0] < tolN):
    return None, leafType(dataSet)
  return bestIndex, bestValue
  
def createTree(dataSet, leafType=regLeaf, errType=regErr, ops=(1,4)):
  feat, val = chooseBestSplit(dataSet,leafType, errType, ops)
  # 2: return leaf value if stopping condition met
  if feat == None:
    return val
  retTree = {}
  retTree['spInd'] = feat
  retTree['spVal'] = val
  lSet, rSet = binSplitDataset(dataSet, feat, val)
  retTree['left'] = createTree(lSet, leafType, errType, ops)
  retTree['right'] = createTree(rSet, leafType, errType, ops)
  return retTree
    












































