import classes
 
import unittest
from unittest.mock import patch
import pygame 


class GameUnittest(unittest.TestCase):

    @patch('shot')
    def test_alive(self, test_patch):
        test_patch.return_value = {self.prev_shoot: 0}
        self.assertRaises(TypeError, self.testListNone[:1])


if __name__ == '__main__':
    unittest.main()
