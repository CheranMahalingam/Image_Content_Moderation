"""Module to get s3 images and process them"""

import boto3
import base64
import os
from PIL import Image
from io import BytesIO
from censor import blur_text


def moderate_image(event):
    """
    Controller function that gets an image from s3, censors profanity and stores
    the processed image.

    Args:
        event: Dict providing context for the s3 trigger
    """
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    image_name = event['Records'][0]['s3']['object']['key']
    print(image_name)

    image_bytes = get_image(bucket_name, image_name)

    rek = boto3.client("rekognition")
    response = rek.detect_text(Image={'Bytes': image_bytes.getvalue()})
    print(response['TextDetections'])

    censored_image = blur_text(image_bytes, response['TextDetections'])

    update_s3_object(image_name, censored_image)


def get_image(bucket_name, key):
    """
    Gets the binary data of the s3 image that triggered the lambda.

    Args:
        bucket_name: String providing the unique id of the s3 bucket containing unprocessed iamges
        key: String representing the unique id of the s3 object that triggered the lambda

    Returns:
        BytesIO object containing the image's binary data
    """
    client = boto3.client('s3')
    file_byte_string = client.get_object(Bucket=bucket_name, Key=key)['Body'].read()
    image = Image.open(BytesIO(file_byte_string))
    b = BytesIO()
    image.save(b, format='JPEG')
    return b


def update_s3_object(key, byte_data):
    """
    Takes the censored image and stores it in the processed image s3 bucket.

    Args:
        key: String representing the unique id of the s3 object
        byte_data: binary data representing the censored image
    """
    client = boto3.client('s3')

    response = client.put_object(Body=byte_data.getvalue(), Bucket=os.getenv("S3_PROCESSED_IMAGE_BUCKET_NAME"), Key=key)
    print(response)
