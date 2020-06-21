import unittest

from codes.scrapping import get_html_from_link

class TestScrapping(unittest.TestCase):

    def test_get_html_from_link(self):
        # Given
        l = 'https://www.imdb.com/chart/toptv/'
        
        #When
        result = get_html_from_link(l)

        #Then
        