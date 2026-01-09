import pandas as pd
from io import BytesIO
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import OCRDocument
from .serializers import OCRUploadSerializer
from .ai_processor import AIProcessor
from openpyxl.styles import Font, PatternFill, Alignment

class AIOCRProcessView(APIView):
    def post(self, request):
        serializer = OCRUploadSerializer(data=request.data)
        if serializer.is_valid():
            doc = serializer.save()
            ai = AIProcessor()
            # Dynamic prompt wala processor yahan call hoga
            structured_data = ai.process_handwriting_to_json(doc.image.path)
            
            if structured_data:
                doc.processed_json = structured_data
                doc.save()
                return Response({
                    "status": "success",
                    "data": structured_data
                }, status=200)
            else:
                return Response({"status": "error", "message": "Gemini could not read image"}, status=500)
        return Response(serializer.errors, status=400)

class ExportExcelView(APIView):
    def post(self, request):
        structured_data = request.data.get('data')
        if not structured_data:
            return Response({"error": "No data provided"}, status=400)

        # 1. DataFrame Create karein (Ye automatic saare JSON keys ko columns bana dega)
        df = pd.DataFrame(structured_data)
        
        # Agar data khali nahi hai, toh columns ka order wahi rakhein jo AI ne bheja hai
        output = BytesIO()
        
        # 2. Excel Table Formatting
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # index=False taaki extra numeric column na aaye
            df.to_excel(writer, index=False, sheet_name='Extracted_Data')
            worksheet = writer.sheets['Extracted_Data']
            
            # Styling: Header color aur font
            # Blue background aur White bold text
            header_fill = PatternFill(start_color="0070C0", end_color="0070C0", fill_type="solid")
            header_font = Font(bold=True, color="FFFFFF")
            
            # Har detect hue column header par styling apply karein
            for cell in worksheet[1]:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal="center", vertical="center")

            # Column Width Auto-Adjust (Saare detect hue columns ke liye)
            for col in worksheet.columns:
                max_length = 0
                column = col[0].column_letter # Get Column Letter (A, B, C...)
                
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except: pass
                
                # Header length aur data length mein jo bada ho, uske hisaab se width set karein
                adjusted_width = (max_length + 4) 
                worksheet.column_dimensions[column].width = adjusted_width

        output.seek(0)
        
        # 3. Dynamic Response Setup
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        # Filename mein timestamp add kar sakte hain taaki unique rahe
        response['Content-Disposition'] = 'attachment; filename="Dynamic_Measurement_Report.xlsx"'
        return response