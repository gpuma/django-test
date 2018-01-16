from django.test import TestCase
from .word_cloud import WordCloud

def create_dummy_local_file():
    """
    Returns the filename of a generated dummy
    plaintext file.
    """
    # todo: not sure if necessary


# Create your tests here.
class WordCloudTests(TestCase):
    def test_word_cloud_from_local_file(self):
        # todo: change to something more dynamic
        test_filename = 'D:\\borrar.txt'
        cloud = WordCloud(uri=test_filename, type="local")
        # dimensions must be greater zero
        self.assertGreater(cloud.canv_x, 0, msg=None)
        self.assertGreater(cloud.canv_y, 0, msg=None)
        # word_list must have items
        self.assertGreater(len(cloud.words), 0)

    # def test_word_cloud_from_url(self):
    #     # todo: change this shit
    #     test_url = 'some url'
    #     wc = WordCloud(test_filename, type="internet")
