import azure.functions as func
import json
import logging
import base64
from io import BytesIO, StringIO
try:
    import pandas as pd
except ImportError:
    pd = None
from datetime import datetime
import csv

def export_as_csv(export_data, buffer):
    """Export data as CSV when pandas is not available"""
    if not export_data:
        return {"success": False, "error": "No data to export"}
    
    # Write CSV content
    csv_content = StringIO()
    if export_data:
        fieldnames = export_data[0].keys()
        writer = csv.DictWriter(csv_content, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(export_data)
    
    # Convert to bytes and base64
    csv_bytes = csv_content.getvalue().encode('utf-8')
    file_base64 = base64.b64encode(csv_bytes).decode()
    filename = f"volvo_dmc_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    mimetype = "text/csv"
    
    return {
        "success": True,
        "file": file_base64,
        "filename": filename,
        "mimetype": mimetype,
        "records": len(export_data)
    }

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Export function processed a request.')
    
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
        export_data = req_body.get('data', [])
        export_format = req_body.get('format', 'excel')
        
        if not export_data:
            return func.HttpResponse(
                json.dumps({"error": "No export data provided"}),
                status_code=400,
                headers={"Content-Type": "application/json"}
            )
        
        # Create DataFrame or fallback to manual processing
        if export_format.lower() == 'excel' and pd is not None:
            # Use pandas for Excel export
            df = pd.DataFrame(export_data)
            df['Generated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Generate Excel file
            buffer = BytesIO()
            df.to_excel(buffer, index=False, engine='openpyxl')
            file_base64 = base64.b64encode(buffer.getvalue()).decode()
            filename = f"volvo_dmc_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            mimetype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
            response = {
                "success": True,
                "file": file_base64,
                "filename": filename,
                "mimetype": mimetype,
                "records": len(export_data)
            }
        else:
            # Export as CSV (fallback or requested format)
            for item in export_data:
                item['Generated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            response = export_as_csv(export_data, None)
        
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
        logging.error(f"Error in export: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            headers={"Content-Type": "application/json"}
        )
