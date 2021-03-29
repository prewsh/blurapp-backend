import unittest

def addition(num1, num2):
    # if (num1 < 0):
    #     num1 *= -1
    # if (num2 < 0):
    #     num2 *= -1

    return num1 + num2


class AppTests(unittest.TestCase):

    def test_addition(self):
  
        self.assertEqual(addition(5,5),100)

    # def test_addition_not_equal(self):
    
    #     self.assertNotEqual(addition(5,5),0)

    # def test_adding_negatives(self):
    #     self.assertEqual(addition(-1, -2), -3)

    # def test_numbers(self):
    #     self.assertLess(5, 10)
    #     self.assertLessEqual(5, 5)
    #     self.assertGreater(10,5)
    #     self.assertGreaterEqual(10,10)
    #     self.assertGreaterEqual(10,9)

if __name__ == '__main__':
    unittest.main()
   