# Standard library imports
import cv2

# Define the function
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
        apiPreference=0,
        fourcc=cv2.VideoWriter_fourcc(*fourcc),  # the new codec for the output file
        fps=fps,  # the frames per second, retrieved above
        frameSize=frame_size  # the frame size, retrieved above
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

if __name__ == '__main__':
    video_to_mp4()
