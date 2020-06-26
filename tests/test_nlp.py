import unittest
import pytest
import sys

sys.path.append("C:\\Users\\stosc\\Documents\\ESME\\Ingé2_2019-2020\\S2\\UE1\\DataTools\\Projet\\codes\\NLP")

from NLP import remove_punctuation, remove_digits



class TestNlp(unittest.TestCase):
    def test_remove_punctuation(self):

        # Given
        given = "remove."
        expected_output = "remove"
        # When
        output = remove_punctuation(given)
        # Then
        self.assertEqual(expected_output, output)



    def test_remove_digits(self):

        # Given
        given = "Remove 3"
        expected_output = "Remove "
        # When
        output = remove_digits(given)
        # Then
        self.assertEqual(expected_output, output)