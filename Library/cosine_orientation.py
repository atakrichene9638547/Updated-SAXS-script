def cosine_orientation(phi, intensity,plot_azimuth = 1,stat = 0):
    """ Perform the orientation analysis based on cSAXS orientation process. Take the azimuthal data and perform a fft of the signal.

    Args:
        phi (float,int): azimuthal agle going from 0 to 360 degree
        intensity (float, int): intensity of the azimuthal profile
        plot_azimuth (int, optional): Plot azimuthal profile before inspection and with the fit. Defaults to 1.
        stat (int, optional): Display goodness of the fit. Defaults to 0.
        
    Returns:
        float: degree of orientation and angle of orientation
    """
    import numpy as np
    import pandas as pd
    import math
    import matplotlib.pyplot as plt
    from scipy.fft import fft
    
    # Define the size of half of the data set for averaging. 
    halflength = len(intensity) // 2  # Use // for integer division
    intensity_mean = np.zeros(halflength)

    # Average the data over the range 0:180
    for ii, _ in enumerate(intensity[:halflength]):
        Int_mean = (intensity[ii] + intensity[ii + halflength]) / 2
        intensity_mean[ii] = Int_mean
        
    # Define the segements
    segment = len(phi)
    # Fourier tansform of the azimuth
    I_fft = fft(intensity_mean)
    
    # Extract parameters symmetric and assymetric intensities
    f1_amp = np.real(I_fft[0]) / (segment/2)
    f2_amp = 2 * np.abs(I_fft[1]) / (segment/2)
    
    # Extract the angle of orientation (phase of the FFT[1])
    f2_phase = np.angle(I_fft[1])
    # Calculate the degree of orientation
    degree_of_orientation = f2_amp / f1_amp
    # Calculate the angle of orientation
    angle_of_orientation = math.degrees(f2_phase)

    # Calculate the fitted values
    n = np.arange(0,halflength)
    fit_intensity = f1_amp + f2_amp * np.cos(2 * np.pi * n / (segment / 2) + f2_phase)
    
    if stat == 1:
    # Calculate the delta
        Delta_fit = abs(intensity_mean-fit_intensity)
        MSE = np.sqrt(np.nanmean(Delta_fit))
        goodness_of_fit = {'MSE': MSE}
    elif stat == 0:
        goodness_of_fit = {}
    
    # Plotting data and fitted values 
    if plot_azimuth == 1:
        plt.plot ( n, intensity_mean)
        plt.plot (n,fit_intensity,linewidth = 1)
 
       
    return degree_of_orientation, angle_of_orientation, goodness_of_fit