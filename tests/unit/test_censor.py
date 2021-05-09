"""Module testing methods in censor.py"""

import boto3
import unittest
from unittest.mock import patch
from PIL import Image
from io import BytesIO, StringIO
import sys

sys.path.insert(1, '../../lambdas/moderate_content/handler')

from censor import evaluate_profanity, blur_text


class TestCensor(unittest.TestCase):

    @patch('censor.get_profanity_score')
    def test_evaluate_profanity(self, mock_get_profanity_score):
        # Test whether it does not detect inappropriate text when predict_prob < 0.4
        mock_get_profanity_score.return_value = 0.15
        low_profanity_word = 'test'
        is_profanity = evaluate_profanity(low_profanity_word)
        self.assertFalse(is_profanity)

        # Test whether it detects inappropriate text when predict_prob > 0.4
        mock_get_profanity_score.return_value = 0.41
        high_profanity_word = 'test'
        is_profanity = evaluate_profanity(high_profanity_word)
        self.assertTrue(is_profanity)

        # Test whether it does not detect inappropriate text when predict_prob = 0.4
        mock_get_profanity_score.return_value = 0.40
        medium_profanity_word = 'test'
        is_profanity = evaluate_profanity(medium_profanity_word)
        self.assertFalse(is_profanity)

    @patch('censor.get_text_position')
    @patch('censor.get_profanity_score')
    def test_blur_text(self, mock_get_profanity_score, mock_get_text_position):
        # Test whether image remains the same if no inappropriate text is detected
        test_rek_response = [{'DetectedText': 'test', 'Confidence': 95}]
        mock_get_profanity_score.return_value = 0.15
        mock_get_text_position.return_value = []

        # Save image as raw data
        im = Image.open(r'../images/words-quote.jpg')
        b = BytesIO()
        im.save(b, format='JPEG')

        blurred_image_bytes = blur_text(b, test_rek_response)

        # Pillow has unknown behaviour causing some bytes to be lost when saving so
        # the saving from the blur_text method is copied here to make the raw data the same
        get_image = Image.open(b)
        binary_data = BytesIO()
        get_image.save(binary_data, format='JPEG')

        # Check that the byte strings match
        self.assertEqual(binary_data.getvalue(), blurred_image_bytes.getvalue())

        # Test whether image byte are modified when profanity is detected
        # High profanity score will cause it to blur the profane text
        mock_get_profanity_score.return_value = 0.85
        # Provide fake bounding box to blur
        mock_get_text_position.return_value = [(0, 0, 10, 10)]

        blurred_image_bytes = blur_text(b, test_rek_response)

        # Blurred image will have different bytes from original image
        self.assertNotEqual(binary_data.getvalue(), blurred_image_bytes.getvalue())


if __name__ == '__main__':
    unittest.main()
