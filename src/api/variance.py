from scipy.spatial.distance import euclidean

# TODO The params should have the same dimensions but this function should
# not depend on the actual number of them
def variance(a, b):
    '''
    Takes finds the Euclidean distance between two points
    '''
    if (len(a) != len(b)):
        raise Exception('Can only calculate variance for vectors of the same size')
    return euclidean(a, b)

