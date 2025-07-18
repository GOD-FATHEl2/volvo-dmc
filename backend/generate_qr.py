# generate_qr.py
from pylibdmtx.pylibdmtx import encode
from PIL import Image
import base64
import io

def generate_dmc_code(data, filepath):
    try:
        result = encode(data.encode('utf-8'))
        img = Image.frombytes('RGB', (result.width, result.height), result.pixels)
        img = img.convert("L").resize((38, 38), Image.Resampling.NEAREST)
        img.save(filepath)
        
        # Convert to base64 for frontend
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        base64_string = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return base64_string
    except Exception as e:
        print(f"Error generating DMC: {e}")
        return None
