from django.db import models
import os
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.utils.html import format_html
from django.urls import reverse

class Report(models.Model):
    report_type = models.CharField(max_length=50)
    file_path = models.FilePathField(path="media/reports")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.report_type} Report - {self.created_at}"

    def download_link(self):
        if self.file_path:
            filename = os.path.basename(self.file_path)
            download_url = reverse('admin:download_report', args=[self.pk])
            return format_html(f'<a href="{download_url}" download>{filename}</a>')
        return "No file available"

    download_link.short_description = "Download Report"

@receiver(post_delete, sender=Report)
def delete_report_file(sender, instance, **kwargs):
    # Ensure the file is deleted after the model instance is deleted
    if instance.file_path:
        if os.path.isfile(instance.file_path):
            try:
                os.remove(instance.file_path)
                print(f"Deleted file: {instance.file_path}")
            except Exception as e:
                print(f"Error deleting file: {instance.file_path}. Exception: {e}")
        else:
            print(f"File not found: {instance.file_path}")
