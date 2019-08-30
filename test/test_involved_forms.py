import unittest
from test import client, OPEN_ID


class InvolvedFormsTestCase(unittest.TestCase):
    def test_get_involved_forms(self):
        response = client.get('/api/involved_forms?open_id={}'.format(OPEN_ID))
        data = response.get_json()
        self.assertEqual(data['err_msg'], 'ok')


if __name__ == '__main__':
    unittest.main()
