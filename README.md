Python package for IGRA v2

Author: Gopikrishnan G S

Institute : Indian Institute of Technology Kharagpur

www.atmoslabiitkgp.com

www.github.com/gopikrishnangs44

USAGE:

**SEE THE EXAMPLE.ipynb for a detailed description on how to use the data**


From IGRApy import IGRA

IGRA.igra(file_path, stat=['INM0040032'], save=True, save_dir='path_to_the_folder_for_output')

1. file_path: The complete path to which the data is downloaded.
e.g. '/home/user/Desktop/IGRA/temp_00z-mly.txt'

2. stat = []
The station ID's should be written here.
Station ID are available at  https://www.ncei.noaa.gov/pub/data/igra/igra2-station-list.txt

eg: stat=['INM00043003']

3. save = True/None
The data for each station will be saved as individual files.
eg: INM00043003.nc will be the output at the given save_dir 

4. save_dir: The path to the directory where (3) is saved
eg: '/home/user/Desktop/IGRA/'


A graphical representation of the data is available through:

x = IGRA.igra(file_path, stat=['INM0040032'], save=True/None)
IGRA.plot_fig(x)

DATA that can be used in this package:
https://www.ncei.noaa.gov/pub/data/igra/monthly/monthly-por/

FORMAT AND DESCRIPTION OF DATA: https://www.ncei.noaa.gov/pub/data/igra/monthly/igra2-monthly-format.txt
