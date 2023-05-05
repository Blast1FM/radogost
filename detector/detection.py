from ultralytics import yolo
import cv2
from pathlib import Path

# Create a VideoCapture object and read from input file
cwd = Path("./radogost/detector/")
vid_list = cwd.glob('*.mp4')

for vid in vid_list:
    capture = cv2.VideoCapture(str(vid))
    # Check if camera opened successfully
    if (capture.isOpened()== False):
        print("Error opening video file")
    # Read until video is completed
    while(capture.isOpened()):
        
    # Capture frame-by-frame
        ret, frame = capture.read()
        if ret == True:
        # Display the resulting frame
            cv2.imshow('Frame', frame)
            
        # Press Q on keyboard to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
    
    # Break the loop
        else:
            break
    
    # When everything done, release
    # the video capture object
    capture.release()
    
    # Closes all the frames
    cv2.destroyAllWindows()