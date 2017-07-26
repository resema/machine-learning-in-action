'''
Created on 26 July 2017
Method for dimensionality reduction
  Principal component reduction (PCA)
    where is the majority of the variance contained?
  Factor analysis
    data is assumed to be a linear combination of latent variable and some noise
  Independent component analysis (ICA)
    similar to PCA, but sources are statically independent, which assumes data is uncorrelated
@autor: resema
'''

from numpy import *

def loadDataSet(fileName, delim='\t'):
  fr = open(fileName)
  stringArr = [line.strip().split(delim) for line in fr.readlines()]
  datArr = [map(float, line) for line in stringArr]
  return mat(datArr)
  
def replaceNanWithMean():
  datMat = loadDataSet('secom.data', ' ')
  numFeat = shape(datMat)[1]
  for i in range(numFeat):
    # 1: find mean of non-NaN values
    meanVal = mean(datMat[nonzero(~isnan(datMat[:,i].A))[0],i])
    # 2: set NaN values to mean
    datMat[nonzero(isnan(datMat[:,i].A))[0],i] = meanVal
  return datMat
  
def pca(dataMat, topNfeat=9999999):
  meanVals = mean(dataMat, axis=0)
  # 1: remove mean
  meanRemoved = dataMat - meanVals
  covMat = cov(meanRemoved, rowvar=0)
  eigVals, eigVects = linalg.eig(mat(covMat))
  eigValInd = argsort(eigVals)
  # 2: sort top N smallest to largest
  eigValInd = eigValInd[:-(topNfeat+1):-1]
  redEigVects = eigVects[:,eigValInd]
  # 3: transform data into new dimension
  lowDDataMat = meanRemoved * redEigVects
  reconMat = (lowDDataMat * redEigVects.T) + meanVals
  return lowDDataMat, reconMat





































