import json
from django.test import TestCase, Client
from django.urls import reverse

class DataViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_data_endpoint_returns_json(self):
        """Test that data endpoint returns valid JSON"""
        response = self.client.get('/data/all')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        # Parse JSON response
        data = json.loads(response.content)
        self.assertIn('businesses', data)
        self.assertIsInstance(data['businesses'], list)

    def test_businesses_structure(self):
        """Test that businesses have required fields"""
        response = self.client.get('/data/all')
        data = json.loads(response.content)

        businesses = data['businesses']
        self.assertGreater(len(businesses), 0)

        # Check first business has all required fields
        business = businesses[0]
        required_fields = ['name', 'streetAddress', 'cityStateZip', 'phoneNumber',
                          'website', 'imageURL', 'membershipLevel', 'adcopy']
        for field in required_fields:
            self.assertIn(field, business)

    def test_membership_levels(self):
        """Test that membership levels are valid"""
        response = self.client.get('/data/all')
        data = json.loads(response.content)

        valid_levels = ['bronze', 'silver', 'gold', 'nonprofit']
        for business in data['businesses']:
            self.assertIn(business['membershipLevel'], valid_levels)
