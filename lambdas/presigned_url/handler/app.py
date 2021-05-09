"""Lambda entrypoint to handle API requests"""

import json
import os

from presigned_url import create_presigned_url_put, create_presigned_url_get, get_s3_image_list, create_multiple_presigned_urls
from errors import BucketObjectError, ResourceNotFoundError

ALLOWED_HEADERS = 'Content-Type'
ALLOWED_ORIGINS = 'http://localhost:3000'
ALLOWED_METHODS = 'GET'

def lambda_handler(event, context):
    try:
        if event['resource'] == '/upload/public':
            response = create_presigned_url_put(os.getenv("S3_IMAGE_BUCKET_NAME"))

        elif event['resource'] == '/upload/private':
            user_id = event['requestContext']['authorizer']['claims']['sub']
            response = create_presigned_url_put(
                os.getenv("S3_IMAGE_BUCKET_NAME"),
                is_public=False,
                user=user_id
            )

        elif event['resource'] == '/view-image/public':
            image_list = get_s3_image_list(os.getenv("S3_PROCESSED_IMAGE_BUCKET_NAME"))
            if image_list:
                response = create_multiple_presigned_urls(image_list)
            else:
                raise BucketObjectError('No data in bucket')

        elif event['resource'] == '/view-image/private':
            user_id = event['requestContext']['authorizer']['claims']['sub']
            image_list = get_s3_image_list(
                os.getenv("S3_PROCESSED_IMAGE_BUCKET_NAME"),
                is_public=False,
                user=user_id
            )
            if image_list:
                response = create_multiple_presigned_urls(image_list)
            else:
                raise BucketObjectError('No data in bucket')

        else:
            raise ResourceNotFoundError("Invalid Route")
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': ALLOWED_HEADERS,
                'Access-Control-Allow-Origin': ALLOWED_ORIGINS,
                'Access-Control-Allow-Methods': ALLOWED_METHODS
            },
            'body': json.dumps({'response': response})
        }

    except BucketObjectError as e:
        return {
            'statusCode': 400,
            'body': json.dumps('Error in processing request: {}'.format(e))
        }

    except ResourceNotFoundError as e:
        return {
            'statusCode': 404,
            'body': json.dumps('Error in processing request: {}'.format(e))
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps('Error in processing request: {}'.format(e))
        }
