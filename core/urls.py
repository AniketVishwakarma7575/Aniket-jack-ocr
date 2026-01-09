from django.urls import path
from .views import AIOCRProcessView, ExportExcelView

urlpatterns = [
    path('process/', AIOCRProcessView.as_view(), name='ai_ocr_process'),
    path('export-excel/', ExportExcelView.as_view(), name='export_excel'),
]