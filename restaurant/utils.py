import qrcode
from io import BytesIO
from django.core.files import File

def generate_qr_code(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    blob = BytesIO()
    img.save(blob, 'PNG')
    return File(blob, name='qr_code.png')
