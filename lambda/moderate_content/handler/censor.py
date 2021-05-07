from profanity_check import predict_prob
from PIL import Image, ImageFilter
from io import BytesIO


def evaluate_profanity(text):
    score = predict_prob([text])[0]
    print(score, text)
    if score > 0.4:
        return True
    else:
        return False


def blur_text(b, rek_response):
    image = Image.open(b)
    source_size = image.size[0], image.size[1]
    image.seek(0)

    text_list = [word for word in rek_response if word['Confidence'] > 80 and evaluate_profanity(word['DetectedText'])]
    print(text_list)

    for text in get_text_position(text_list, source_size):
        print(text)
        image_copy = image.copy()
        blurred_text = image_copy.crop(text[:4])
        blurred_text = blurred_text.filter(ImageFilter.GaussianBlur(10))
        image.paste(blurred_text, (text[0], text[1]))

    b = BytesIO()
    image.save(b, format="JPEG")
    return b


def get_text_position(text_list, source_size):
    return [
        (
            int(text['Geometry']['BoundingBox']['Left'] * source_size[0]),
            int(text['Geometry']['BoundingBox']['Top'] * source_size[1]),
            int((text['Geometry']['BoundingBox']['Left'] + text['Geometry']['BoundingBox']['Width']) * source_size[0]),
            int((text['Geometry']['BoundingBox']['Top'] + text['Geometry']['BoundingBox']['Height']) * source_size[1])
        )
        for text in text_list
    ]
