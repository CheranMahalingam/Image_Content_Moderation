"""Module testing methods in moderate_image.py"""

import boto3
from moto import mock_s3
import unittest
import os
from PIL import Image
from io import BytesIO
import sys

sys.path.insert(1, '../handler')

BUCKET_NAME = 'test_bucket'
OBJECT_KEY = "test-key"


@mock_s3
class TestModerateImage(unittest.TestCase):
    def setUp(self):
        client = boto3.client(
            's3',
            region_name='us-east-1',
            aws_access_key_id='test',
            aws_secret_access_key='test'
        )
        s3 = boto3.resource(
            's3',
            region_name='us-east-1',
            aws_access_key_id='test',
            aws_secret_access_key='test'
        )
        client.create_bucket(Bucket=BUCKET_NAME)

    def tearDown(self):
        s3 = boto3.resource(
            's3',
            region_name='us-east-1',
            aws_access_key_id='test',
            aws_secret_access_key='test'
        )
        bucket = s3.Bucket(BUCKET_NAME)
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()

    def test_get_image(self):
        # Imported the methods inside the function to avoid creating this AWS resource in reality
        from moderate_image import get_image

        # Initialize s3 client
        client = boto3.client(
            's3',
            region_name='us-east-1',
            aws_access_key_id='test',
            aws_secret_access_key='test'
        )

        # Test getting a processed image from a s3 bucket
        # Save image as raw data
        im = Image.open(r'images/words-quote.jpg')
        b = BytesIO()
        im.save(b, format='JPEG')

        # Push the raw data to an s3 bucket
        client.put_object(Body=b.getvalue(), Bucket=BUCKET_NAME, Key=OBJECT_KEY)

        binary_data = get_image(BUCKET_NAME, OBJECT_KEY)
        # Convert raw data to an image
        fetched_image = Image.open(BytesIO(binary_data.getvalue()))

        # Compare image dimensions to see if image was fetched
        # Could not evaluate date creation or bucket key since the metadata is not
        # returned by get_image()
        self.assertEqual(fetched_image.size, im.size)

    def test_update_s3_object(self):
        # Imported the methods inside the function to avoid creating AWS resources in reality
        from moderate_image import update_s3_object

        # Initialize s3 client
        client = boto3.client(
            's3',
            region_name='us-east-1',
            aws_access_key_id='test',
            aws_secret_access_key='test'
        )

        # Test sending a single processed image to a s3 bucket
        # Save image as raw data
        im = Image.open(r'images/words-quote.jpg')
        b = BytesIO()
        im.save(b, format='JPEG')

        update_s3_object(BUCKET_NAME, OBJECT_KEY, b)

        response = client.list_objects(Bucket=BUCKET_NAME)

        # Ensure there is only 1 object that has been placed in the s3 bucket
        self.assertEqual(len(response['Contents']), 1)
        # Make sure the key of the updated object matches
        self.assertEqual(response['Contents'][0]['Key'], OBJECT_KEY)

        # Test updating s3 bucket with multiple processed images
        # Save new image as raw data
        im = Image.open(r'images/swear.jpg')
        b = BytesIO()
        im.save(b, format='JPEG')

        new_key = 'test-key-2'
        update_s3_object(BUCKET_NAME, new_key, b)

        response = client.list_objects(Bucket=BUCKET_NAME)

        # Ensure there is only 2 object that has been placed in the s3 bucket
        self.assertEqual(len(response['Contents']), 2)
        # Make sure the key of the updated object matches
        self.assertEqual(response['Contents'][0]['Key'], OBJECT_KEY)
        self.assertEqual(response['Contents'][1]['Key'], new_key)


if __name__ == '__main__':
    unittest.main()
