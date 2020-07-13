import unittest
from test_base import TestFlaskBase

class TestWeb(TestFlaskBase):
    def test_server_is_on(self):   #Los test deben comenzar por un método test
        response = self.client.get('/')   # .get lleva el verbo de la petición 
        self.assertEqual(response.status_code, 200)

    def test_route_index_is_Hola_mundo(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Hola mundo')


if __name__ == '__main__':
    unittest.main()