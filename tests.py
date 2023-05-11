import unittest
from unittest.mock import patch, MagicMock
from ultralytics import YOLO
import cv2
from pathlib import Path


class TestVideoProcessing(unittest.TestCase):
    @patch('cv2.VideoCapture')
    @patch('cv2.imshow')
    @patch('cv2.destroyAllWindows')
    @patch('cv2.waitKey', return_value=113)  # ASCII for 'q'
    def test_process_video(self, mock_key, mock_destroy, mock_imshow, mock_capture):
        mock_capture.return_value.isOpened.return_value = True
        mock_capture.return_value.read.return_value = (True, 'frame')
        mock_model = MagicMock()
        mock_model.return_value = [MagicMock()]
        mock_model.return_value[0].plot.return_value = 'result_plotted'

        result = process_video(mock_model, 'test_video.mp4')

        self.assertTrue(result)
        mock_capture.assert_called_once_with('test_video.mp4')
        mock_capture.return_value.isOpened.assert_called_once()
        mock_capture.return_value.read.assert_called()
        mock_model.assert_called_with('frame')
        mock_imshow.assert_called_once_with('lmao', 'result_plotted')
        mock_destroy.assert_called_once()
        mock_key.assert_called_once_with(25)


if name == 'main':
    unittest.main()

def process_video(model, video_file):
    capture = cv2.VideoCapture(video_file)
    if (capture.isOpened() == False):
        print("Error opening video file")
        return False

    while (capture.isOpened()):
        ret, frame = capture.read()
        if ret == True:
            result = model(frame)
            result_plotted = result[0].plot()
            cv2.imshow('lmao', result_plotted)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    capture.release()
    cv2.destroyAllWindows()

    return True