README file for the video_file_converter.py Python script


First, make sure python is installed on your computer
You can check this in the command prompt by typing:
python -V

If it tells you the version (Python X.X.X) you're good to go! Otherwise, install Python from the Software Centre (I am using 3.8.3).

Second, make sure you have IDLE installed on your computer (search IDLE in the Windows Search bar).
Install it from the software centre if necessary.

Third, you need to install the open-cv Python module, which can be done using the command prompt:

pip install -m open-cv

Once that's complete, open the video_file_converter.py script in IDLE (right click on the script, select Edit With > IDLE)
This will open the script in IDLE.

In the script you need to specifiy 2 things:
1. The path to the directory that has the videos you want to convert
2. The path to the directory where you want to save the converted videos

Make sure that the full path is specified, and that there are \\ between each directory (otherwise Python "escapes" the characters and doesn't know where the files are)

Once you've specified the file paths in the script, save it and run it (F5). If there are no issues, the console should print the first file name, and each file name after that until it's finished.

This takes time! When it's finished all of the files, the console will display the >>> symbol indicating it is ready to receive additional instructions (i.e. convert a different directory of videos).

Contact Rylan Command (Rylan.Command@dfo-mpo.gc.ca) if there are any issues.