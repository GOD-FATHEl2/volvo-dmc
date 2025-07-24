#!/bin/bash
echo "🔍 Testing VOLVO DMC deployment..."

# Test local app
echo "📱 Testing local app..."
curl -s http://127.0.0.1:8000 > /dev/null && echo "✅ Local app: Working" || echo "❌ Local app: Failed"

# Test cloud app
echo "🌐 Testing cloud app..."
curl -s --max-time 30 https://volvo-dmc-app.braveground-410ffbbc.swedencentral.azurecontainerapps.io/ > /dev/null && echo "✅ Cloud app: Working" || echo "❌ Cloud app: Failed or Timeout"

echo "🏁 Test complete!"
