'''
Created on 20 July 2017
FP-Trees: an efficient way to encode a dataset
  FP := Frequent Pattern

@autor: resema
'''

class treeNode:
  def __init__(self, nameValue, numOccur, parentNode):
    self.name = nameValue
    self.count = numOccur
    self.nodeLink = None
    self.parent = parentNode
    self.children = {}
    
  def inc(self, numOccur):
    self.count += numOccur
    
  def disp(self, ind=1):
    print '  '*ind, self.name, ' ', self.count
    for child in self.children.values():
      child.disp(ind+1)
      
def createTree(dataSet, minSup=1):
  headerTable = {}
  for trans in dataSet:
    for item in trans:
      headerTable[item] = headerTable.get(item, 0) + dataSet[trans]   # dict get('key', defaultVal)
  # 1: remove item not meeting min support
  for k in headerTable.keys():
    if headerTable[k] < minSup:
      del (headerTable[k])
  freqItemSet = set(headerTable.keys())
  # 2: if no items meet min support, exit
  if len(freqItemSet) == 0: return None, None
  for k in headerTable:
    headerTable[k]= [headerTable[k], None]
  retTree = treeNode('Null Set', 1, None)
  for tranSet, count in dataSet.items():
    localID = {}
    # 3: sort transaction by global frequency
    for item in tranSet:
      if item in freqItemSet:
        localD[item] = headerTable[item][0]
    if len(localD) > 0:
      orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=Tre)]
      # 4: populate tree with ordered freq itemset
      updateTree(orderedItems, retTree, headerTable, count)
  return retTree, headerTable
















































