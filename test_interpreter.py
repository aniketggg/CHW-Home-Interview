import unittest
from interpreter import DMNInterpreter

class TestDMN(unittest.TestCase):
    def setUp(self):
        # Point this to your sample ruleset
        self.interpreter = DMNInterpreter('sample_ruleset.json')

    def test_patient_p1(self):
        # P1 is SEVERE because danger_sign is true
        patient = {"id": "P1", "danger_sign": True, "chest_indrawing": False, "stridor": False, "fast_breathing": False}
        result = self.interpreter.run_patient(patient)
        self.assertEqual(result['outcome'], "SEVERE")
        self.assertEqual(result['matched_rule'], "R1")
        self.assertEqual(result['path'], ["R1"])

    def test_patient_p4(self):
        # P4 should hit the default outcome
        patient = {"id": "P4", "danger_sign": False, "chest_indrawing": False, "stridor": False, "fast_breathing": False}
        result = self.interpreter.run_patient(patient)
        self.assertEqual(result['outcome'], "COUGH_NO_PNEUMONIA")
        self.assertEqual(result['matched_rule'], "default")
        self.assertEqual(result['path'], ["R1", "R2", "R3"])

    def test_missing_variable(self):
        # Test the error handling requirement
        patient = {"id": "ERR", "danger_sign": False} # Missing other variables
        with self.assertRaises(ValueError):
            self.interpreter.run_patient(patient)

if __name__ == '__main__':
    unittest.main()