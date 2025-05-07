import unittest

from cancer_prediction.cancer_model import CancerModel


class TestCancerModel(unittest.TestCase):

    def test_target_to_diagnosis(self):
        model = CancerModel()
        self.assertEqual(model.target_to_diagnosis(0), "Malignant")
        self.assertEqual(model.target_to_diagnosis(1), "Benign")

    def test_diagnosis_to_target(self):
        model = CancerModel()
        self.assertEqual(model.diagnosis_to_target("Malignant"), 0)
        self.assertEqual(model.diagnosis_to_target("Benign"), 1)
        self.assertEqual(model.diagnosis_to_target("Malignant"), 0)


if __name__ == "__main__":
    unittest.main()
