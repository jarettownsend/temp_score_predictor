import sys
import os
from unittest.mock import patch, MagicMock
import unittest
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

class TestPredictor(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        '''
        Sets env variable needed to import script, imports script
        and instantiates Class from script
        '''
        print('in setupUpClass')
        cls.env_patcher = patch.dict(os.environ, {"ADD ENV HERE": "KEY OF ENV HERE"}
                                                  )
        cls.env_patcher.start()
        import predictor
        cls.predictor = predictor


        super().setUpClass()
        #Variable to see the difference between expected and actual
        cls.maxDiff = None

    @classmethod
    def tearDownClass(cls):
        '''
        Tears down setUpClass and removes env variables.
        '''
        super().tearDownClass()
        cls.env_patcher.stop()
        print('class torn down')
    
    def test_env_setup(self):
        '''
        Test to ensure setUpClass is implemented as expected.
        '''
        self.assertEqual(os.environ["ADD ENV HERE"], "KEY OF ENV HERE")
        self.assertTrue(callable(self.predictor.calculate_z_score))

    def test_calculate_z_score(self):
        '''
        Test to ensure calculate_z_score function works as expected.
        '''
        # Case: New value is the same as the mean
        historical_values = [1, 2, 3, 4, 5]
        new_value = 3
        expected = 0
        result = self.predictor.calculate_z_score(new_value, historical_values)
        self.assertEqual(result, expected)

        # Case: Identical historical values
        historical_values = [3, 3, 3, 3, 3]
        new_value = 3
        expected = 0 
        result = self.predictor.calculate_z_score(new_value, historical_values)
        self.assertEqual(result, expected)

        # Case: Large new value
        historical_values = [1, 2, 3, 4, 5]
        new_value = 100
        result = self.predictor.calculate_z_score(new_value, historical_values)
        self.assertGreater(result, 0)  # Z should be positive

        # Case: Very small new value
        historical_values = [1, 2, 3, 4, 5]
        new_value = -100
        result = self.predictor.calculate_z_score(new_value, historical_values)
        self.assertLess(result, 0)  # Z should be negative