# read_dmc.py - Pure Python DMC/QR Code Reading with multiple libraries
from pyzbar import pyzbar
from PIL import Image
import cv2
import numpy as np
import io

# Try to import additional DMC libraries
try:
    import datamatrix
    HAS_DATAMATRIX = True
    print("✅ python-datamatrix library available")
except ImportError:
    HAS_DATAMATRIX = False
    print("⚠️ python-datamatrix library not available")

try:
    from pydmtx import DataMatrix
    HAS_PYDMTX = True
    print("✅ pydmtx library available")
except ImportError:
    HAS_PYDMTX = False
    print("⚠️ pydmtx library not available")

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

def try_alternative_dmc_libraries(img):
    """
    Try alternative DMC libraries if available
    """
    results = []
    
    # Try python-datamatrix library
    if HAS_DATAMATRIX:
        try:
            print("🔍 Trying python-datamatrix library...")
            # Convert PIL to numpy array
            img_array = np.array(img)
            
            # Try datamatrix decoding
            codes = datamatrix.decode(img_array)
            for code in codes:
                result = code.data.decode('utf-8')
                print(f"✅ python-datamatrix SUCCESS: {result}")
                return result
        except Exception as e:
            print(f"python-datamatrix failed: {e}")
    
    # Try pydmtx library
    if HAS_PYDMTX:
        try:
            print("🔍 Trying pydmtx library...")
            # Convert PIL to bytes
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            dm = DataMatrix()
            result = dm.decode(img_bytes.read())
            if result:
                print(f"✅ pydmtx SUCCESS: {result}")
                return result
        except Exception as e:
            print(f"pydmtx failed: {e}")
    
    return None

def read_dmc_from_bytes(image_data):
    """
    Read DMC/QR code from image bytes (for file uploads and camera captures)
    Enhanced with better preprocessing for camera images
    """
    try:
        # Reset buffer position
        image_data.seek(0)
        
        # Open image from bytes
        img = Image.open(image_data)
        print(f"Original image size: {img.size}, mode: {img.mode}")
        
        # Convert RGBA to RGB first if needed, then to grayscale
        if img.mode == 'RGBA':
            # Create white background for transparency
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])  # Use alpha channel as mask
            img = background
            print("Converted RGBA to RGB")
        
        # Convert to grayscale if needed
        if img.mode != 'L':
            img = img.convert('L')
            print("Converted to grayscale")
        
        # Try multiple detection strategies - start with the most basic
        print("🔍 Starting DMC detection...")
        
        # First try original image with all supported formats
        print("Trying original image with all pyzbar formats...")
        print(f"Image details: size={img.size}, mode={img.mode}")
        
        # Save a diagnostic image to see what we're working with
        try:
            debug_path = "debug_camera_image.png"
            img.save(debug_path)
            print(f"💾 Saved debug image to {debug_path}")
        except Exception as e:
            print(f"Could not save debug image: {e}")
        
        decoded_objects = pyzbar.decode(img)
        
        if decoded_objects:
            for obj in decoded_objects:
                print(f"✅ Found {obj.type} code: {obj.data.decode('utf-8')}")
                return obj.data.decode('utf-8')
        
        # Try more aggressive scaling for DMC - they often need different sizes
        print("📏 Trying multiple scales for DMC detection...")
        scale_strategies = [
            ("2x larger", img.resize((img.width * 2, img.height * 2), Image.Resampling.LANCZOS)),
            ("1.5x larger", img.resize((int(img.width * 1.5), int(img.height * 1.5)), Image.Resampling.LANCZOS)),
            ("Original size", img),
            ("0.7x smaller", img.resize((int(img.width * 0.7), int(img.height * 0.7)), Image.Resampling.LANCZOS)),
            ("0.5x smaller", img.resize((int(img.width * 0.5), int(img.height * 0.5)), Image.Resampling.LANCZOS))
        ]
        
        for scale_name, scaled_img in scale_strategies:
            print(f"Trying scale: {scale_name} ({scaled_img.size})...")
            
            # For each scale, try different processing
            dmc_strategies = [
                ("Direct", scaled_img),
                ("Inverted", Image.eval(scaled_img, lambda x: 255 - x)),
                ("Enhanced contrast", enhance_contrast(scaled_img)),
                ("Light contrast", enhance_contrast_light(scaled_img))
            ]
            
            for strategy_name, processed_img in dmc_strategies:
                print(f"  -> {scale_name} + {strategy_name}...")
                
                # Try pyzbar detection
                decoded_objects = pyzbar.decode(processed_img)
                
                if decoded_objects:
                    for obj in decoded_objects:
                        result = obj.data.decode('utf-8')
                        print(f"✅ DMC SUCCESS with {scale_name} + {strategy_name} ({obj.type}): {result}")
                        return result
        
        # Only try OpenCV preprocessing as a last resort if all simple strategies fail
        print("🔧 Trying OpenCV preprocessing as last resort for DMC...")
        result = read_with_opencv_preprocessing_for_dmc(img)
        if result:
            print(f"✅ SUCCESS with OpenCV DMC preprocessing: {result}")
            return result
        
        # Try alternative DMC libraries before giving up
        print("🔧 Trying alternative DMC libraries...")
        result = try_alternative_dmc_libraries(img)
        if result:
            print(f"✅ SUCCESS with alternative DMC library: {result}")
            return result
        
        print("❌ No DMC code detected with any strategy")
        return None
            
    except Exception as e:
        print(f"Error reading DMC from bytes: {e}")
        import traceback
        traceback.print_exc()
        return None

