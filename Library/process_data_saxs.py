import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
import glob
import os 
import pathlib

def import_scattering_data(path="Raw", **kwargs):
    """
    Prepare the data from the path folder to be used for transmission correction

    Parameters: Path - full path of the folder containing all your data

    Return: li - an array containing all the q-range, intensity and error data
            qdata - raw q-range data
            idata - raw intensity data
            err - raw incertitude data
    """
    # Get only files with specific extention
    B = glob.glob(path + "*dat_counts")

    # Show list of file
    files = os.listdir(path)
    print("CHECK THE SAMPLES POSITION AND INDEX FOR BACKGROUND SUBSTRACTION")

    for index, file in enumerate(files):
        print(index, file)

    # Create a list for the data
    qdata = []
    idata = []
    err_data = []

    for filenames in B:
        df = pd.read_csv(filenames, delim_whitespace=True, header=None)
        df = df[2:]

        # Convert the DataFrame columns to numeric dtype
        df = df.apply(pd.to_numeric, errors="coerce")
        # Convert the list to a NumPy array
        arr = np.array(df)

        # Extract the first three columns
        data1 = arr[:, :3]
        qdata1 = arr[:, 0]
        idata1 = arr[:, 1]
        err_data1 = arr[:, 2]

        qdata.append(qdata1)
        idata.append(idata1)
        err_data.append(err_data1)

    # Convert the Series to array
    qdata = pd.Series(qdata)
    idata = pd.Series(idata)
    err_data = pd.Series(err_data)

    qdata = qdata.to_numpy()
    idata = idata.to_numpy()
    err_data = err_data.to_numpy()

    # Conversion in nm
    qdata *= 10

    # Define the names of the samples
    names = os.listdir(path)
    sample_name = []
    for i in range(len(names)):
        name1 = names[i].split("_unwarped")[0]
        sample_name.append(name1)

    if "plot" in kwargs:
        for i in range(len(qdata)):
            x1 = qdata[i]
            y1 = idata[i]
            plt.loglog(x1, y1)
        plt.ylabel("Intensity")
        plt.xlabel("q 1/nm")
        plt.show()

    return qdata, idata, err_data, B, sample_name

def transmission_correction(idata, err_data):
    transmission_data = []
    idata_corrected = []
    err_corrected = []

    for i in range(len(idata)):
        data1 = np.divide(idata[i][0], idata[0][0])
        transmission_data.append(data1)

    for i in range(len(idata)):
        data1 = np.divide(idata[i], transmission_data[i])
        idata_corrected.append(data1)
        data2 = np.divide(err_data[i], transmission_data[i])
        err_corrected.append(data2)

    return idata_corrected, transmission_data, err_corrected

import numpy as np
import matplotlib.pyplot as plt

