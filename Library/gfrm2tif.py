
def gfrm2tif (path): 
    """Convert .gfrm to tif file 

    Args:
        path (str): path with gfrm data
    """
    import os
    import fabio

    # enter input and output file extension
    input_file_extension = 'gfrm'
    output_file_extension = 'tif'

    # insert file dir, or just copy script into file dir
    file_dir = os.getcwd()

    ##### 
    os.chdir(file_dir)
    list_file = [f for f in os.listdir(file_dir) if f.endswith( input_file_extension )]
    l = len(list_file)
    c = 0
    for i in xrange(len(list_file)):
        f = list_file[i]
        FileName = os.path.basename(f).split('.gfrm')[0]
        img = fabio.open(f)
        img = img.convert( output_file_extension )
        img.save(FileName+'.'+ output_file_extension )
        if c==int(l/10):
            c=0
    print ('conversion done')