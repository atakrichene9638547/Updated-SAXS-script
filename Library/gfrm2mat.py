def gfrm2mat(path):
    """ Transform Bruker .gfrm format to a matlab matrix plus a header file containing all the informations

    Args:
        path (str): path where your data are stored. 
    """
    import os 
    import matplotlib.pyplot as plt
    from scipy.io import savemat
    files = [filename for filename in os.listdir(path) if filename.endswith('.gfrm')]
    for filenames in files:
        filepath=os.path.join(path,filenames)

        # Run fabio and create the file
        import fabio
        fabio.open(path + filenames)
        image = fabio.open(path + filenames)
        Header_image= image.header

        # Give info that the scrip is running by printing the image
        print(image.data)
        # Save file as matlab file
        # Plot the image
        plt.imshow(image.data)
        
        # Save file
        d={"image":image.data}
        savemat(path +  filenames + ".mat",d)
        savemat(path + 'header_' + filenames + '.mat', Header_image)
        print (f"Data processed and saved at {path}")