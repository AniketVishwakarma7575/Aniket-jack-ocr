from django.urls import path
from .views import AIOCRProcessView

urlpatterns = [
    path('process/', AIOCRProcessView.as_view(), name='ai_ocr_process'),
]