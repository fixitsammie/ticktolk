from django.test import TestCase

# Create your tests here.


import unittest
from .forms import EditThreadForm
class FormTests(unittest.TestCase):
    def test_validation(self):
        form_data = {
            'name': 'X' * 300,
        }

        form = EditThreadForm(data=form_data)
        self.assertFalse(form.is_valid())