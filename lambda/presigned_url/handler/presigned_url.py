import boto3
from botocore.exceptions import ClientError
import os
import random
import uuid


def create_presigned_url_put(expiry=3600, is_public=True, user=None):
    client = boto3.client("s3")

    try:
        if is_public:
            response = client.generate_presigned_url('put_object',
                Params={
                    'Bucket': os.getenv("S3_IMAGE_BUCKET_NAME"),
                    'Key': 'public/' + str(uuid.uuid1()),
                    'ContentType': 'image/jpeg'
                },
                ExpiresIn=expiry
            )
        else:
            print(user)
            response = client.generate_presigned_url('put_object',
                Params={
                    'Bucket': os.getenv("S3_IMAGE_BUCKET_NAME"),
                    'Key': 'private/' + user + '/' + str(uuid.uuid1()),
                    'ContentType': 'image/jpeg'
                },
                ExpiresIn=expiry
            )
    except ClientError as e:
        return None

    return response


def create_presigned_url_get(key, expiry=3600):
    client = boto3.client("s3")

    try:
        response = client.generate_presigned_url('get_object',
            Params={
                'Bucket': os.getenv("S3_PROCESSED_IMAGE_BUCKET_NAME"),
                'Key': key,
            },
            ExpiresIn=expiry
        )
    except ClientError as e:
        return None

    return response


def create_multiple_presigned_urls(list_response_obj):
    key_list = []
    for content in list_response_obj['Contents']:
        key_list.append(content['Key'])

    url_list = []
    for key in key_list:
        new_url = create_presigned_url_get(key)
        url_list.append(new_url)

    return url_list


def get_s3_image_list(is_public=True, user=None):
    client = boto3.client("s3")

    if is_public:
        bucket_prefix = "public/"
    else:
        bucket_prefix = "private/" + user + "/"
    max_images = 20
    bucket_name = os.getenv("S3_PROCESSED_IMAGE_BUCKET_NAME")

    response = client.list_objects_v2(
        Bucket=bucket_name,
        MaxKeys=max_images,
        Prefix=bucket_prefix
    )

    return response
