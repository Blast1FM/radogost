import unittest
from unittest.mock import patch, MagicMock
import cv2
from ultralytics import YOLO
from pathlib import Path

class TestYOLO(unittest.TestCase):
    @patch('cv2.VideoCapture')
    @patch('cv2.imshow')
    @patch('cv2.waitKey')
    def test_video_processing(self, mock_waitKey, mock_imshow, mock_VideoCapture):
        # Расстановка
        model = YOLO("yolov8n.pt")
        cwd = Path("./radogost/detector/sample_vids")
        vid_list = cwd.glob('*.mp4')
        mock_VideoCapture.return_value.isOpened.return_value = True
        mock_VideoCapture.return_value.read.return_value = (True, 'frame')
        mock_waitKey.return_value = ord('a')  # симуляция нажатия клавиши, отличной от 'q'

        # Действие
        for vid in vid_list:
            capture = cv2.VideoCapture(str(vid))
            while(capture.isOpened()):
                success, frame = capture.read()
                if success == True:
                    result = model(frame, verbose=False, classes = [0]) #Обнаружение только людей
                    result_plotted = result[0].plot(probs=True, labels=True, masks=True)
                    cv2.imshow('lmao', result_plotted)
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        break
                else:
                    break
            capture.release()
        cv2.destroyAllWindows()

        # Проверка утверждений
        mock_VideoCapture.assert_called()
        mock_imshow.assert_called_with('lmao', 'frame')
        mock_waitKey.assert_called_with(25)

if name == 'main':
    unittest.main()