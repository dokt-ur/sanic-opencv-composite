from unittest.mock import patch

from sling_api import get_image_urls

from tests import CompTestCase


class TestSlingApi(CompTestCase):

    @patch("requests.get")
    def test_get_image_urls(self, mock_requests):

        get_image_urls()

        self.assertEqual(mock_requests.call_count, 1)