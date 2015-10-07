__author__ = 'Chandu'
import argparse,copy,os
import random,math, codecs

#Command line argument description
parser = argparse.ArgumentParser()
parser.add_argument("clusterCount", help="Number of clusters")
parser.add_argument("initializationMethod", help="Cluster initialisation (rand = random, first = first k points)")
parser.add_argument("threshold", help="convergence error threshold")
parser.add_argument("maxItr", help="maximum number if iterations")
parser.add_argument("inputFile", help="input file path")
args = parser.parse_args()


class kmeans:
    prevCentroids = {}
    centroids = {}
    clusters = {}
    dataPoints={}
    pointToCluster ={}

    def __init__(self, path, centroidOption, clusterCount):
        lines = None
        with open(path,"r") as reader:
            lines = reader.readlines()
        counter=1
        for line in lines:
            vector = line.strip().split(",")
            self.dataPoints[counter] = tuple(vector)
            self.pointToCluster[counter] = 1
            counter+=1

        clusterCount = int(clusterCount)
        #Initialize centroids
        if centroidOption=="first":
            for i in range(1,clusterCount+1,1):
                self.centroids.setdefault(i,[])
                self.centroids[i] = self.dataPoints[i]
        elif centroidOption=="rand":
            dataIndex=[]
            for i in range(1,clusterCount+1,1):
                while True:
                    index = random.randint(1,len(lines))
                    if not dataIndex.__contains__(index):
                        dataIndex.append(index)
                        break
                self.centroids.setdefault(i,[])
                self.centroids[i] = self.dataPoints[index]


        #initialize copy of centroids
        self.prevCentroids = copy.deepcopy(self.centroids)

        #initialize clusters with cluster numbers
        self.initializeClusters()


    def initializeClusters(self):
        for i in range(1,int(clusterCount)+1,1):
            self.clusters[i] = []

    ##End of Initialization

    #Clustering
    def clustering(self):
        #run clustering for the number of iterations provided in input parameters
        for itr in range(1,int(maxItr)+1,1):
            for index in self.dataPoints.keys():
                pointVector = list(self.dataPoints.get(index))
                clusterNumber = self.closestCentriod(pointVector)

                #add the point vector to corresponding cluster
                self.clusters[clusterNumber].append(pointVector)

                #identifies which cluster the point is assigned to
                self.pointToCluster[index] = clusterNumber

            self.updateCentroids()
            self.initializeClusters()
            if not(self.changeInCentroids()):
                #if there is no change in centroids
                break
        self.generateOutput()


    #For each data point identify the closest centroid
    #cluster number is same as centroid number
    def closestCentriod(self,pointVector):
        minDist = float("Inf")
        clusterNumber = 1
        for index in self.centroids.keys():
            centroidVector = list(self.centroids.get(index))
            tempDist = self.distanceMeasure(centroidVector, pointVector)
            if tempDist < minDist:
                clusterNumber = index
                minDist = tempDist

        return clusterNumber

    #calculate the euclidean distance between 2 points.
    def distanceMeasure(self, centroidVector, pointVector):
        sum = 0.0
        for i in range(0,len(centroidVector),1):
            sum += (float(centroidVector[i]) - float(pointVector[i]))**2
        return math.sqrt(sum)

    #check if cluster centers have moved
    def changeInCentroids(self):
        for i in self.centroids.keys():
            dist = self.distanceMeasure(self.centroids.get(i), self.prevCentroids.get(i))
            if(dist > float(threshold)):
                return True
        return False

    #update cluster centers and calculate new centroids
    def updateCentroids(self):

        #for every cluster, with the points
        for key in self.clusters.keys():
            count = len(self.clusters[key])

            #create an empty centroid point vector
            centroid = [0.0]*len(list(self.centroids.get(key)))

            #for every point in the cluster
            for point in self.clusters.get(key):
                #add the value of every dimension to corresponding dimension in centroid vector.
                for i in range(0,len(point),1):
                    centroid[i] += float(point[i])
            #get the mean value for each dimension by dividing with the number of points in that cluster
            for i in range(0,len(centroid),1):
                if not float(centroid[i]==0.0):
                    centroid[i] = float(centroid[i]) / count

            #save the old centroid co-ordinates
            self.prevCentroids[key] = self.centroids[key]

            #update the corresponding cluster centroid with the new centroid
            self.centroids[key] = centroid

    def generateOutput(self):
        output = ""

        for i in self.centroids.keys():
            output += ",".join([str(val) for val in self.centroids.get(i)])+ os.linesep

        #prints cluster numbers for all input points in the same order.
        for key in sorted(self.pointToCluster.keys()):
            output+=str(self.pointToCluster.get(key)-1)+os.linesep

        with open(inputFile+".output","w") as writer:
            writer.write(output)


if __name__ == '__main__':

    #read command line arguments into variables.
    clusterCount = args.clusterCount
    option = args.initializationMethod
    threshold = float(args.threshold.decode())
    maxItr = args.maxItr
    inputFile = args.inputFile


    kmeansInstance = kmeans(inputFile,option,clusterCount)
    kmeansInstance.clustering()