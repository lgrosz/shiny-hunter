from colorsys import rgb_to_hls


def change_basis(rgb: tuple[float], colormodel: str, scalars: [str]):
    '''
    Takes an `rgb` color changes it to the specified `colormodel`, then reduces
    its span to the `scalars` specified
    '''
    if (len(rgb) != len(colormodel)):
        raise Exception("Provided color and colormodel must be of the same size.")

    color = rgb

    if (colormodel == 'hls'):
        color = rgb_to_hls(*color)

    if (scalars):
        color = list(zip(*filter(lambda x: x[0] in scalars, zip(colormodel, color))))[1]

    return color

