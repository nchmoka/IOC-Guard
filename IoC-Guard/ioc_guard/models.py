from django.db import models
import os
from django.utils.html import format_html
from django.urls import reverse

class Report(models.Model):
    report_type = models.CharField(max_length=50)
    file_path = models.FilePathField(path="media/reports")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.report_type} Report - {self.created_at}"

    def delete(self, *args, **kwargs):
        # Delete the file from the filesystem
        if self.file_path and os.path.isfile(self.file_path):
            os.remove(self.file_path)
        
        # Call the superclass delete method to delete the model instance
        super().delete(*args, **kwargs)

    def download_link(self):
        if self.file_path:
            filename = os.path.basename(self.file_path)
            download_url = reverse('admin:download_report', args=[self.pk])
            return format_html(f'<a href="{download_url}" download>{filename}</a>')
        return "No file available"

    download_link.short_description = "Download Report"