def enhance_contrast(img):
    """
    Enhance image contrast for better code detection
    """
    try:
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(img)
        return enhancer.enhance(2.0)  # Increase contrast
    except Exception as e:
        print(f"Contrast enhancement failed: {e}")
        return img

def enhance_contrast_light(img):
    """
    Very light contrast enhancement to preserve original structure
    """
    try:
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(img)
        return enhancer.enhance(1.3)  # Just slightly increase contrast
    except Exception as e:
        print(f"Light contrast enhancement failed: {e}")
        return img

def preprocess_for_dmc(img):
    """
    Specialized preprocessing for DMC codes
    """
    try:
        # Convert PIL to OpenCV format - handle different image modes properly
        img_array = np.array(img)
        
        if len(img_array.shape) == 3:
            # Color image - convert to grayscale
            if img_array.shape[2] == 3:  # RGB
                opencv_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            elif img_array.shape[2] == 4:  # RGBA
                opencv_img = cv2.cvtColor(img_array, cv2.COLOR_RGBA2GRAY)
            else:
                opencv_img = img_array[:, :, 0]  # Take first channel
        else:
            # Already grayscale
            opencv_img = img_array
        
        print(f"OpenCV preprocessing: Input shape {img_array.shape}, Output shape {opencv_img.shape}")
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(opencv_img, (3, 3), 0)
        
        # Apply adaptive threshold
        adaptive = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
        # Apply morphological operations to clean up
        kernel = np.ones((2,2), np.uint8)
        cleaned = cv2.morphologyEx(adaptive, cv2.MORPH_CLOSE, kernel)
        
        # Convert back to PIL
        return Image.fromarray(cleaned)
        
    except Exception as e:
        print(f"DMC preprocessing failed: {e}")
        import traceback
        traceback.print_exc()
        return img

