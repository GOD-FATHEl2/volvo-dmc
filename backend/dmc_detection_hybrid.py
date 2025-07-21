# dmc_detection_hybrid.py - Hybrid DMC Detection System
# Tries pylibdmtx first (best for DMC), falls back to pyzbar (good for QR)

import os
import sys
from PIL import Image
import io

# Detection priority order
DETECTION_METHODS = []

# Try to import pylibdmtx (best for DMC, but has deployment issues)
try:
    from pylibdmtx import pylibdmtx
    DETECTION_METHODS.append('pylibdmtx')
    print("✅ pylibdmtx available - EXCELLENT DMC detection")
except ImportError as e:
    print(f"⚠️ pylibdmtx not available: {e}")

# Always have pyzbar as backup (good for QR, poor for DMC)
try:
    from pyzbar import pyzbar
    DETECTION_METHODS.append('pyzbar')
    print("✅ pyzbar available - Good QR detection")
except ImportError as e:
    print(f"❌ pyzbar not available: {e}")

# OpenCV for preprocessing
try:
    import cv2
    import numpy as np
    HAS_OPENCV = True
    print("✅ OpenCV available for preprocessing")
except ImportError:
    HAS_OPENCV = False
    print("⚠️ OpenCV not available")

def read_dmc_hybrid(image_data):
    """
    Hybrid DMC/QR detection using the best available library
    Priority: pylibdmtx > pyzbar with preprocessing
    """
    try:
        # Reset buffer position
        image_data.seek(0)
        
        # Open image from bytes
        img = Image.open(image_data)
        print(f"Hybrid detection - Image: {img.size}, mode: {img.mode}")
        
        # Convert RGBA to RGB if needed
        if img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            img = background
            print("Converted RGBA to RGB")
        
        # Try each detection method in priority order
        for method in DETECTION_METHODS:
            print(f"🔍 Trying {method}...")
            
            if method == 'pylibdmtx':
                result = try_pylibdmtx(img)
                if result:
                    return result
                    
            elif method == 'pyzbar':
                result = try_pyzbar_enhanced(img)
                if result:
                    return result
        
        print("❌ No code detected with any hybrid method")
        return None
        
    except Exception as e:
        print(f"Hybrid detection error: {e}")
        return None

def try_pylibdmtx(img):
    """Try pylibdmtx - excellent for DMC codes"""
    try:
        # Convert to grayscale
        if img.mode != 'L':
            img = img.convert('L')
        
        # Convert to numpy array for pylibdmtx
        img_array = np.array(img)
        
        # Decode with pylibdmtx
        codes = pylibdmtx.decode(img_array)
        
        for code in codes:
            result = code.data.decode('utf-8')
            print(f"✅ pylibdmtx SUCCESS: {result}")
            return result
            
        # Try with different preprocessing for pylibdmtx
        if HAS_OPENCV:
            print("  Trying pylibdmtx with preprocessing...")
            
            # Try inverted image
            inverted = 255 - img_array
            codes = pylibdmtx.decode(inverted)
            for code in codes:
                result = code.data.decode('utf-8')
                print(f"✅ pylibdmtx inverted SUCCESS: {result}")
                return result
            
            # Try with different scaling
            for scale in [0.5, 1.5, 2.0]:
                scaled_img = img.resize((int(img.width * scale), int(img.height * scale)), Image.Resampling.LANCZOS)
                scaled_array = np.array(scaled_img.convert('L'))
                codes = pylibdmtx.decode(scaled_array)
                for code in codes:
                    result = code.data.decode('utf-8')
                    print(f"✅ pylibdmtx scale {scale}x SUCCESS: {result}")
                    return result
        
        return None
        
    except Exception as e:
        print(f"pylibdmtx error: {e}")
        return None

def try_pyzbar_enhanced(img):
    """Try pyzbar with enhanced preprocessing - good for QR, poor for DMC"""
    try:
        # Convert to grayscale
        if img.mode != 'L':
            img = img.convert('L')
        
        # First try direct pyzbar
        codes = pyzbar.decode(img)
        for code in codes:
            result = code.data.decode('utf-8')
            print(f"✅ pyzbar direct SUCCESS ({code.type}): {result}")
            return result
        
        # If OpenCV available, try preprocessing
        if HAS_OPENCV:
            img_array = np.array(img)
            
            # Try different preprocessing methods
            methods = [
                ("OTSU", cv2.threshold(img_array, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]),
                ("Inverted", 255 - img_array),
                ("Adaptive", cv2.adaptiveThreshold(img_array, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)),
            ]
            
            for method_name, processed in methods:
                processed_img = Image.fromarray(processed)
                codes = pyzbar.decode(processed_img)
                for code in codes:
                    result = code.data.decode('utf-8')
                    print(f"✅ pyzbar {method_name} SUCCESS ({code.type}): {result}")
                    return result
        
        return None
        
    except Exception as e:
        print(f"pyzbar error: {e}")
        return None

def get_detection_status():
    """Get status of available detection methods"""
    status = {
        'methods': DETECTION_METHODS,
        'has_opencv': HAS_OPENCV,
        'recommended': 'pylibdmtx' if 'pylibdmtx' in DETECTION_METHODS else 'pyzbar'
    }
    return status

if __name__ == "__main__":
    # Test the hybrid detection
    status = get_detection_status()
    print("🔍 Detection Methods Available:", status['methods'])
    print("🎯 Recommended Method:", status['recommended'])
    print("🔧 OpenCV Available:", status['has_opencv'])