def background_subtraction(idata_corrected, err_corrected, qdata, sample_name, averaging, **kwargs):
    
    def averaging_function(idata_corrected, err_corrected):
        bck_idata = idata_corrected[:3]
        bck_err = err_corrected[:3]
        idata_to_avg = idata_corrected[3:]
        err_to_avg = err_corrected[3:]
        bck_idata.append(np.mean(idata_to_avg, axis=0))
        bck_err.append(np.mean(err_to_avg, axis=0))
        return bck_idata, bck_err 

    """
    Do the background subtraction of the data based on the different input parameters and plot the results.

    Parameters: 
        idata_corrected - Transmission corrected data
        err_corrected - Uncertainty of the intensity corrected
        qdata - q-range of the data in nm
        sample_name - Names of the samples
        averaging - Boolean indicating if averaging should be done
        **kwargs - Additional arguments including:
            air - Position of the air scattering data in the data array
            capillary - Position of the capillary scattering data in the data array
            water - Position of the water scattering data in the data array
            bck_coef - Background coefficients that will be multiplied to the background data (function of the concentration of your sample)
            q_lim - Experimental distance, will be used to cut the exploitable q-range. Options are '107', '67', '27', '5'

    Return: 
        Qdata - Usable q-range for the data set
        Idata - Background subtracted intensity data
        Err - Background subtracted uncertainty on the intensity
        sample_name - Sample names
        bck_coef - Background coefficients used
    """

    # Check how to do the background subtraction
    if "air" in kwargs and not "capillary" in kwargs:
        case = 1
    elif "air" in kwargs and "capillary" in kwargs and not "water" in kwargs:
        case = 2
    elif "air" in kwargs and "capillary" in kwargs and "water" in kwargs:
        case = 3
    else:
        raise ValueError("Invalid input arguments, arguments should be [air =0, capillary = 1, water = 2, bck_coef = [0.99], q_lim = 107]")

    # Ensure bck_coef is an array
    if "bck_coef" in kwargs:
        bck_coef = kwargs["bck_coef"]
        if not isinstance(bck_coef, (list, np.ndarray)):
            raise ValueError("bck_coef must be an array of numbers")
    else:
        bck_coef = [0.99]

    # Get all data to the same length
    lmin = min(len(arr) for arr in idata_corrected)
    idata_corrected = [arr[:lmin] for arr in idata_corrected]
    err_corrected = [arr[:lmin] for arr in err_corrected]
    qdata = [arr[:lmin] for arr in qdata]
    if averaging:
        idata_corrected, err_corrected = averaging_function(idata_corrected, err_corrected)
        # Remove all strings starting from the 3rd position (index 2)
        sample_name = sample_name[:3]
        # Add 'Averaged_data' to the list
        sample_name.append('Averaged_data')
    all_Qdata = []
    all_Idata = []
    all_Err = []
    all_sample_names = []

    plt.figure(figsize=(10, 6))
    
    for coef in bck_coef:
        bck_data = []
        bck_err = []

        # Clone the arrays for each coefficient iteration
        idata_clone = [np.copy(arr) for arr in idata_corrected]
        err_clone = [np.copy(arr) for arr in err_corrected]
        qdata_clone = [np.copy(arr) for arr in qdata]
        sample_name_clone = np.copy(sample_name)

        if case == 1:
            air_data = idata_clone[kwargs["air"]]
            err_air = err_clone[kwargs["air"]]

            for i in range(len(idata_clone)):
                data1 = idata_clone[i] - air_data * coef
                data2 = err_clone[i] - err_air * coef
                bck_data.append(data1)
                bck_err.append(data2)

            bck_data = np.delete(bck_data, [kwargs["air"]], axis=0)
            bck_err = np.delete(bck_err, [kwargs["air"]], axis=0)
            qdata_clone = np.delete(qdata_clone, [kwargs["air"]], axis=0)
            sample_name_clone = np.delete(sample_name_clone, [kwargs["air"]], axis=0)

        elif case == 2:
            air_data = idata_clone[kwargs["air"]]
            err_air = err_clone[kwargs["air"]]
            empty_cap = idata_clone[kwargs["capillary"]]
            err_cap = err_clone[kwargs["capillary"]]

            for i in range(len(idata_clone)):
                data1 = idata_clone[i] - empty_cap * coef
                data2 = err_clone[i] - err_cap * coef
                bck_data.append(data1)
                bck_err.append(data2)

            bck_data = np.delete(bck_data, [kwargs["air"], kwargs["capillary"]], axis=0)
            bck_err = np.delete(bck_err, [kwargs["air"], kwargs["capillary"]], axis=0)
            qdata_clone = np.delete(qdata_clone, [kwargs["air"], kwargs["capillary"]], axis=0)
            sample_name_clone = np.delete(sample_name_clone, [kwargs["air"], kwargs["capillary"]], axis=0)

        elif case == 3:
            air_data = idata_clone[kwargs["air"]]
            err_air = err_clone[kwargs["air"]]
            empty_cap = idata_clone[kwargs["capillary"]]
            err_cap = err_clone[kwargs["capillary"]]
            water_bck = idata_clone[kwargs["water"]]
            err_water = err_clone[kwargs["water"]]
            I_water = water_bck - empty_cap
            err_I_water = np.sqrt(err_water**2 + err_cap**2)

            for i in range(len(idata_clone)):
                data1 = idata_clone[i] - empty_cap - (I_water * (1 - coef))
                data2 = np.sqrt(
                    err_clone[i] ** 2 + err_cap**2 + (err_I_water * (coef - 1)) ** 2
                )
                bck_data.append(data1)
                bck_err.append(data2)

            bck_data = np.delete(bck_data, [kwargs["air"], kwargs["capillary"], kwargs["water"]], axis=0)
            bck_err = np.delete(bck_err, [kwargs["air"], kwargs["capillary"], kwargs["water"]], axis=0)
            qdata_clone = np.delete(qdata_clone, [kwargs["air"], kwargs["capillary"], kwargs["water"]], axis=0)
            sample_name_clone = np.delete(sample_name_clone, [kwargs["air"], kwargs["capillary"], kwargs["water"]], axis=0)

        indices = []
        qdata_clone = np.array(qdata_clone)

        if kwargs["q_lim"] == 107:
            cut_off = 0.07
        elif kwargs["q_lim"] == 147:
            cut_off = 0.05
        elif kwargs["q_lim"] == 67:
            cut_off = 0.12
        elif kwargs["q_lim"] == 27:
            cut_off = 0.25
        elif kwargs["q_lim"] == 5:
            cut_off = 4.5

        for col in range(qdata_clone.shape[0]):
            index = np.argmin(np.abs(qdata_clone[col, :] - cut_off))
            indices.append(index)

        Idata = []
        Qdata = []
        Err = []

        for i, data in enumerate(bck_data):
            cut_data1 = data[indices[i]:]
            Idata.append(cut_data1)
            cut_data2 = qdata_clone[i][indices[i]:]
            Qdata.append(cut_data2)
            cut_data3 = bck_err[i][indices[i]:]
            Err.append(cut_data3)

        all_Qdata.extend(Qdata)
        all_Idata.extend(Idata)
        all_Err.extend(Err)
        all_sample_names.extend([f"{name}, coef={coef:.2f}" for name in sample_name_clone])

        for q, I, s in zip(Qdata, Idata, sample_name_clone):
            plt.loglog(q, I, label=f'{s}, coef={coef:.2f}')

    plt.xlabel('Q')
    plt.ylabel('Intensity')
    plt.legend()
    plt.title('Background Subtracted Data')
    plt.show()

    return all_Qdata, all_Idata, all_Err, all_sample_names, bck_coef,averaging



