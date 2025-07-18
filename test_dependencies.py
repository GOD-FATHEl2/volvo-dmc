#!/usr/bin/env python3
"""
Test script to verify system dependencies are properly installed
"""

def test_dmtx_library():
    """Test that pylibdmtx can be imported and used"""
    try:
        from pylibdmtx import pylibdmtx
        print("✅ pylibdmtx import successful")
        
        # Test basic functionality
        from pylibdmtx.pylibdmtx import encode
        data = b"test data"
        encoded = encode(data)
        if encoded:
            print("✅ pylibdmtx encode successful")
        else:
            print("❌ pylibdmtx encode failed")
            return False
            
        return True
    except ImportError as e:
        print(f"❌ pylibdmtx import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ pylibdmtx test failed: {e}")
        return False

def test_other_dependencies():
    """Test other critical dependencies"""
    try:
        import flask
        print("✅ Flask import successful")
        
        import flask_cors
        print("✅ Flask-CORS import successful")
        
        from PIL import Image
        print("✅ Pillow import successful")
        
        import pandas
        print("✅ Pandas import successful")
        
        import openpyxl
        print("✅ OpenPyXL import successful")
        
        return True
    except ImportError as e:
        print(f"❌ Dependency import failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing system dependencies...")
    
    success = True
    success &= test_dmtx_library()
    success &= test_other_dependencies()
    
    if success:
        print("\n🎉 All dependencies test passed!")
        exit(0)
    else:
        print("\n❌ Some dependencies tests failed!")
        exit(1)
