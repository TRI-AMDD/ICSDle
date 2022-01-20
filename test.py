import unittest
from monty.serialization import loadfn
from main import check_formula


class IcsdleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = loadfn("formulas.json")
        return cls

    def test_response(self):
        # Works and all correct for identity
        response = check_formula("TiO2", "TiO2")
        self.assertTrue(all([r[1] for r in response]))

        # Test group
        response = check_formula("GeO2", "SnO2")
        self.assertEqual(response[0][1], "group")
        self.assertEqual(response[-1][1], "correct")

        # Test nothing
        response = check_formula("GeO2", "SbO2")
        self.assertEqual(response[0][1], "nothing")
        self.assertEqual(response[-1][1], "correct")

        # Test row
        response = check_formula("Fe2O3", "TiO2")
        self.assertEqual(response[0][1], "row")
        self.assertEqual(response[2][1], "correct")
        self.assertEqual(response[3][1], "nothing")

        response = check_formula("CO2", "La13B4O26")
        self.assertEqual(response[0][1], "row")


if __name__ == "__main__":
    unittest.main()
