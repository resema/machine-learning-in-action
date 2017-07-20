'''
Created on 18 July 2017
Association analysis with the Apriori algorithm

@autor: resema
'''

from numpy import *

def loadDataSet():
  return [[1,3,4], [2,3,5], [1,2,3,5], [2,5]]
  
def createC1(dataSet):
  C1 = []   # C1 is a candidate itemset of size one
  for transaction in dataSet:
    for item in transaction:
      if not [item] in C1:  # add a list instead of elem -> possible to use set operations
        C1.append([item])
  C1.sort()
  # 1: create a frozenset of each item in CI
  return map(frozenset, C1)
  
def scanD(D, Ck, minSupport): # D := dataset, Ck := list of candidate sets
  ssCnt = {}
  for tid in D:
    for can in Ck:
      if can.issubset(tid):
        if not ssCnt.has_key(can):
          ssCnt[can] = 1
        else:
          ssCnt[can] += 1
  numItems = float(len(D))
  retList = []
  supportData = {}
  for key in ssCnt:
    # 2: calculate support for every itemset
    support = ssCnt[key]/numItems
    if support >= minSupport:
      retList.insert(0,key) # insert at the beginning
    supportData[key] = support
  return retList, supportData
  
'''
create candidate itemsets
'''
def aprioriGen(Lk, k):  # creates Ck
  retList = []
  lenLk = len(Lk)
  for i in range(lenLk):
    for j in range(i+1, lenLk):
      # 1: joins sets if first k-2 items are equal
      L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]
      L1.sort(); L2.sort()
      if L1==L2:
        retList.append(Lk[i] | Lk[j])   # set union operation
  return retList
  
def apriori(dataSet, minSupport = 0.5):
  C1 = createC1(dataSet)
  D = map(set, dataSet)
  L1, supportData = scanD(D, C1, minSupport)
  L = [L1]
  k = 2
  while (len(L[k-2]) > 0):
    Ck = aprioriGen(L[k-2], k)
    # 2: scan data set to get Lk from Ck
    Lk, supK = scanD(D, Ck, minSupport)
    supportData.update(supK)
    L.append(Lk)
    k += 1
  return L, supportData
  
def generateRules(L, supportData, minConf=0.7):
  bigRuleList = []
  # 1: get only sets with two or more items
  for i in range(1, len(L)):
    for freqSet in L[i]:
      H1 = [frozenset([item]) for item in freqSet]
      if (i > 1):
        rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
      else:
        calcConf(freqSet, H1, supportData, bigRuleList, minConf)
  return bigRuleList
  
def calcConf(freqSet, H, supportData, br1, minConf=0.7):
  prunedH = []
  for conseq in H:
    conf = supportData[freqSet]/supportData[freqSet-conseq]
    if conf >= minConf:
      print freqSet-conseq, '-->', conseq, 'conf:', conf
      br1.append((freqSet-conseq, conseq, conf))
      prunedH.append(conseq)
  return prunedH
  
def rulesFromConseq(freqSet, H, supportData, br1, minConf=0.7):
  m = len(H[0])
  # 2: try further merging
  if (len(freqSet) > (m + 1)):
    # 3: create Hm+1 new candidates
    Hmp1 = aprioriGen(H, m + 1)
    hmp1 = calcConf(freqSet, Hmp1, supportData, br1, minConf)
    if (len(hmp1) > 1):
      rulesFromConseq(freqSet, Hmp1, supportData, br1, minConf)
      
from time import sleep
from votesmart import votesmart
votesmart.apikey = 'a7fa40adec6f4a77178799fae4441030'
def getActionIds():
  actionIdList = []; billTitleList = []
  fr = open('recent20bills.txt')
  for line in fr.readlines():
    billNum = int(line.split('\t')[0])
    try:
      billDetail = votesmart.votes.getBill(billNum)
      for action in billDetail.actions:
        # 1: Filter out actions that have votes
        if action.level == 'House' and \
          (action.stage == 'Passage' or \
           action.stage == 'Amendment Vote'):
          actionId = int(action.actionId)
          print 'bill: %d has actionId: %d' % (billNum, actionId)
          actionIdList.append(actionId)
          billTitleList.append(line.strip().split('\t')[1])
    except:
      print 'problem getting bill %d' % billNum
    # 2: delay to be polite
  return actionIdList, billTitleList














































