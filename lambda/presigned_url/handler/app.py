import json
from presigned_url import create_presigned_url_put, create_presigned_url_get, get_s3_image_list, create_multiple_presigned_urls


def lambda_handler(event, context):
    print(event)
    response = None
    if event['resource'] == '/upload/public':
        print("public")
        response = create_presigned_url_put()
    elif event['resource'] == '/upload/private':
        print("private")
        user_id = event['requestContext']['authorizer']['claims']['sub']
        response = create_presigned_url_put(
            is_public=False,
            user=user_id
        )
    elif event['resource'] == '/view-image/public':
        image_list = get_s3_image_list()
        response = create_multiple_presigned_urls(image_list)
    elif event['resource'] == '/view-image/private':
        user_id = event['requestContext']['authorizer']['claims']['sub']
        image_list = get_s3_image_list(
            is_public=False,
            user=user_id
        )
        response = create_multiple_presigned_urls(image_list)
    print(response)
    return {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Methods': 'POST,GET'
        },
        'body': json.dumps({'response': response})
    }
