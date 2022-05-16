from .change_basis import change_basis
from .pick import pick
from .variance import variance

def detect(pos, color, colormodel='rgb', scalars=[], allowed_variance=0):
    '''
    Detects the colored pixel at the given location. A tolerance can be
    provided as well as a timeout. This function is blocking.

    pos := (x, y) position of the screen
    color: = (r, g, b) color of the pixel
    colormodel := The colormodel which to detect the pixel in
    scalars := The scalars which to take into account when detecting the pixel
    allowed_variance := maximum allowed color variance where variance is the square of
                 the Euclidean distance between two colors.

    '''
    color = change_basis(color, colormodel, scalars)
    while True:
        c = change_basis(pick(*pos), colormodel, scalars)
        if (variance(c, color) <= allowed_variance):
            break

