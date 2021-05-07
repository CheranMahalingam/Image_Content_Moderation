import boto3
import base64
import os
from PIL import Image
from io import BytesIO
from censor import blur_text


def moderate_image(event):
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
    client = boto3.client('s3')
    file_byte_string = client.get_object(Bucket=bucket_name, Key=key)['Body'].read()
    print(file_byte_string)
    image = Image.open(BytesIO(file_byte_string))
    b = BytesIO()
    image.save(b, format='JPEG')
    return b


def update_s3_object(key, byte_data):
    client = boto3.client('s3')

    response = client.put_object(Body=byte_data.getvalue(), Bucket=os.getenv("S3_PROCESSED_IMAGE_BUCKET_NAME"), Key=key)
    print(response)
