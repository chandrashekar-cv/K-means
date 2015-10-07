# K-means
K-means algorithm.

K-means clustering of data points. In this implementation I have considered the data points te be vector co-ordinates of points in multidimensional space. Code is scalable to any dimension. Constraint is that all the data points need to be of the same dimension. Euclidean distance is used to identify the cluster for a data point. Code is modular and easy to understand. The distance metrics calculation is written in a different function so that the code can be reused on different data sets or different distance metrics by just replacing the distance calculation function.   If you feel the code needs some updates or optimization, then please let me know. We can work together to make it even simpler.

Command line arguments:
1st argument: number of clusters - k
2nd argument: initialization method -­‐ "rand": random -­‐ "first": select first k points from input file as initialized centroids.
3rd argument: convergence threshold (if change between 2 iterations is smaller than this threshold, converged).
4th argument: maximum number of iterations (stops after max number of trials even if convergence threshold not met)
5th argument: input file name
