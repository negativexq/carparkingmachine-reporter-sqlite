import unittest
from datetime import datetime
from carparking import CarParkingMachine

class TestCarParkingMachine(unittest.TestCase):
    def setUp(self):
        self.parking_machine = CarParkingMachine(id="North",capacity=2, hourly_rate=2.5)

    def test_check_in(self):
        result = self.parking_machine.check_in("ABC123")
        self.assertTrue(result)

        result = self.parking_machine.check_in("DEF456")
        self.assertTrue(result)

        result = self.parking_machine.check_in("GHI789")
        self.assertFalse(result)  # capacity reached

    def test_check_out(self):
        self.parking_machine.check_in("ABC123")

        result = self.parking_machine.check_out("ABC123")
        self.assertEqual(result, 2.50)

        
if __name__ == '__main__':
    unittest.main()