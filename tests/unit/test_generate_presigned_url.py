"""Module testing methods in presigned_url.py"""

import boto3
from moto import mock_s3
import unittest
from unittest.mock import patch
import os
from PIL import Image
from io import BytesIO
import sys

sys.path.insert(1, '../../lambdas/presigned_url/handler')

BUCKET_NAME = 'test_bucket'


@mock_s3
class TestPresignedUrl(unittest.TestCase):
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
    
    def test_create_presigned_url_put(self):
        # Imported the methods inside the function to avoid creating AWS resources in reality
        from generate_presigned_url import create_presigned_url_put

        # Initialize s3 client
        client = boto3.client(
            's3',
            region_name='us-east-1',
            aws_access_key_id='test',
            aws_secret_access_key='test'
        )

        # Test whether a presigned url is generated to upload an image to the public gallery
        response = create_presigned_url_put(BUCKET_NAME)
    
        self.assertIsInstance(response, str)
        self.assertTrue('https://s3.amazonaws.com/{}'.format(BUCKET_NAME) in response)
        self.assertTrue('AWSAccessKeyId' in response)
        self.assertTrue('Signature' in response)
        self.assertTrue('Expires' in response)

        # Test whether a presigned url is generated to upload an image to the private repository
        user_id = 'test-id'
        response = create_presigned_url_put(BUCKET_NAME, is_public=False, user=user_id)

        self.assertIsInstance(response, str)
        self.assertTrue('https://s3.amazonaws.com/{}'.format(BUCKET_NAME) in response)
        self.assertTrue('AWSAccessKeyId' in response)
        self.assertTrue('Signature' in response)
        self.assertTrue('Expires' in response)


    def test_create_presigned_url_get(self):
        # Imported the methods inside the function to avoid creating AWS resources in reality
        from generate_presigned_url import create_presigned_url_get

        # Initialize s3 client
        client = boto3.client(
            's3',
            region_name='us-east-1',
            aws_access_key_id='test',
            aws_secret_access_key='test'
        )

        # Test whether a presigned url is generated to get a public image
        # Save image as raw data
        im = Image.open(r'../images/words-quote.jpg')
        b = BytesIO()
        im.save(b, format='JPEG')

        object_key = 'public/123'
        client.put_object(Body=b.getvalue(), Bucket=BUCKET_NAME, Key=object_key)

        response = create_presigned_url_get(BUCKET_NAME, object_key)
        self.assertIsInstance(response, str)
        self.assertTrue('https://s3.amazonaws.com/{}/{}'.format(BUCKET_NAME, object_key) in response)
        self.assertTrue('AWSAccessKeyId' in response)
        self.assertTrue('Signature' in response)
        self.assertTrue('Expires' in response)
    
    @patch('generate_presigned_url.create_presigned_url_get')
    def test_create_multiple_presigned_urls(self, mock_create_presigned_url_get):
        # Imported the methods inside the function to avoid creating AWS resources in reality
        from generate_presigned_url import create_multiple_presigned_urls

        # Test whether presigned urls will be generated if there are no s3 objects
        empty_s3_bucket = {}
        response = create_multiple_presigned_urls(empty_s3_bucket)

        self.assertEqual(response, None)

        # Test whether presigned urls will be generated if there is a single s3 object
        mock_create_presigned_url_get.return_value = 'test_uri'
        s3_object_list = {'Contents': [{'Key': 'public/123'}]}
        response = create_multiple_presigned_urls(s3_object_list)

        self.assertEqual(response, ['test_uri'])

        # Test whether mutiple presigned urls will be generate if many s3 objects exist
        s3_object_list = {'Contents': [{'Key': 'public/1'}, {'Key': 'public/2'}, {'Key': 'public/3'}]}
        response = create_multiple_presigned_urls(s3_object_list)

        # create_presigned_url() has been mocked to provided 'test_uri' as a presigned url
        expected_uri_list = ['test_uri' for i in range(3)]
        self.assertEqual(response, expected_uri_list)


    def test_get_s3_image_list(self):
        # Imported the methods inside the function to avoid creating AWS resources in reality
        from generate_presigned_url import get_s3_image_list

        # Initialize s3 client
        client = boto3.client(
            's3',
            region_name='us-east-1',
            aws_access_key_id='test',
            aws_secret_access_key='test'
        )

        # Test whether images are returned when there are no images in the s3 bucket
        response = get_s3_image_list(BUCKET_NAME)

        self.assertEqual(response['KeyCount'], 0)

        # Test whether public images are returned when there is a single image in the s3 bucket
        # Save image as raw data
        im = Image.open(r'../images/words-quote.jpg')
        b = BytesIO()
        im.save(b, format='JPEG')

        public_object_key = "public/test"
        client.put_object(Body=b.getvalue(), Bucket=BUCKET_NAME, Key=public_object_key)

        response = get_s3_image_list(BUCKET_NAME)

        self.assertEqual(response['KeyCount'], 1)

        # Test whether private images are returned when there are multiple images in the s3 bucket
        # Save image as raw data
        im = Image.open(r'../images/swear.jpg')
        b = BytesIO()
        im.save(b, format='JPEG')

        user_id = "test-123"
        for i in range(5):
            # Folder structure for private object is private/{user_id}/{uuid}
            private_object_key = "private/" + user_id + "/" + str(i)
            client.put_object(Body=b.getvalue(), Bucket=BUCKET_NAME, Key=private_object_key)

        # Gets all private images from user "test-123"
        response = get_s3_image_list(BUCKET_NAME, is_public=False, user=user_id)

        self.assertEqual(response['KeyCount'], 5)


if __name__ == '__main__':
    unittest.main()