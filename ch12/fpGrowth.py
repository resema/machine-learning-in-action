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
      
'''
builds the FP Tree (FP:=Frequent Pattern)
'''
def createTree(dataSet, minSup=1):
  headerTable = {}
  # first pass goes through everthing and counts the frequencies of each term
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
  # expand table to hold a count and a pointer to the first item of each type
  for k in headerTable:
    headerTable[k] = [headerTable[k], None]
  retTree = treeNode('Null Set', 1, None)   # create base node
  # iterate a second time using only items that are frequent
  for tranSet, count in dataSet.items():
    localD = {}
    # 3: sort transaction by global frequency
    for item in tranSet:
      if item in freqItemSet:
        localD[item] = headerTable[item][0]
    if len(localD) > 0:
      orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
      # 4: populate tree with ordered freq itemset
      updateTree(orderedItems, retTree, headerTable, count)
  return retTree, headerTable
  
'''
growth the tree
'''
def updateTree(items, inTree, headerTable, count):
  if items[0] in inTree.children:
    inTree.children[items[0]].inc(count)
  else:
    inTree.children[items[0]] = treeNode(items[0], count, inTree)
    if headerTable[items[0]][1] == None:
      headerTable[items[0]][1] = inTree.children[items[0]]
    else:
      updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
  if len(items) > 1:
    # 5: recursevely call updateTree on remaining items
    updateTree(items[1::], inTree.children[items[0]], headerTable, count)
 
'''
makes sure the node links point to very instance of this item in the tree
'''
def updateHeader(nodeToTest, targetNode):
  while (nodeToTest.nodeLink != None):
    nodeToTest = nodeToTest.nodeLink
  nodeToTest.nodeLink = targetNode
  
'''
Example Dataset
'''
def loadSimpDat():
  simpDat = [['r','z','h','j','p'],
             ['z','y','x','w','v','u','t','s'],
             ['z'],
             ['r','x','n','o','s'],
             ['y','r','x','z','q','t','p'],
             ['y','z','x','e','q','s','t','m']]
  return simpDat
  
def createInitSet(dataSet):
  retDict = {}
  for trans in dataSet:
    retDict[frozenset(trans)] = 1
  return retDict
      
















