def read_with_opencv_preprocessing_for_dmc(pil_image):
    """
    OpenCV preprocessing specifically optimized for Data Matrix Code (DMC) detection
    """
    try:
        # Convert PIL to OpenCV format - handle different image modes
        img_array = np.array(pil_image)
        
        if len(img_array.shape) == 3:
            # Color image - convert to grayscale
            if img_array.shape[2] == 3:  # RGB
                opencv_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            elif img_array.shape[2] == 4:  # RGBA
                opencv_img = cv2.cvtColor(img_array, cv2.COLOR_RGBA2GRAY)
            else:
                opencv_img = img_array[:, :, 0]  # Take first channel
        else:
            # Already grayscale
            opencv_img = img_array
        
        # DMC-specific preprocessing techniques - try even more aggressive methods
        dmc_preprocessed_images = [
            ("Original OpenCV", opencv_img),
            ("Binary threshold 127", cv2.threshold(opencv_img, 127, 255, cv2.THRESH_BINARY)[1]),
            ("Binary threshold 100", cv2.threshold(opencv_img, 100, 255, cv2.THRESH_BINARY)[1]),
            ("Binary threshold 150", cv2.threshold(opencv_img, 150, 255, cv2.THRESH_BINARY)[1]),
            ("Binary threshold 80", cv2.threshold(opencv_img, 80, 255, cv2.THRESH_BINARY)[1]),
            ("Binary threshold 200", cv2.threshold(opencv_img, 200, 255, cv2.THRESH_BINARY)[1]),
            ("Inverted binary", cv2.threshold(opencv_img, 127, 255, cv2.THRESH_BINARY_INV)[1]),
            ("Inverted binary 100", cv2.threshold(opencv_img, 100, 255, cv2.THRESH_BINARY_INV)[1]),
            ("Inverted binary 150", cv2.threshold(opencv_img, 150, 255, cv2.THRESH_BINARY_INV)[1]),
            ("OTSU threshold", cv2.threshold(opencv_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]),
            ("OTSU inverted", cv2.threshold(opencv_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]),
            ("Adaptive threshold mean", cv2.adaptiveThreshold(opencv_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)),
            ("Adaptive threshold gaussian", cv2.adaptiveThreshold(opencv_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)),
            ("Slight blur + threshold", cv2.threshold(cv2.GaussianBlur(opencv_img, (3, 3), 0), 127, 255, cv2.THRESH_BINARY)[1]),
            ("Heavy blur + threshold", cv2.threshold(cv2.GaussianBlur(opencv_img, (5, 5), 0), 127, 255, cv2.THRESH_BINARY)[1]),
            ("Median filter + threshold", cv2.threshold(cv2.medianBlur(opencv_img, 5), 127, 255, cv2.THRESH_BINARY)[1]),
            ("Morphology close + threshold", cv2.threshold(cv2.morphologyEx(opencv_img, cv2.MORPH_CLOSE, np.ones((3,3), np.uint8)), 127, 255, cv2.THRESH_BINARY)[1]),
            ("Morphology open + threshold", cv2.threshold(cv2.morphologyEx(opencv_img, cv2.MORPH_OPEN, np.ones((2,2), np.uint8)), 127, 255, cv2.THRESH_BINARY)[1])
        ]
        
        # Try decoding each preprocessed image with more diagnostics
        for name, processed_img in dmc_preprocessed_images:
            print(f"  🔍 Trying DMC OpenCV: {name}")
            
            # Save debug image for this strategy (optional - only save a few to avoid clutter)
            if "OTSU" in name or "Adaptive" in name:
                try:
                    debug_path = f"debug_{name.replace(' ', '_').lower()}.png"
                    Image.fromarray(processed_img).save(debug_path)
                    print(f"    💾 Saved {debug_path}")
                except:
                    pass
            
            # Convert back to PIL for pyzbar
            pil_processed = Image.fromarray(processed_img)
            decoded_objects = pyzbar.decode(pil_processed)
            
            if decoded_objects:
                for obj in decoded_objects:
                    print(f"  ✅ DMC OpenCV success with {name} ({obj.type})")
                    return obj.data.decode('utf-8')
            
            # Also check if pyzbar found ANY patterns (even if not decodable)
            try:
                # This might give us more info about what pyzbar is seeing
                symbols = pyzbar.decode(pil_processed)
                if hasattr(pyzbar, 'ZBarSymbol'):
                    print(f"    📊 Found {len(symbols)} symbols with {name}")
            except:
                pass
        
        # If no symbols found anywhere, try cropping to different regions
        print("🔍 Trying region-based detection (DMC might be in a specific area)...")
        h, w = opencv_img.shape
        
        # Try different crops/regions
        regions = [
            ("Center region", opencv_img[h//4:3*h//4, w//4:3*w//4]),
            ("Top half", opencv_img[0:h//2, :]),
            ("Bottom half", opencv_img[h//2:, :]),
            ("Left half", opencv_img[:, 0:w//2]),
            ("Right half", opencv_img[:, w//2:]),
            ("Top-left quadrant", opencv_img[0:h//2, 0:w//2]),
            ("Top-right quadrant", opencv_img[0:h//2, w//2:]),
            ("Bottom-left quadrant", opencv_img[h//2:, 0:w//2]),
            ("Bottom-right quadrant", opencv_img[h//2:, w//2:])
        ]
        
        for region_name, region_img in regions:
            if region_img.size == 0:  # Skip empty regions
                continue
                
            print(f"  🔍 Trying region: {region_name} ({region_img.shape})")
            
            # Apply basic processing to each region
            region_strategies = [
                ("Direct", region_img),
                ("OTSU", cv2.threshold(region_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]),
                ("Adaptive", cv2.adaptiveThreshold(region_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2) if min(region_img.shape) > 11 else region_img)
            ]
            
            for strategy_name, processed_region in region_strategies:
                if processed_region.size == 0:
                    continue
                    
                try:
                    pil_region = Image.fromarray(processed_region)
                    decoded_objects = pyzbar.decode(pil_region)
                    
                    if decoded_objects:
                        for obj in decoded_objects:
                            print(f"  ✅ REGION SUCCESS: {region_name} + {strategy_name} ({obj.type})")
                            return obj.data.decode('utf-8')
                    else:
                        print(f"    → {region_name} + {strategy_name}: 0 symbols")
                except Exception as e:
                    print(f"    → {region_name} + {strategy_name}: Error {e}")
        
        return None
        
    except Exception as e:
        print(f"Error in DMC OpenCV preprocessing: {e}")
        import traceback
        traceback.print_exc()
        return None

def read_with_opencv_preprocessing(pil_image):
    """
    Use OpenCV for image preprocessing before pyzbar decoding
    """
    try:
        # Convert PIL to OpenCV format - handle different image modes
        img_array = np.array(pil_image)
        
        if len(img_array.shape) == 3:
            # Color image - convert to grayscale
            if img_array.shape[2] == 3:  # RGB
                opencv_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            elif img_array.shape[2] == 4:  # RGBA
                opencv_img = cv2.cvtColor(img_array, cv2.COLOR_RGBA2GRAY)
            else:
                opencv_img = img_array[:, :, 0]  # Take first channel
        else:
            # Already grayscale
            opencv_img = img_array
        
        # Apply very light preprocessing techniques - keep it simple
        preprocessed_images = [
            ("Original OpenCV", opencv_img),
            ("Light blur", cv2.GaussianBlur(opencv_img, (3, 3), 0)),
            ("Simple threshold", cv2.threshold(opencv_img, 128, 255, cv2.THRESH_BINARY)[1])
        ]
        
        # Try decoding each preprocessed image
        for name, processed_img in preprocessed_images:
            # Convert back to PIL for pyzbar
            pil_processed = Image.fromarray(processed_img)
            decoded_objects = pyzbar.decode(pil_processed)
            
            if decoded_objects:
                print(f"✅ OpenCV success with {name}")
                return decoded_objects[0].data.decode('utf-8')
        
        return None
        
    except Exception as e:
        print(f"Error in OpenCV preprocessing: {e}")
        import traceback
        traceback.print_exc()
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


