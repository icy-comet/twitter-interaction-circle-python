from base64 import b64encode
from io import BytesIO

def encode(img):
    io_data = BytesIO()
    img.save(io_data, 'JPEG')
    encoded_data = b64encode(io_data.getvalue()).decode('ascii')
    return encoded_data