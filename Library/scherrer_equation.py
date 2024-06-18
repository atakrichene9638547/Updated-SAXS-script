import math 
import numpy as np
def scherrer_equation(fwhm, peak_max, **kwargs):
    """Calculate the Scherrer Equation for a diffraction peak based on the FWHM and peak position

    Args:
        fwhm (float, int): full width half max of the fitted diffraction peak. Can be in nm or 2theta 
        peak_max (_type_): position of maximum of the fitted peak. Can be in nm or 2theta
        
    Kwargs: 
        unit = nm - convert fwhm and peak_max to 2theta using q2t() function
        source = ('Cu','Mo','Ag', 'Co', 'Fe', wavelength) - (str, float): wavelength of the source in nm - default 'Cu'= 1.5406
 
    Returns:
        crystallite_length (float): crystallite size in nm
    """
    if not isinstance(fwhm, (float, int,str)):
        raise TypeError('fwhem should be a float or int')
    if not isinstance (peak_max, (float,int)):
        raise TypeError('peak_max should be a float or int')
    if 'source' in kwargs:
        if not isinstance(kwargs['source'], (str,float,int)):
            raise TypeError('source should be a string or float or int')      

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
        
    if 'unit' in kwargs and kwargs['unit'] == 'nm':
        fwhm = q2t (fwhm, source = wavelength)
        peak_max= q2t (peak_max, source = wavelength)
    else: 
        pass 
    crystallite_length = (wavelength *0.89) / (math.radians(fwhm)*np.cos(math.radians(peak_max)))   
    return crystallite_length 