from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class IoCGuardAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_domain_check_valid(self):
        response = self.client.post('/ioc_guard/api/check-domain/', {'domain': "example.com"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('file_path', response.data)
        self.assertIn('download_url', response.data)

    def test_ip_check_valid(self):
        response = self.client.post('/ioc_guard/api/check-ip/', {'ip': "8.8.8.8"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('file_path', response.data)
        self.assertIn('download_url', response.data)

    def test_hash_check_valid(self):
        response = self.client.post('/ioc_guard/api/check-hash/', {'hash_value': "44d88612fea8a8f36de82e1278abb02f"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('file_path', response.data)
        self.assertIn('download_url', response.data)

    def test_domain_check_no_domain(self):
        response = self.client.post('/ioc_guard/api/check-domain/', {'domain': ""}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ip_check_no_ip(self):
        response = self.client.post('/ioc_guard/api/check-ip/', {'ip': ""}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_hash_check_no_hash(self):
        response = self.client.post('/ioc_guard/api/check-hash/', {'hash_value': ""}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
