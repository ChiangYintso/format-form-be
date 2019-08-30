import unittest
from test import app


class AppTestCase(unittest.TestCase):
    def setUp(self) -> None:
        app.config.update(
            TESTING=True,
        )

    def test_app_exist(self):
        self.assertFalse(app is None)

    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])


if __name__ == '__main__':
    unittest.main()
