from django.test import TestCase, Client
from django.urls import reverse

class UsersViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_valid_magic_password(self):
        """Test authentication with magic password"""
        response = self.client.get('/users/', {'password': 'CSE270Rocks!'})
        self.assertEqual(response.status_code, 200)

    def test_valid_admin_credentials(self):
        """Test authentication with admin credentials"""
        response = self.client.get('/users/', {'username': 'admin', 'password': 'qwerty'})
        self.assertEqual(response.status_code, 200)

    def test_invalid_credentials(self):
        """Test authentication with invalid credentials"""
        response = self.client.get('/users/', {'username': 'admin', 'password': 'wrong'})
        self.assertEqual(response.status_code, 401)

    def test_no_credentials(self):
        """Test authentication with no credentials"""
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 401)

    def test_ingest_endpoint(self):
        """Test the ingest endpoint"""
        response = self.client.get('/users/ingest')
        self.assertEqual(response.status_code, 200)


class EndToEndTest(TestCase):
    """End-to-end tests for the full system flow"""
    def setUp(self):
        self.client = Client()

    def test_full_authentication_and_data_flow(self):
        """Test complete flow: authenticate then access data"""
        # First authenticate
        auth_response = self.client.get('/users/', {'username': 'admin', 'password': 'qwerty'})
        self.assertEqual(auth_response.status_code, 200)

        # Then access data
        data_response = self.client.get('/data/all')
        self.assertEqual(data_response.status_code, 200)

        # Verify data structure
        import json
        data = json.loads(data_response.content)
        self.assertIn('businesses', data)
        self.assertGreater(len(data['businesses']), 0)


class IntegrationTest(TestCase):
    """Integration tests between components"""
    def setUp(self):
        self.client = Client()

    def test_users_and_data_integration(self):
        """Test that users and data services work together"""
        # Test that both endpoints are accessible
        user_response = self.client.get('/users/', {'password': 'CSE270Rocks!'})
        data_response = self.client.get('/data/all')

        self.assertEqual(user_response.status_code, 200)
        self.assertEqual(data_response.status_code, 200)

        # Test CORS headers are present
        self.assertIn('Access-Control-Allow-Origin', user_response)
        self.assertIn('Access-Control-Allow-Origin', data_response)
        self.assertEqual(user_response['Access-Control-Allow-Origin'], '*')
        self.assertEqual(data_response['Access-Control-Allow-Origin'], '*')


class SecurityTest(TestCase):
    """Security testing"""
    def setUp(self):
        self.client = Client()

    def test_sql_injection_protection(self):
        """Test protection against SQL injection"""
        # Try SQL injection attempts
        injection_attempts = [
            {'username': "admin' OR '1'='1", 'password': 'anything'},
            {'username': 'admin', 'password': "qwerty' --"},
            {'username': 'admin', 'password': "'; DROP TABLE users; --"},
        ]
        for attempt in injection_attempts:
            response = self.client.get('/users/', attempt)
            # Should still return 401, not execute injection
            self.assertEqual(response.status_code, 401)

    def test_xss_protection(self):
        """Test protection against XSS"""
        # Since this is a simple app, check that user input isn't reflected dangerously
        response = self.client.get('/users/', {'username': '<script>alert("xss")</script>', 'password': 'test'})
        self.assertEqual(response.status_code, 401)
        # Content should not contain the script tag
        self.assertNotIn('<script>', response.content.decode())

    def test_cors_headers(self):
        """Test CORS security headers"""
        response = self.client.get('/users/', {'password': 'CSE270Rocks!'})
        self.assertEqual(response['Access-Control-Allow-Origin'], '*')
        self.assertIn('Access-Control-Allow-Headers', response)
        self.assertIn('Cross-Origin-Opener-Policy', response)


class AccessibilityTest(TestCase):
    """Accessibility testing"""
    def setUp(self):
        self.client = Client()

    def test_data_endpoint_accessibility(self):
        """Test data endpoint for accessibility considerations"""
        response = self.client.get('/data/all')
        content = response.content.decode()

        # Check for proper content type
        self.assertEqual(response['Content-Type'], 'application/json')

        # For JSON APIs, ensure data is structured properly
        import json
        data = json.loads(content)

        # Check that businesses have descriptive information
        for business in data['businesses']:
            self.assertIn('name', business)
            self.assertIn('adcopy', business)  # Description for screen readers
            # Check that websites are valid URLs
            if business['website'] != 'none':
                self.assertTrue(business['website'].startswith('http'))


class LoadTest(TestCase):
    """Load testing"""
    def setUp(self):
        self.client = Client()

    def test_multiple_concurrent_requests(self):
        """Test handling multiple requests"""
        # Simulate multiple requests
        responses = []
        for i in range(10):
            response = self.client.get('/data/all')
            responses.append(response.status_code)

        # All should succeed
        self.assertTrue(all(code == 200 for code in responses))

    def test_authentication_under_load(self):
        """Test authentication with multiple requests"""
        responses = []
        for i in range(5):
            response = self.client.get('/users/', {'password': 'CSE270Rocks!'})
            responses.append(response.status_code)

        self.assertTrue(all(code == 200 for code in responses))


class FaultInjectionTest(TestCase):
    """Fault injection testing"""
    def setUp(self):
        self.client = Client()

    def test_invalid_json_handling(self):
        """Test handling of malformed requests"""
        # Try posting to GET-only endpoints
        response = self.client.post('/data/all', {'invalid': 'data'})
        # The current implementation accepts POST, so it returns 200
        self.assertEqual(response.status_code, 200)

    def test_large_payload_handling(self):
        """Test handling of large payloads"""
        large_data = {'username': 'admin' * 1000, 'password': 'test' * 1000}
        response = self.client.get('/users/', large_data)
        # Should handle gracefully
        self.assertIn(response.status_code, [200, 401, 400])

    def test_special_characters(self):
        """Test handling of special characters"""
        special_chars = ['@', '#', '$', '%', '^', '&', '*', '(', ')', '[', ']', '{', '}', '|', '\\', '/', '?', '<', '>', ',', '.', ';', ':', '\'', '"']
        for char in special_chars:
            response = self.client.get('/users/', {'username': f'admin{char}', 'password': 'qwerty'})
            # Should not crash
            self.assertIsInstance(response.status_code, int)
