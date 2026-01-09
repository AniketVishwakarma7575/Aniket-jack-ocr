# ==================== core/models.py ====================
from django.db import models

class OCRDocument(models.Model):
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_json = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Document {self.id} - {self.uploaded_at}"
    
    class Meta:
        ordering = ['-uploaded_at']
