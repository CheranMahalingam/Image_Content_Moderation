"""
Methods generating presigned urls to provide users with temporary credentials
to access images. Also reduces traffic by allowing browser to directly communicate
with s3 buckets.
"""

import boto3
from botocore.exceptions import ClientError
import os
import random
import uuid


def create_presigned_url_put(bucket, expiry=3600, is_public=True, user=None):
    """
    Generates a presigned url allowing users to temporarily upload an image to a s3 bucket.

    Args:
        expiry: Integer respresenting seconds before the presigned url expires
        is_public: Boolean for whether the object should be publicly accessible or private
        user: String representing the autheticated user's id, used for storing a private object

    Returns:
        String representing the presigned url
    """
    client = boto3.client("s3")

    try:
        if is_public:
            response = client.generate_presigned_url('put_object',
                Params={
                    'Bucket': bucket,
                    'Key': 'public/' + str(uuid.uuid1()),
                    'ContentType': 'image/jpeg'
                },
                ExpiresIn=expiry
            )
        else:
            response = client.generate_presigned_url('put_object',
                Params={
                    'Bucket': bucket,
                    'Key': 'private/' + user + '/' + str(uuid.uuid1()),
                    'ContentType': 'image/jpeg'
                },
                ExpiresIn=expiry
            )
    except ClientError as e:
        return None

    return response


def create_presigned_url_get(bucket, key, expiry=3600):
    """
    Generates a presigned url allowing users to temporarily get an image from a s3 bucket.

    Args:
        key: String of a unique id of the s3 object that needs to be fetched
        expiry: Integer respresenting seconds before the presigned url expires

    Returns:
        String representing the presigned url
    """
    client = boto3.client("s3")

    try:
        response = client.generate_presigned_url('get_object',
            Params={
                'Bucket': bucket,
                'Key': key,
            },
            ExpiresIn=expiry
        )
    except ClientError as e:
        return None

    return response


def create_multiple_presigned_urls(list_response_obj):
    """
    Used when getting multiple images from an s3 bucket. Creates a unique presigned url
    for each image.

    Args:
        list_response_obj: List made up of Dicts which contain the key

    Returns;
        List of presigned urls used to get multiple images 
    """
    key_list = []
    # Indicates that the folder did not exist or there are no images in the folder
    if 'Contents' not in list_response_obj:
        return None

    for content in list_response_obj['Contents']:
        key_list.append(content['Key'])

    url_list = []
    for key in key_list:
        new_url = create_presigned_url_get(os.getenv("S3_PROCESSED_IMAGE_BUCKET_NAME"), key)
        url_list.append(new_url)

    return url_list


def get_s3_image_list(bucket_name, is_public=True, user=None):
    """
    Gets a list of the ids for processed images from the s3 bucket.

    Args:
        is_public: Boolean representing whether to find public images or private images
        user: Optional string representing the user id when finding the folder containing a
            user's private images
    
    Returns:
        List of dicts containing information about the s3 bucket and the individual s3 objects
    """
    client = boto3.client("s3")

    if is_public:
        bucket_prefix = "public/"
    else:
        # Folder structure for private objects is private/userid/uuid to easily get images
        bucket_prefix = "private/" + user + "/"
    max_images = 20

    response = client.list_objects_v2(
        Bucket=bucket_name,
        MaxKeys=max_images,
        Prefix=bucket_prefix
    )

    return response
