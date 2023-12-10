import cv2
import argparse
from ultralytics import YOLO
import message_producer
import video_server

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
        msg_producer = message_producer.MessageProducer()

        server = video_server.VideoServer()

        prev_obj_id = None
        while True:
            ret, frame = cap.read()
            if (ret):
                #Run inference
                result = model.track(source=frame, agnostic_nms=True, verbose = False, classes = [0], device="cpu",persist=True)
                if result[0]:
                    #Plot results
                    result_plotted = result[0].plot(probs=True, labels=True, masks=True)
                    #Get tracking id tensor
                    object_id = result[0].boxes.id
                    #TODO This won't work in a real scenario as it takes complete match = need to check individual ids,
                    #For which i need to properly convert the tensor

                    #TODO throw this into a separate function maybe lol
                    #Try to check if the object with this id has been in the previous frame
                    #to avoid message spam
                    try:
                        if (object_id != prev_obj_id) & (object_id!=None):
                            #TODO ONLY WORLS FOR SINGLE ELEMENT TENSOR
                            try:
                                #this WILL fail with multiple elements in tensor
                                int_obj_id = object_id.item()
                                #TODO replace print with msg_producer.send_message to detections queue when it works
                                print(({
                                    "type":"appeared",
                                    "id":int_obj_id,
                                    "obj_data":result[0].tojson()
                                    }),
                                "detections")
                                prev_obj_id = object_id
                            except:
                                print("detection event error: not implemented")
                        #case when leaves the frame. Doesn't work 
                        #TODO fix
                        #TODO check what happens when a result is empty (what model.track returns)
                        #Also look into boxes.is_track. Sometimes it detects a person but can't track it,
                        #Boxes.is_track can help (it is a bool)
                        #https://github.com/ultralytics/ultralytics/blob/main/ultralytics/yolo/engine/results.py line 361
                        elif (object_id != prev_obj_id) & (object_id==None):
                            try:
                                #this WILL fail with multiple elements in tensor
                                int_obj_id = object_id.item()
                                print(({
                                    "type":"left",
                                    "id":int_obj_id,
                                    "obj_data":result[0].tojson()
                                    }),
                                "detections")
                                prev_obj_id = object_id
                            except:
                                print("detection event error: not implemented")
                    except RuntimeError:
                        print("logging multiple people is not implemented")
                    cv2.imshow("yolov8", result_plotted)
                else:
                    cv2.imshow("yolov8", frame)
                if (cv2.waitKey(30) == 27):
                    break
            else:
                print("Could not read frame")

detector = Detector()

detector.start_detector()