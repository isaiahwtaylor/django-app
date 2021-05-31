import google.api_core.exceptions
from django.test import TestCase, RequestFactory
from root.utils import Firestore

class RequestTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_request_all_urls(self):
        urls = ['/', '/images', '/blog', '/internal']
        for url in urls:
            response = self.client.get(url, follow=True)
            self.assertEqual(response.status_code, 200)
    def test_request_image_details(self):
        response = self.client.get('/images/?exp=2460.1')
        self.assertEqual(response.status_code, 200)


class FirestoreTest(TestCase):
    def setUp(self):
        self.db = Firestore('file-sorting-root-tracking')

    def test_get(self):
        doc = self.db.get('root', '2460')
        assert doc is not None
    def test_invalid_get(self):
        doc = self.db.get('root', 'invalid')
        assert doc is None

    def test_update(self):
        self.assertRaises(google.api_core.exceptions.NotFound,
                          self.db.update, 'robot-run-sample', 'invalid', {'example': 10})
    def test_invalid_update(self):
        self.db.update('robot-run-sample', 'box-example', {'example': 10})
    def test_put(self):
        self.db.put('robot-run-sample', 'box-example', {'example': 10}, True)