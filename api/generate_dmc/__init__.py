import azure.functions as func
import json
import logging
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import datetime
import os

# Create a simplified DMC generator without pylibdmtx
def generate_dmc_placeholder(data):
    """Generate a placeholder image for DMC since pylibdmtx isn't available in Azure Functions"""
    # Create a simple placeholder image
    img = Image.new('RGB', (200, 200), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple grid pattern to simulate DMC
    for i in range(0, 200, 10):
        for j in range(0, 200, 10):
            if (i + j) % 20 == 0:
                draw.rectangle([i, j, i+5, j+5], fill='black')
    
    # Add text
    try:
        font = ImageFont.load_default()
        draw.text((10, 10), "DMC", fill='black', font=font)
        draw.text((10, 30), str(data)[:20], fill='black', font=font)
    except:
        pass
    
    # Convert to base64
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return img_str

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Generate DMC function processed a request.')
    
    try:
        # Get request data
        req_body = req.get_json()
        
        if not req_body:
            return func.HttpResponse(
                json.dumps({"error": "No data provided"}),
                status_code=400,
                headers={"Content-Type": "application/json"}
            )
        
        # Extract data
        data = req_body.get('data', '')
        batch_data = req_body.get('batch_data', [])
        
        if batch_data:
            # Handle batch generation
            results = []
            for item in batch_data:
                img_base64 = generate_dmc_placeholder(item)
                results.append({
                    'data': item,
                    'image': img_base64
                })
            
            response = {
                "success": True,
                "batch_results": results,
                "count": len(results)
            }
        else:
            # Single DMC generation
            img_base64 = generate_dmc_placeholder(data)
            response = {
                "success": True,
                "image": img_base64,
                "data": data
            }
        
        return func.HttpResponse(
            json.dumps(response),
            status_code=200,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            }
        )
        
    except Exception as e:
        logging.error(f"Error in generate_dmc: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            headers={"Content-Type": "application/json"}
        )
