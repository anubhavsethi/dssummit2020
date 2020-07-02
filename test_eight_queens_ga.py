from eight_queens_ga import *
import unittest

class TestFitness(unittest.TestCase):
    def test_board_negative(self):
        test_list=[1,1,1,1,1,1,1,1]
        self.assertNotEqual(producescore(test_list),0)
        test_list=[1,1,1,1,1,1]
        self.assertRaises(IndexError,producescore,test_list)

    def test_board_positive(self):
        test_list=[2,5,7,0,3,6,4,1]
        self.assertEqual(producescore(test_list),0)

class TestCrossOver(unittest.TestCase):
    def test_crossover_negative(self):
        test_list=[[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1]]
        self.assertRaises(CustomError,crossmutate,test_list)
    
        
if __name__=="__main__":
    unittest.main()