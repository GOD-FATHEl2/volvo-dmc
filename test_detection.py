"""
Test Detection Methods Available
Run this to see which DMC detection libraries are working
"""
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from dmc_detection_hybrid import get_detection_status

if __name__ == "__main__":
    print("🔍 VOLVO DMC Detection System Status")
    print("=" * 50)
    
    status = get_detection_status()
    
    print(f"📚 Available Methods: {', '.join(status['methods'])}")
    print(f"🎯 Recommended Method: {status['recommended']}")
    print(f"🔧 OpenCV Available: {status['has_opencv']}")
    
    if 'pylibdmtx' in status['methods']:
        print("✅ EXCELLENT: pylibdmtx is available - Best DMC detection!")
        print("   → Use for local development")
        print("   → May have issues on Azure Web App")
    
    if 'pyzbar' in status['methods']:
        print("✅ GOOD: pyzbar is available - Excellent QR detection, basic DMC")
        print("   → Works well on Azure Web App")
        print("   → Good fallback method")
    
    print("\n🚀 Ready to test DMC detection!")
    print("   → Point camera at DMC code")
    print("   → System will try best available method first")
