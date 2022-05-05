import os

directory = 'C:\\Users\\COMMANDR\\Documents\\2017_ROPOS_video\\R2035'

[os.rename(os.path.join(directory, f), os.path.join(directory, f).replace(' ', '_')) for f in os.listdir(directory)]
