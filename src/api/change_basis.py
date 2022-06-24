from colorsys import rgb_to_hls, rgb_to_yiq, rgb_to_hsv


Bases = ['rgb', 'hls', 'hsv', 'yiq']

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
    elif (colormodel == 'hsv'):
        color = rgb_to_hsv(*color)
    elif (colormodel == 'yiq'):
        color = rgb_to_yiq(*color)

    if (scalars):
        color = list(zip(*filter(lambda x: x[0] in scalars, zip(colormodel, color))))[1]

    return color

