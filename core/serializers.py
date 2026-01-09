from rest_framework import serializers
from .models import OCRDocument

class OCRUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = OCRDocument
        fields = ['id', 'image', 'uploaded_at', 'processed_json']
        read_only_fields = ['id', 'uploaded_at', 'processed_json']