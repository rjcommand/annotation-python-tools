import cv2
import os
import argparse

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-vd", "--video-directory", help = "path to the to-be-converted video directory")
ap.add_argument("-cd", "--converted-directory", help = "path to where you want to save the converted videos")
args = vars(ap.parse_args())

# This function converts the videos to codec H264
def video_to_mp4(input, output, fps: int = 0, frame_size: tuple = (), fourcc: str = "avc1"):
    vidcap = cv2.VideoCapture(input)
    if not fps:
        fps = round(vidcap.get(cv2.CAP_PROP_FPS))
    success, arr = vidcap.read()
    if not frame_size:
        height, width, _ = arr.shape
        frame_size = width, height
    writer = cv2.VideoWriter(
        output,
        apiPreference=0,
        fourcc=cv2.VideoWriter_fourcc(*fourcc),
        fps=fps,
        frameSize=frame_size
    )
    while True:
        if not success:
            break
        writer.write(arr)
        success, arr = vidcap.read()
    writer.release()
    vidcap.release()

# Path to the directory that contains the videos that you want to convert
path_of_the_directory = args["video_directory"]  # e.g. "C:\\Users\\COMMANDR\\Documents\\2017_ROPOS_video\\R2035"
# Path to the directory where you want to save the converted videos
path_of_the_out_directory = args["converted_directory"]  # e.g. "C:\\Users\\COMMANDR\\Documents\\2017_ROPOS_video\\R2035_fixed"

# Set the codec to H264
fourcc = cv2.VideoWriter_fourcc(*"H264")

# Print a header
print("Files and directories in a specified path:")

# For each file in the list of files in the directory you want to convert
for filename in os.listdir(path_of_the_directory):

    # Get the full path to the file
    f = os.path.join(path_of_the_directory, filename)

    # Create a path name for the "converted" directory
    f_out = os.path.join(path_of_the_out_directory, filename)

    # Get the path name without the extension at the end of the filename
    f_out_pathname, f_out_extension = os.path.splitext(f_out)

    # Check if the end of the path is a file
    if os.path.isfile(f):
        
        # If it is, print the name of the "converted" video file
        print(f_out_pathname + ".mp4")

        # Convert and save the video file using the above function
        video_to_mp4(f, f_out_pathname + ".mp4")
    
