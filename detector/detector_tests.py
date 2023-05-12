import unittest
from unittest.mock import patch, MagicMock
import cv2
from ultralytics import YOLO
from pathlib import Path

class TestYOLO(unittest.TestCase):
    @patch('cv2.VideoCapture')
    def test_video_cannot_be_opened(self, mock_VideoCapture):
        # Расстановка
        mock_VideoCapture.return_value.isOpened.return_value = False
        vid = "non_existing_video.mp4"
        capture = cv2.VideoCapture(vid)
        # Действие и Проверка утверждений
        self.assertFalse(capture.isOpened())

    @patch('cv2.VideoCapture')
    @patch('cv2.imshow')
    @patch('cv2.waitKey')
    def test_video_processing_stops_on_q_key(self, mock_waitKey, mock_imshow, mock_VideoCapture):
        # Расстановка
        mock_VideoCapture.return_value.isOpened.return_value = True
        mock_VideoCapture.return_value.read.return_value = (True, 'frame')
        mock_waitKey.return_value = ord('q')  # симуляция нажатия 'q'
        vid = "existing_video.mp4"
        capture = cv2.VideoCapture(vid)
        model = YOLO("yolov8n.pt")
        # Действие
        while(capture.isOpened()):
            success, frame = capture.read()
            if success == True:
                result = model(frame, verbose=False, classes = [0]) #Обнаружение только людей
                result_plotted = result[0].plot(probs=True, labels=True, masks=True)
                cv2.imshow('lmao', result_plotted)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
        # Проверка утверждений
        mock_waitKey.assert_called_with(25)
        self.assertTrue(mock_waitKey.called)

    @patch('cv2.VideoCapture')
    @patch('cv2.imshow')
    @patch('cv2.waitKey')
    def test_video_processing_stops_at_end_of_video(self, mock_waitKey, mock_imshow, mock_VideoCapture):
        # Расстановка
        mock_VideoCapture.return_value.isOpened.return_value = True
        mock_VideoCapture.return_value.read.return_value = (False, 'frame')  # конец видео
        mock_waitKey.return_value = ord('a')  # симуляция нажатия клавиши, отличной от 'q'
        vid = "existing_video.mp4"
        capture = cv2.VideoCapture(vid)
        model = YOLO("yolov8n.pt")
        # Действие
        while(capture.isOpened()):
            success, frame = capture.read()
            if not success:
                break
            result = model(frame, verbose=False, classes = [0]) #Обнаружение только людей
            result_plotted = result[0].plot(probs=True, labels=True, masks=True)
            cv2.imshow('lmao', cv2.imshow('lmao', result_plotted)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        # Проверка утверждений
        mock_VideoCapture.return_value.read.assert_called()
        self.assertFalse(success)

if name == 'main':
    unittest.main()
