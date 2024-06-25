# admin.py
from django.contrib import admin
from .models import Document

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'description')
    search_fields = ('title', 'description')

# Register the Document model with the custom admin
admin.site.register(Document, DocumentAdmin)
