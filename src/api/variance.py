from scipy.spatial.distance import euclidean

# TODO The params should have the same dimensions but this function should
# not depend on the actual number of them
def variance(a, b):
    '''
    Takes finds the Euclidean distance between two points
    '''
    return euclidean(a, b)

