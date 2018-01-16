from django.test import TestCase
from django.urls import reverse

from PIL import ImageFont

from .word_cloud import WordCloud
from .constants import *

def create_dummy_local_file():
    """
    Returns the filename of a generated dummy
    plaintext file.
    """
    # todo: not sure if necessary


class WordCloudTests(TestCase):
    def test_word_cloud_from_local_file(self):
        # todo: change to something more dynamic
        test_filename = 'D:\\borrar.txt'
        cloud = WordCloud(uri=test_filename, type="local")
        # font is valid
        fnt = ImageFont.truetype(cloud.font_location, 10)
        # dimensions must be greater zero
        self.assertGreater(cloud.canv_x, 0)
        self.assertGreater(cloud.canv_y, 0)
        # word_list must have items
        self.assertGreater(len(cloud.words), 0)

    def test_word_cloud_from_url(self):
        # todo: change this shit
        test_url = 'https://pastebin.com/raw/y4BskUX2'
        cloud = WordCloud(test_url, type="internet")
        # font is valid
        fnt = ImageFont.truetype(cloud.font_location, 10)
        # dimensions must be greater zero
        self.assertGreater(cloud.canv_x, 0)
        self.assertGreater(cloud.canv_y, 0)
        # word_list must have items
        self.assertGreater(len(cloud.words), 0)

class CreateViewTests(TestCase):
    def test_no_uri(self):
        """
        If no URI is provided, an error message is displayed
        """
        response = self.client.post(reverse('nube:create'), {'uri':''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, URI_NOT_SPECIFIED)
