from unittest.mock import patch

import aiohttp
import cv2
from helper import BLACK_IMAGE, download_image_from_url, download_images
from tests import CompTestCase



class TestHelper(CompTestCase):
    # TODO: to be fixed
    @patch("aiohttp.ClientSession.get")
    async def test_download_image_from_url(self, mock_clientsession_get):
        """Test download image from url."""
        dummy_url = "http://url"
        async with aiohttp.ClientSession() as session:
            download_image_from_url(session=session, url=dummy_url)

        mock_clientsession_get.assert_called_once_with(dummy_url)
        self.assertEqual(mock_clientsession_get.call_count, 1)

    # TODO: to be fixed
    @patch("aiohttp.ClientSession.get")
    async def test_download_image_from_url_fail(self, mock):
        """Test download image from url (fail case)."""
        dummy_url = "http://url"
        mock.return_value.__aenter__.return_value.status = 500
        
        async with aiohttp.ClientSession() as session:
            resp = download_image_from_url(session=session, url=dummy_url)

            image_bytes = cv2.imencode(".png", BLACK_IMAGE)[1].tobytes()
            self.assertEqual(resp == image_bytes)

        mock.assert_called_once_with(dummy_url)
        self.assertEqual(mock.call_count, 1)