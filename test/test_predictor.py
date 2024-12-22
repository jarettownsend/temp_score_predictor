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