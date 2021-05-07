import json
from moderate_image import moderate_image


def lambda_handler(event, context):
    print(event)
    moderate_image(event)
    # return {
    #     "statusCode": 200,
    #     'headers': {
    #         'Access-Control-Allow-Headers': 'Content-Type',
    #         'Access-Control-Allow-Origin': 'http://localhost:3000',
    #         'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
    #     },
    #     'body': json.dumps({'response': 'Image was moderated'})
    # }
