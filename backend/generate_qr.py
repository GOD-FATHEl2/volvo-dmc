# generate_qr.py
from pylibdmtx.pylibdmtx import encode
from PIL import Image

def generate_dmc_code(data, filepath):
    try:
        result = encode(data.encode('utf-8'))
        img = Image.frombytes('RGB', (result.width, result.height), result.pixels)
        img = img.convert("L").resize((38, 38), Image.NEAREST)
        img.save(filepath)
    except Exception as e:
        print(f"Error generating DMC: {e}")
