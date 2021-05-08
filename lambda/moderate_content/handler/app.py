"""Lambda entrypoint triggered by a put operation on s3 bucket"""

import json
from moderate_image import moderate_image


def lambda_handler(event, context):
    print(event)
    moderate_image(event)
