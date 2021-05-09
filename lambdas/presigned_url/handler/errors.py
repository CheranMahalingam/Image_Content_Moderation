"""Custom exception class declarations"""


class LambdaError(Exception):
    """Base exception class"""

    pass


class BucketObjectError(LambdaError):
    """S3 object does not exist"""
    
    pass


class ResourceNotFoundError(LambdaError):
    """Invalid path error"""

    pass



