import os
import numpy as np

def save_1D_data (path, sname, Qdata, Idata, Err):
    """Function that saves the data in a folder "1D" at your path.

    Parameters: 'path' where your data are stored,
                'sname, Qdata, Idata, Err' data processed in the process data function"""

    # Create the "1D" folder if it doesn't exist
    path_out_folder = os.path.join(path, '1D')
    os.makedirs(path_out_folder, exist_ok=True)

    for i in range(len(sname)):
        substring = sname[i]
        path_out = os.path.join(path_out_folder, f'{substring}_1D.txt')

        arr = np.column_stack((Qdata[i], Idata[i], Err[i]))

        np.savetxt(path_out, arr, delimiter=',')

    print(f'1D data have been saved at: {path_out_folder}')
       
def save_1D_average_data(path,sname,Qdata,Idata,Err):
    path_out_folder = os.path.join(path, 'Averaged_Data')
    os.makedirs(path_out_folder, exist_ok=True)   
    for i in range(len(sname)):
        substring = sname[i]
        path_out = os.path.join(path_out_folder, f'{substring}Averaged_Data_1D.txt')
        arr = np.column_stack((Qdata[i], Idata[i], Err[i]))
        np.savetxt(path_out, arr, delimiter=',') 
    print(f'Averaged data have been saved at: {path_out_folder}')    