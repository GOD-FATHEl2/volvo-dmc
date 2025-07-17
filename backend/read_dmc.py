# read_dmc.py
from pylibdmtx.pylibdmtx import decode
from PIL import Image
import os

def read_dmc_code(image_path):
    """
    Read DMC code from an image file
    Returns the decoded text or None if no code found
    """
    try:
        # Open and process the image
        img = Image.open(image_path)
        
        # Convert to grayscale if needed
        if img.mode != 'L':
            img = img.convert('L')
        
        # Decode the DMC code
        decoded = decode(img)
        
        if decoded:
            # Return the first decoded result
            return decoded[0].data.decode('utf-8')
        else:
            return None
            
    except Exception as e:
        print(f"Error reading DMC code: {e}")
        return None

def read_dmc_from_bytes(image_bytes):
    """
    Read DMC code from image bytes (for uploaded files)
    Returns the decoded text or None if no code found
    """
    try:
        # Create image from bytes
        img = Image.open(image_bytes)
        
        # Convert to grayscale if needed
        if img.mode != 'L':
            img = img.convert('L')
        
        # Decode the DMC code
        decoded = decode(img)
        
        if decoded:
            # Return the first decoded result
            return decoded[0].data.decode('utf-8')
        else:
            return None
            
    except Exception as e:
        print(f"Error reading DMC code from bytes: {e}")
        return None
