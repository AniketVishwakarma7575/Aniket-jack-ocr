from django.contrib import admin
from django.utils.html import format_html
from .models import OCRDocument

@admin.register(OCRDocument)
class OCRDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_preview', 'uploaded_at')
    readonly_fields = ('image_preview_large', 'formatted_json')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px;" />', obj.image.url)
        return "No Image"

    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 500px;" />', obj.image.url)
        return "No Image"

    def formatted_json(self, obj):
        if not obj.processed_json: return "Not Processed"
        
        # Table UI for Admin Panel
        html = '<table border="1" style="border-collapse: collapse; width: 100%; text-align: left;">'
        html += '<tr style="background: #eee;"><th>Description</th><th>No</th><th>L</th><th>B</th><th>H</th><th>Qty</th></tr>'
        
        for row in obj.processed_json:
            html += f"""<tr>
                <td>{row.get('description', '-')}</td>
                <td>{row.get('no', '-')}</td>
                <td>{row.get('length', '-')}</td>
                <td>{row.get('breadth', '-')}</td>
                <td>{row.get('height', '-')}</td>
                <td>{row.get('quantity', '-')}</td>
            </tr>"""
        return format_html(html + '</table>')