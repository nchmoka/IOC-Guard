from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ioc_guard.ioc_checker.main import process_iocs
from ioc_guard.ioc_checker.report_generator import generate_pdf
from .serializers import DomainSerializer, IPSerializer, HashSerializer
import os
from django.conf import settings
from .models import Report
import uuid

class DomainCheckView(APIView):
    def post(self, request):
        serializer = DomainSerializer(data=request.data)
        if serializer.is_valid():
            domain = serializer.validated_data.get('domain')
            report_data = process_iocs([domain], ioc_type='domain')

            unique_filename = f"domain_report_{uuid.uuid4().hex}.pdf"
            output_file = os.path.join(settings.MEDIA_ROOT, 'reports', unique_filename)
            generate_pdf(report_data, output_file)

            Report.objects.create(report_type='Domain', file_path=output_file)

            download_url = request.build_absolute_uri(settings.MEDIA_URL + f"reports/{unique_filename}")
            return Response({"message": "PDF report generated", "file_path": output_file, "download_url": download_url}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IPCheckView(APIView):
    def post(self, request):
        serializer = IPSerializer(data=request.data)
        if serializer.is_valid():
            ip = serializer.validated_data.get('ip')
            report_data = process_iocs([ip], ioc_type='ip')

            unique_filename = f"ip_report_{uuid.uuid4().hex}.pdf"
            output_file = os.path.join(settings.MEDIA_ROOT, 'reports', unique_filename)
            generate_pdf(report_data, output_file)

            Report.objects.create(report_type='IP', file_path=output_file)

            download_url = request.build_absolute_uri(settings.MEDIA_URL + f"reports/{unique_filename}")
            return Response({"message": "PDF report generated", "file_path": output_file, "download_url": download_url}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HashCheckView(APIView):
    def post(self, request):
        serializer = HashSerializer(data=request.data)
        if serializer.is_valid():
            hash_value = serializer.validated_data.get('hash_value')
            report_data = process_iocs([hash_value], ioc_type='hash')

            unique_filename = f"hash_report_{uuid.uuid4().hex}.pdf"
            output_file = os.path.join(settings.MEDIA_ROOT, 'reports', unique_filename)
            generate_pdf(report_data, output_file)

            Report.objects.create(report_type='Hash', file_path=output_file)

            download_url = request.build_absolute_uri(settings.MEDIA_URL + f"reports/{unique_filename}")
            return Response({"message": "PDF report generated", "file_path": output_file, "download_url": download_url}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
