import unittest
from app import calculate_points

class ReceiptProcessingTests(unittest.TestCase):

    def test_calculate_points(self):
        receipt = {
            "retailer": "Walmart",
            "purchaseDate": "2022-12-25",
            "purchaseTime": "15:30",
            "items": [
                {"shortDescription": "Apple", "price": "1.25"},
                {"shortDescription": "Banana", "price": "0.75"}
            ],
            "total": "2.00"
        }

        expected_points = 104  # Corrected expected points value
        calculated_points = calculate_points(receipt)
        self.assertEqual(calculated_points, expected_points)

if __name__ == '__main__':
    unittest.main()
