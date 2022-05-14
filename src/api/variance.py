# TODO The params should have the same dimensions but this function should
# not depend on the actual number of them
def variance(a, b):
    '''
    Takes finds the Euclidean distance between two points
    '''
    return (b[0]-a[0])**2 + (b[1]-a[1])**2 + (b[2]-a[2])**2

