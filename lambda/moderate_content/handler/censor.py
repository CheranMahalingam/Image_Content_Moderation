"""Contains methods to censor profanity in images"""

from profanity_check import predict_prob
from PIL import Image, ImageFilter
from io import BytesIO


def evaluate_profanity(text):
    """
    Evaluates whether a word is considered inappropriate.

    Args:
        text: String representing a word detected in the image
    
    Returns:
        Boolean representing whether the word was inappropriate and should be censored
    """
    score = predict_prob([text])[0]
    print(score, text)
    # Words with negativity above this threshold are censored
    if score > 0.4:
        return True
    else:
        return False


def blur_text(binary_image, rek_response):
    """
    Uses Gaussian blurs to censor all inappropriate text in an image.

    Args:
        binary_image: BytesIO object representing an image
        rek_response: Dict returned from Amazon Rekognition containing the detected words
            and location of text in image

    Returns:
        BytesIO object representing a censored image
    """
    image = Image.open(binary_image)
    # Get the dimensions of the image (width, height)
    source_size = image.size[0], image.size[1]
    image.seek(0)

    # List of detected words that are considered profane and Amazon Rekognition is confident about its prediction
    text_list = [word for word in rek_response if word['Confidence'] > 80 and evaluate_profanity(word['DetectedText'])]
    print(text_list)

    for text in get_text_position(text_list, source_size):
        print(text)
        image_copy = image.copy()
        blurred_text = image_copy.crop(text[:4])
        blurred_text = blurred_text.filter(ImageFilter.GaussianBlur(10))
        # Creates new image with blurred content
        image.paste(blurred_text, (text[0], text[1]))

    b = BytesIO()
    image.save(b, format="JPEG")
    return b


def get_text_position(text_list, source_size):
    """
    Finds the coordinates of the vertices of a rectangle which covers any inappropriate text.

    Args:
        text_list: List of words detected by Amazon Rekognition
        source_size: List with first value being the image width and the second value
            being the image height

    Returns;
        List of tuples representing the vertices of the bounding box for the word in
        the form (left, bottom, right, top)
    """
    coordinates = [
        (
            int(text['Geometry']['BoundingBox']['Left'] * source_size[0]),
            int(text['Geometry']['BoundingBox']['Top'] * source_size[1]),
            int((text['Geometry']['BoundingBox']['Left'] + text['Geometry']['BoundingBox']['Width']) * source_size[0]),
            int((text['Geometry']['BoundingBox']['Top'] + text['Geometry']['BoundingBox']['Height']) * source_size[1])
        )
        for text in text_list
    ]
    return coordinates
