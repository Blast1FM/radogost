import cv2
import argparse
from ultralytics import YOLO
import asyncio

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

    #TODO port detection login onto async framework
    async def run_detection(model):
        pass

    def main(self):
        args = self.parse_arguments()
        frame_width, frame_height = args.webcam_resolution

        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

        model = YOLO("yolov8n.pt")

        while True:
            ret, frame = cap.read()

            result = model(frame, agnostic_nms=True, verbose = False, classes = [0], device="cpu")
            result_plotted = result[0].plot(probs=True, labels=True, masks=True)
            
            cv2.imshow("yolov8", result_plotted)

            if (cv2.waitKey(30) == 27):
                break

detector = Detector()

detector.main()
