'''
Created on 26 July 2017
Simplifying data with the singular value decomposition (SVD)
  apply the SVD to recommendation engines to improve their accuracy

@autor: resema
'''

from numpy import *
from numpy import linalg as la

def loadExData():
  return[[1,1,0,2,2],
         [0,0,0,3,3],
         [0,0,0,1,1],
         [1,1,1,0,0],
         [2,2,2,0,0],
         [1,1,1,0,0],
         [5,5,5,0,0]]
         
def ecludSim(inA, inB):
  return 1.0/(1.0 + la.norm(inA - inB))
  
def pearsSim(inA, inB):
  if len(inA) < 3: return 1.0
  return 0.5 + 0.5*corrcoef(inA, inB, rowvar=0)[0][1]
  
def cosSim(inA, inB):
  num = float(inA.T*inB)
  denom = la.norm(inA)*la.norm(inB)
  return 0.5+0.5*(num/denom)
  
def standEst(dataMat, user, simMeas, item):
  n = shape(dataMat)[1]
  simTotal = 0.0; ratSimTotal = 0.0
  for j in range(n):
    userRating = dataMat[user,j]
    if userRating == 0: 
      continue
    # 1: find items rated by both users
    overLap = nonzero(logical_and(dataMat[:,item].A>0, dataMat[:,j].A>0))[0]
    if len(overLap == 0): 
      similarity = 0
    else: 
      similarity = simMeas(dataMat[overLap, item], dataMat[overLap,j])
    print 'the %d and %d similarity is: %f' % (item, j, similarity)
    simTotal += similarity
    ratSimTotal += similarity * userRating
  if simTotal == 0: 
    return 0
  else: 
    return ratSimTotal/simTotal
  
'''
recommendation engine
'''
def recommend(dataMat, user, N=3, simMeas=cosSim, estMethod=standEst):
  # 2: find unrated items
  unratedItems = nonzero(dataMat[user,:].A==0)[1]
  if len(unratedItems) == 0:
    return 'you rated everything'
  itemScores = []
  for item in unratedItems:
    estimatedScore = estMethod(dataMat, user, simMeas, item)
    itemScores.append((item, estimatedScore))
  # 3: return top N unreated items
  return sorted(itemScores, key=lambda jj: jj[1], reverse=True)[:N]
  
''' 
calculate similarities in data space
'''
def svdEst(dataMat, user, simMeas, item):
  n = shape(dataMat)[1]
  simTotal = 0.0; ratSimTotal = 0.0
  U,Sigma,VT = la.svd(dataMat)
  # 1: create diagonal matrix
  Sig4 = mat(eye(4)*Sigma[:4])
  # 2: create transformed items
  xformedItems = dataMat.T * U[:,:4] * Sig4.I
  for j in range(n):
    userRating = dataMat[user,j]
    if userRating == 0 or j == item:
      continue
    similarity = simMeas(xformedItems[item,:].T, xformedItems[j,:].T)
    print 'the %d and %d similarity is: %f' % (item, j, similarity)
    simTotal += similarity
    ratSimTotal += similarity * userRating
  if simTotal == 0:
    return 0
  else:
    return ratSimTotal/simTotal









































