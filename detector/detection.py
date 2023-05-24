import cv2
import argparse
from ultralytics import YOLO
import producer

class Detector():

    def parse_arguments(self) -> argparse.Namespace:
        parser = argparse.ArgumentParser(description="YOLOv8")
        parser.add_argument(
            "--webcam-resolution", 
            default=[1280, 720], 
            nargs=2, 
            type=int
        )
        args = parser.parse_args()
        return args
    
    def setup_capture(self):
        args = self.parse_arguments()
        frame_width, frame_height = args.webcam_resolution

        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

        return cap

    def start_detector(self):
        
        cap = self.setup_capture()

        model = YOLO("yolov8n.pt")

        while True:
            ret, frame = cap.read()
            if (ret):
                result = model(frame, agnostic_nms=True, verbose = False, classes = [0], device="cpu")
                if result[0]:
                    result_plotted = result[0].plot(probs=True, labels=True, masks=True)
                    #print(result[0].tojson())
                    cv2.imshow("yolov8", result_plotted)
                else:
                    cv2.imshow("yolov8", frame)

                if (cv2.waitKey(30) == 27):
                    break
            else:
                print("Could not read frame")

detector = Detector()

detector.start_detector()