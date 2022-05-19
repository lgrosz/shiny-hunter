def verify_scalars(colormodel: str, scalars: [str]) -> bool:
    '''
    Takes a colormodel and a list of scalars. It ensures that each scalar
    exists in the colormodel
    '''
    for scalar in scalars:
        if scalar not in colormodel:
            return False
    return True

