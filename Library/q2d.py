def q2d (q,**kwargs): 
    import math 
    import numpy as np
    """Calculate the distance in real space based on the q-value given. Unit can be A or nm - nm per default.

    Args:
        q (float): Qvalue for the particular size
        source (string): Source 
    Return: 
        dist (float): distance in real space in nm
    """
    if not isinstance(q, (float, int)):
        raise TypeError('q should be a float')
    if 'unit' in kwargs:
        if not isinstance(kwargs['unit'], str):
            raise TypeError('unit should be a string')
        if kwargs['unit'] == 'nm':
            dist = 2 * np.pi / q
            print(f'{dist} nm')
        elif kwargs['unit'] == 'A':
            dist= 2 * np.pi / q * 10
            print(f'{dist} A')
        else:
            raise ValueError('Unit unknown - Should be A or nm')
    else:
        dist = 2 * np.pi / q
        print(f'{dist} nm')
    return dist