def process_data(path,averaging, **kwargs):
    """
    Function including all the previous function of the class object - read the data in the path folder, clean the data, perform background substrction

    Paramters:  path - full path of the folder containing the data
                air - position of the air scattering (also called empty beam) data in the data-array
                capillary - position of the capillary scattering (or kapton or any other background that needs to be substracted) data in the data-array
                water - position of the water scattering (or any other solvent background that needs to be substracted) data in the data-array
                bck_coef - backround coefficient that will be multiplied to the background data (function of the concentration of your sample)
                q_lim - experimental distance, will be used to cut the exploitable q-range. Options are '107', '67', '27','5'


    Return: Qdata - q-range of the transmission corrected and background substracted data in nm
            Idata - transmission corrected and background substracted data
            Err - incertitude on the transmission and background substracted data
            sname - sample name

    Example:
    Qdata, Idata, Err, sname = dp.process_data(path,air = 0, capillary = 1, water = 2, bck_coef = 0.99, q_lim = 107)
    """

    qdata, idata, err_data, B, sample_name = import_scattering_data(path)
    (
        idata_corrected,
        transmission_data,
        err_corrected,
    ) = transmission_correction(idata, err_data)
    Qdata, Idata, Err, sname,bck_coef,avg  = background_subtraction(
        idata_corrected, err_corrected, qdata, sample_name, averaging, **kwargs
    )

    return Qdata, Idata, Err, sname,bck_coef,avg 

