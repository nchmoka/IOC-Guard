from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from .models import Report
import os

class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'created_at', 'download_link')
    readonly_fields = ('report_type', 'created_at', 'download_link')

    def has_add_permission(self, request):
        # Disable the add functionality
        return False

    def has_change_permission(self, request, obj=None):
        # Disable the change functionality, but allow viewing the object
        return False

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('download/<int:report_id>/', self.download_report, name='download_report'),
        ]
        return custom_urls + urls

    def download_report(self, request, report_id):
        report = self.get_object(request, report_id)
        if report and report.file_path and os.path.isfile(report.file_path):
            with open(report.file_path, 'rb') as report_file:
                response = HttpResponse(report_file.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename={os.path.basename(report.file_path)}'
                return response
        else:
            self.message_user(request, "The requested file does not exist.", level='error')
            return HttpResponse(status=404)

admin.site.register(Report, ReportAdmin)
