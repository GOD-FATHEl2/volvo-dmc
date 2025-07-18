import azure.functions as func
import json
import logging
import base64
from io import BytesIO
import pandas as pd
from datetime import datetime

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
        
        # Create DataFrame
        df = pd.DataFrame(export_data)
        
        # Add timestamp
        df['Generated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Generate file
        buffer = BytesIO()
        
        if export_format.lower() == 'excel':
            # Export as Excel
            df.to_excel(buffer, index=False, engine='openpyxl')
            file_base64 = base64.b64encode(buffer.getvalue()).decode()
            filename = f"volvo_dmc_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            mimetype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        else:
            # Export as CSV
            df.to_csv(buffer, index=False)
            file_base64 = base64.b64encode(buffer.getvalue()).decode()
            filename = f"volvo_dmc_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            mimetype = "text/csv"
        
        response = {
            "success": True,
            "file": file_base64,
            "filename": filename,
            "mimetype": mimetype,
            "records": len(export_data)
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
        logging.error(f"Error in export: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            headers={"Content-Type": "application/json"}
        )
