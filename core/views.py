from rest_framework.views import APIView
from rest_framework.response import Response
from .models import OCRDocument
from .serializers import OCRUploadSerializer # Ensure you have a serializer
from .ai_processor import AIProcessor

class AIOCRProcessView(APIView):
    def post(self, request):
        # 1. Image upload handle karein
        serializer = OCRUploadSerializer(data=request.data)
        if serializer.is_valid():
            doc = serializer.save()
            
            # 2. Gemini Processor ko call karein
            ai = AIProcessor()
            structured_data = ai.process_handwriting_to_json(doc.image.path)
            
            if structured_data:
                # Database mein result save karein
                doc.processed_json = structured_data
                doc.save()
                
                return Response({
                    "status": "success",
                    "data": structured_data
                }, status=200)
            else:
                return Response({"status": "error", "message": "Gemini could not read image"}, status=500)
        
        return Response(serializer.errors, status=400)