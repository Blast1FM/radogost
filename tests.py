import unittest
from unittest.mock import patch, MagicMock
from my_module import load_video, run_inference


class TestInference(unittest.TestCase):

    @patch('my_module.YOLO', autospec=True)
    @patch('my_module.cv2', autospec=True)
    def test_run_inference(self, mock_cv2, mock_yolo):
        # Set up mocks
        mock_yolo.side_effect = MagicMock(side_effect=lambda *args, **kw: {'bboxes': [], 'scores': [], 'labels': []})
        mock_capture = MagicMock()

        # Call the function
        run_inference("vid.mp4", mock_capture, mock_yolo)

        # Assert that all the mock functions were called correctly
        mock_cv2.VideoCapture.assert_called_once_with("vid.mp4")
        mock_yolo.assert_called_once_with("yolov8n.pt\")\n
        self.assertEqual(mock_capture.isOpened.call_count, 2)
        mock_capture.read.assert_called()
        mock_yolo.assert_called()

    def test_load_video(self):
        # Call the function
        video = load_video("test_vid.mp4")

        # Check that the returned object is of the correct type
        self.assertIsInstance(video, Path)