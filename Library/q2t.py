import math 
import numpy as np
def q2t (q_value,**kwargs):
    """Calculate the 2theta angle from the q-value in nm and the wavelength of the source
        kwargs = source (Cu, Mo, Ag, Co, Fe) - if left empty = Cu
    Args:
        q_value (float, int): q_value in nanometer

    Returns:
       2theta vavlue (float): 2theta angle in degree
    """
    if not isinstance(q_value, (float, int,str)):
        raise TypeError('q should be a float')
    if 'source' in kwargs:
        if not isinstance(kwargs['source'], (str,float,int)):
            raise TypeError('source should be a string')
        
    if 'source' in kwargs:     
        if kwargs['source'] == ('Cu'):
            wavelength =  0.15406
        elif kwargs['source'] == ('Mo'):
            wavelength = 0.071073
        elif kwargs['source'] == ('Ag'):
            wavelength = 0.024
        elif kwargs['source'] == ('Co'):
            wavelength = 0.17902
        elif kwargs['source'] == ('Fe'):
            wavelength = 0.19373
        elif kwargs['source'] is not ['Cu','Mo','Ag', 'Co', 'Fe']:
            wavelength = kwargs['source']
    else:
        wavelength = 0.15406  
    
    theta = 2*math.sin((q_value*wavelength)/(4*np.pi))*(180/np.pi)
    return theta