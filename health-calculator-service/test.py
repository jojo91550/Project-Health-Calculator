import unittest
from health_utils import calculate_bmi, calculate_bmr

class TestHealthUtils(unittest.TestCase):
    def test_calculate_bmi(self):
        bmi = calculate_bmi(1.75, 70)
        print(f"BMI: {bmi}")
        self.assertAlmostEqual(bmi, 22.86, places=2)
        
    def test_calculate_bmr(self):
        # Test pour un homme
        bmr_male = calculate_bmr(175, 70, 30, 'male')
        print(f"BMR for male: {bmr_male}")
        self.assertAlmostEqual(bmr_male, 1695.67, places=2)
        
        # Test pour une femme
        bmr_female = calculate_bmr(165, 60, 25, 'female')
        print(f"BMR for female: {bmr_female}")
        self.assertAlmostEqual(bmr_female, 1405.33, places=2)

if __name__ == '__main__':
    unittest.main()