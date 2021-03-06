'''
Created on 12 July 2017
Grouping unlabeled items using k-means clustering

@autor: resema
'''

from numpy import *
import urllib
import json
from time import sleep

def loadDataSet(fileName):
  dataMat = []
  fr = open(fileName)
  for line in fr.readlines():
    curLine = line.strip().split('\t')
    fltLine = map(float, curLine)
    dataMat.append(fltLine)
  return dataMat
  
# Euclidean distance
def distEclud(vecA, vecB):
  return sqrt(sum(power(vecA - vecB, 2)))
  
def randCent(dataSet, k):
  n = shape(dataSet)[1]
  centroids = mat(zeros((k,n)))
  # create cluster centroids
  for j in range(n):
    minJ = min(dataSet[:,j])
    rangeJ = float(max(dataSet[:,j]) - minJ)
    centroids[:,j] = minJ + rangeJ * random.rand(k,1)
  return centroids
  
def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
  m = shape(dataSet)[0]
  clusterAssment = mat(zeros((m,2)))  # two columns: one for cluster index and second to store error
  centroids = createCent(dataSet, k)
  clusterChanged = True
  while clusterChanged:
    clusterChanged = False
    for i in range(m):
      minDist = inf; minIndex = -1
       # 1: find the closest centroid
      for j in range(k):
        distJI = distMeas(centroids[j,:], dataSet[i,:])
        if distJI < minDist:
          minDist = distJI; minIndex = j
      if clusterAssment[i,0] != minIndex:
        clusterChanged = True
      clusterAssment[i,:] = minIndex, minDist**2
    print centroids
    # 2: update centroid location
    for cent in range(k):
      ptsInClust = dataSet[nonzero(clusterAssment[:,0].A == cent)[0]]
      centroids[cent,:] = mean(ptsInClust, axis=0)
  return centroids, clusterAssment

# bisecting k-means clustering algorithm
def biKmeans(dataSet, k, distMeas=distEclud):
  m = shape(dataSet)[0]
  clusterAssment = mat(zeros((m,2)))
  # 1: initially create one cluster
  centroid0 = mean(dataSet, axis=0).tolist()[0]
  centList = [centroid0]
  for j in range(m):
    clusterAssment[j,1] = distMeas(mat(centroid0), dataSet[j,:])**2
  while(len(centList) < k):
    lowestSSE = inf   # SSE: sum of squared errors
    for i in range(len(centList)):
      # 2: try splitting every cluster
      ptsInCurrCluster = dataSet[nonzero(clusterAssment[:,0].A==i)[0],:]
      centroidMat, splitClustAss = kMeans(ptsInCurrCluster, 2, distMeas)
      sseSplit = sum(splitClustAss[:,1])
      sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:,0].A!=i)[0],1])
      print "sseSplit, and notSplit: ", sseSplit, sseNotSplit
      if(sseSplit + sseNotSplit) < lowestSSE:
        bestCentToSplit = i
        bestNewCents = centroidMat
        bestClustAss = splitClustAss.copy()
        lowestSSE = sseSplit + sseNotSplit
    # 3: update the cluster assignments
    bestClustAss[nonzero(bestClustAss[:,0].A == 1)[0],0] = len(centList)
    bestClustAss[nonzero(bestClustAss[:,0].A == 0)[0],0] = bestCentToSplit
    print 'the bestCentToSplit is: ', bestCentToSplit
    print 'the len of bestClustAss is: ', len(bestClustAss)
    centList[bestCentToSplit] = bestNewCents[0,:]
    centList.append(bestNewCents[1,:])
    clusterAssment[nonzero(clusterAssment[:,0].A == bestCentToSplit)[0],:] = bestClustAss
  return centList, clusterAssment
  
def geoGrab(stAddress, city):
  apiStem = 'https://maps.googleapis.com/maps/api/geocode/json?'
  params = {}
  # 1: set JSON as return type
  params['address'] = '%s %s' % (stAddress, city)
  params['key'] = 'AIzaSyArXPPExHkU6J8WW6sJiMOCqClPwEZYIHE'
  url_params = urllib.urlencode(params)
  googleApi = apiStem + url_params
  # 2: print outgoing URL
  # print googleApi
  c = urllib.urlopen(googleApi)
  return json.loads(c.read())
  
def massPlaceFind(fileName):
  fw = open('places.txt', 'w')
  for line in open(fileName).readlines():
    line = line.strip()
    lineArr = line.split('\t')
    retDict = geoGrab(lineArr[1], lineArr[2])
    # if retDict['ResultSet']['Error'] == 0:
    if retDict['status'] == 'OK':
      lat = float(retDict['results'][0]['geometry']['location']['lat'])
      lng = float(retDict['results'][0]['geometry']['location']['lng'])
      print "%s\t%f\t%f" % (lineArr[0], lat, lng)
      fw.write('%s\t%f\t%f\n' % (line, lat, lng))
    else:
      print "error fetching"
    sleep(1)
  fw.close()
  
def distSLC(vecA, vecB):
  a = sin(vecA[0,1]*pi/180) * sin(vecB[0,1]*pi/180)
  b = cos(vecA[0,1]*pi/180) * cos(vecB[0,1]*pi/180) * cos(pi * (vecB[0,0]-vecA[0,0]) / 180)
  return arccos(a + b)*6371.0
  
import matplotlib
import matplotlib.pyplot as plt
def clusterClubs(numClust=5):
  datList = []
  for line in open('places.txt').readlines():
    lineArr = line.split('\t')
    datList.append([float(lineArr[4]), float(lineArr[3])])
  datMat = mat(datList)
  myCentroids, clustAssing = biKmeans(datMat, numClust, distMeas=distSLC) # why assignment in function passing
  fig = plt.figure()
  rect=[0.1,0.1,0.8,0.8]
  scatterMarkers = ['s','o','^','8','p','d','v','h','>','<']
  axprops = dict(xticks=[], yticks=[])
  ax0 = fig.add_axes(rect, label='ax0', **axprops)
  # 1: create matrix from image
  imgP = plt.imread('Portland.png')
  ax0.imshow(imgP)
  ax1 = fig.add_axes(rect, label='ax1', frameon=False)
  for i in range(numClust):
    ptsInCurrCluster = datMat[nonzero(clustAssing[:,0].A==i)[0],:]
    markerStyle = scatterMarkers[i % len(scatterMarkers)]
    ax1.scatter(ptsInCurrCluster[:,0].flatten().A[0], \
                ptsInCurrCluster[:,1].flatten().A[0], \
                marker=markerStyle, s=90)
  myCents = mat(zeros((numClust, 2)))
  for i in range(numClust):
    myCents[i,0] = myCentroids[i][:,0]
    myCents[i,1] = myCentroids[i][:,1]
  ax1.scatter([myCents[:,0]], \
              [myCents[:,1]], marker='+', s=300)
  plt.show()
  
  
  
  
  

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  



















