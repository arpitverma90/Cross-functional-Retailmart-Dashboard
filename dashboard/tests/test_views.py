import os
import unittest
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

class ViewRoutingTests(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'test_executive'
        self.password = 'ExecutivePass123!'
        if not User.objects.filter(username=self.username).exists():
            self.user = User.objects.create_user(
                username=self.username,
                password=self.password
            )
        else:
            self.user = User.objects.get(username=self.username)

    def test_health_check_endpoint(self):
        response = self.client.get('/health/')
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(json_data['status'], 'ok')
        self.assertEqual(json_data['database'], 'healthy')

    def test_login_page_renders(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('RetailMart', response.content.decode('utf-8'))

    def test_unauthenticated_redirect(self):
        response = self.client.get('/executive-summary/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_authenticated_executive_summary(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/executive-summary/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Executive Summary', response.content.decode('utf-8'))
        self.assertIn('Delivered Net Revenue', response.content.decode('utf-8'))

    def test_authenticated_sales_dashboard(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/business-dashboard/sales/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Sales Intelligence', response.content.decode('utf-8'))
        self.assertIn('Average Order Value', response.content.decode('utf-8'))

    def test_authenticated_customer_dashboard(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/business-dashboard/customers/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Customer Intelligence', response.content.decode('utf-8'))
        self.assertIn('RFM', response.content.decode('utf-8'))

    def test_authenticated_operations_dashboard(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/business-dashboard/operations/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Operations &amp; Logistics', response.content.decode('utf-8'))
        self.assertIn('On-Time Delivery', response.content.decode('utf-8'))

    def test_authenticated_cross_functional_dashboard(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/business-dashboard/cross-functional/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Cross-Functional Analytics', response.content.decode('utf-8'))
        self.assertIn('Perfect Order Rate', response.content.decode('utf-8'))

    def test_authenticated_scenario_simulator(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/business-dashboard/simulator/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Contribution Margin Scenario Simulator', response.content.decode('utf-8'))

    def test_api_endpoints(self):
        self.client.login(username=self.username, password=self.password)
        res_stores = self.client.get('/api/stores/')
        self.assertEqual(res_stores.status_code, 200)
        self.assertIn('stores', res_stores.json())

        res_sim = self.client.get('/api/simulator-baseline/')
        self.assertEqual(res_sim.status_code, 200)
        self.assertIn('base_net_revenue', res_sim.json())

    def test_filtered_views(self):
        self.client.login(username=self.username, password=self.password)
        params = {
            'start_date': '2025-01-01',
            'end_date': '2025-12-31',
            'region_id': '1',
            'category_id': '1',
            'customer_tier': 'Gold',
        }
        for path in [
            '/executive-summary/',
            '/business-dashboard/sales/',
            '/business-dashboard/customers/',
            '/business-dashboard/operations/',
            '/business-dashboard/cross-functional/',
        ]:
            response = self.client.get(path, params)
            self.assertEqual(response.status_code, 200, f"Filtered GET to {path} failed with status {response.status_code}")

    def test_cascading_stores_api_by_region(self):
        self.client.login(username=self.username, password=self.password)
        res = self.client.get('/api/stores/?region_id=1')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn('stores', data)
        self.assertTrue(len(data['stores']) > 0)

