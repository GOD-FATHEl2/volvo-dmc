# read_dmc.py - Pure Python DMC/QR Code Reading
from pyzbar import pyzbar
from PIL import Image
import cv2
import numpy as np
import io

def read_dmc_code(image_path):
    """
    Read DMC/QR code from an image file using pyzbar
    Returns the decoded text or None if no code found
    """
    try:
        # Open and process the image
        img = Image.open(image_path)
        
        # Convert to grayscale if needed
        if img.mode != 'L':
            img = img.convert('L')
        
        # Decode using pyzbar (supports QR codes, Data Matrix, and other formats)
        decoded_objects = pyzbar.decode(img)
        
        if decoded_objects:
            # Return the first decoded result
            return decoded_objects[0].data.decode('utf-8')
        else:
            # Try with OpenCV preprocessing if pyzbar fails
            return read_with_opencv_preprocessing(img)
            
    except Exception as e:
        print(f"Error reading DMC code with pyzbar: {e}")
        # Fallback to OpenCV method
        try:
            return read_with_opencv(image_path)
        except Exception as e2:
            print(f"Error with OpenCV fallback: {e2}")
            return None

def read_dmc_from_bytes(image_data):
    """
    Read DMC/QR code from image bytes (for file uploads and camera captures)
    """
    try:
        # Reset buffer position
        image_data.seek(0)
        
        # Open image from bytes
        img = Image.open(image_data)
        
        # Convert to grayscale if needed
        if img.mode != 'L':
            img = img.convert('L')
        
        # Decode using pyzbar
        decoded_objects = pyzbar.decode(img)
        
        if decoded_objects:
            return decoded_objects[0].data.decode('utf-8')
        else:
            # Try with OpenCV preprocessing
            return read_bytes_with_opencv_preprocessing(image_data)
            
    except Exception as e:
        print(f"Error reading DMC from bytes: {e}")
        return None

def read_with_opencv_preprocessing(pil_image):
    """
    Use OpenCV for image preprocessing before pyzbar decoding
    """
    try:
        # Convert PIL to OpenCV format
        opencv_img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2GRAY)
        
        # Apply various preprocessing techniques
        preprocessed_images = [
            opencv_img,  # Original
            cv2.threshold(opencv_img, 127, 255, cv2.THRESH_BINARY)[1],  # Binary threshold
            cv2.adaptiveThreshold(opencv_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2),  # Adaptive threshold
            cv2.medianBlur(opencv_img, 3),  # Noise reduction
        ]
        
        # Try decoding each preprocessed image
        for processed_img in preprocessed_images:
            # Convert back to PIL for pyzbar
            pil_processed = Image.fromarray(processed_img)
            decoded_objects = pyzbar.decode(pil_processed)
            
            if decoded_objects:
                return decoded_objects[0].data.decode('utf-8')
        
        return None
        
    except Exception as e:
        print(f"Error in OpenCV preprocessing: {e}")
        return None

def read_bytes_with_opencv_preprocessing(image_data):
    """
    OpenCV preprocessing for image bytes
    """
    try:
        # Reset buffer position
        image_data.seek(0)
        
        # Convert bytes to numpy array
        image_array = np.frombuffer(image_data.read(), np.uint8)
        
        # Decode image with OpenCV
        opencv_img = cv2.imdecode(image_array, cv2.IMREAD_GRAYSCALE)
        
        if opencv_img is None:
            return None
        
        # Apply preprocessing and try decoding
        preprocessed_images = [
            opencv_img,
            cv2.threshold(opencv_img, 127, 255, cv2.THRESH_BINARY)[1],
            cv2.adaptiveThreshold(opencv_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2),
            cv2.medianBlur(opencv_img, 3),
        ]
        
        for processed_img in preprocessed_images:
            pil_processed = Image.fromarray(processed_img)
            decoded_objects = pyzbar.decode(pil_processed)
            
            if decoded_objects:
                return decoded_objects[0].data.decode('utf-8')
        
        return None
        
    except Exception as e:
        print(f"Error in OpenCV bytes preprocessing: {e}")
        return None

def read_with_opencv(image_path):
    """
    Fallback method using only OpenCV (if available)
    """
    try:
        # Read image with OpenCV
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        if img is None:
            return None
        
        # Convert to PIL and try pyzbar
        pil_img = Image.fromarray(img)
        decoded_objects = pyzbar.decode(pil_img)
        
        if decoded_objects:
            return decoded_objects[0].data.decode('utf-8')
        
        return None
        
    except Exception as e:
        print(f"Error in OpenCV fallback: {e}")
        return None


