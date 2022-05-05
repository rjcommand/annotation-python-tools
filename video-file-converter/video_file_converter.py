# Import libraries
import cv2
import os

#### Parameters you need to set (the double \ needs to be added to the path otherwise it gets upset):

# Path to the directory that contains the videos that you want to convert
path_of_the_directory = "D:\\2017-CHONe_DFO_MLB\\HD_Video\\R2035\\Mini_Zeus"

# Path to the directory where you want to save the converted videos
path_of_the_out_directory = "C:\\Users\\COMMANDR\\Documents\\2017_ROPOS_video\\R2035_fixed\\Mini_Zeus"

####


# This function converts the videos to codec H264
def video_to_mp4(input, output, fps: int = 0, frame_size: tuple = (), fourcc: str = "H264"):

    # Create a video capture object that can be used to open the video
    vidcap = cv2.VideoCapture(input)

    # Get the frames per second
    if not fps:
        fps = round(vidcap.get(cv2.CAP_PROP_FPS))

    # Open the video (using the .read method) and get the frame parameters (stored in arr)   
    success, arr = vidcap.read()

    # Get the frame size
    if not frame_size:
        height, width, _ = arr.shape
        frame_size = width, height

    # Define the parameters for the video writer function
    writer = cv2.VideoWriter(
        output,  # the path to the output file
        apiPreference = 0,
        fourcc = cv2.VideoWriter_fourcc(*fourcc),  # the new codec for the output file
        fps = fps,  # the frames per second, retrieved above
        frameSize = frame_size  # the frame size, retrieved above
    )
    
    # Write the video to file as long as there is video to write
    while True:
        if not success:
            break
        writer.write(arr)
        success, arr = vidcap.read()
    # Stop writing and release the new video file
    writer.release()
    # Release (close) the old video file
    vidcap.release()


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
    
