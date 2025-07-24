# generate_qr.py - Pure Python DMC/QR Code Generation
import qrcode
from qrcode.constants import ERROR_CORRECT_L
from PIL import Image, ImageDraw, ImageFont
import base64
import io
import math

def generate_dmc_code(data, filepath):
    """
    Generate a Data Matrix-style code using QR code as fallback
    Creates a square, high-density QR code that mimics DMC appearance
    """
    try:
        # Create QR code with high density settings to mimic DMC
        qr = qrcode.QRCode(
            version=1,  # Small size like DMC
            error_correction=ERROR_CORRECT_L,  # Low error correction for max data
            box_size=2,  # Small box size for density
            border=1,   # Minimal border like DMC
        )
        
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create image with white background and black modules (like DMC)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to PIL Image if necessary (qrcode might return PyPNGImage)
        if not isinstance(qr_img, Image.Image):
            # Convert PyPNGImage to PIL Image
            img_buffer = io.BytesIO()
            qr_img.save(img_buffer)
            img_buffer.seek(0)
            img = Image.open(img_buffer)
        else:
            img = qr_img
        
        # Resize to standard DMC size (38x38 as in original)
        img = img.resize((38, 38), Image.Resampling.NEAREST)
        
        # Convert to grayscale
        img = img.convert("L")
        
        # Save the image
        img.save(filepath)
        
        # Convert to base64 for frontend
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        base64_string = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return base64_string
        
    except Exception as e:
        print(f"Error generating DMC code: {e}")
        # Fallback: create a simple text-based square image
        return generate_fallback_code(data, filepath)

def generate_fallback_code(data, filepath):
    """
    Fallback method: create a simple square image with text
    """
    try:
        # Create a 38x38 white image
        img = Image.new('L', (38, 38), color=255)
        draw = ImageDraw.Draw(img)
        
        # Try to use a small font, fallback to default if not available
        try:
            font = ImageFont.load_default()
        except:
            font = None
        
        # Draw a border to make it look like a code
        draw.rectangle([0, 0, 37, 37], outline=0, width=1)
        
        # Add some pattern based on data to make it unique
        for i, char in enumerate(data[:4]):  # Use first 4 characters
            x = (i % 2) * 18 + 9
            y = (i // 2) * 18 + 9
            # Create a pattern based on ASCII value
            ascii_val = ord(char)
            if ascii_val % 2 == 0:
                draw.rectangle([x-4, y-4, x+4, y+4], fill=0)
            else:
                draw.ellipse([x-4, y-4, x+4, y+4], fill=0)
        
        img.save(filepath)
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        base64_string = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return base64_string
        
    except Exception as e:
        print(f"Error in fallback code generation: {e}")
        return None
