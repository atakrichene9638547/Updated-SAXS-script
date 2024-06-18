import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 

def plot_scattering_curves(qdata,idata,**kwargs):
    """Create a graph for the scattering curves
        Parameters: q-data - q-range of the data in nm
                    idata - Intensity 
                    sname - sample name
                    legend - show legend
                    
        Return = none
    """
    plt.figure(figsize=(10, 6))
    
    for i in range(len(qdata)):
        x1 = qdata[i]
        y1 = idata[i]
        
        # Plotting the curves in log-log
        if 'sname' in kwargs and kwargs['sname']:
            sname = kwargs['sname']
            plt.loglog(x1, y1, label=sname[i]) 
        else:
            plt.loglog(x1, y1)
            
        # Optionally plot in linear scale
        if 'linear' in kwargs and kwargs['linear']: 
            plt.plot(x1, y1)

    # Define the label of the curves 
    if 'ylabel' in kwargs and kwargs['ylabel']: 
        plt.ylabel(kwargs['ylabel'])
    else:
        plt.ylabel('Intensity')
        
    plt.xlabel('q (nm⁻¹)')
    
    # Optionally show legend
    if 'legend' in kwargs and kwargs['legend']: 
        plt.legend()

    plt.show()