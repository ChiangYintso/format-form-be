import unittest
from test import client, OPEN_ID


class FormTemplatesTestCase(unittest.TestCase):
    def test_get_form_temp_success(self):
        response = client.get('/api/launched_forms?open_id={}'.format(OPEN_ID))
        data = response.get_json()
        self.assertEqual(data['err_msg'], 'ok')

    def test_get_form_temp_failed(self):
        response = client.get('/api/launched_forms?open={}'.format(OPEN_ID))
        data = response.get_json()
        self.assertEqual(data['err_code'], 3000)


if __name__ == '__main__':
    unittest.main()
