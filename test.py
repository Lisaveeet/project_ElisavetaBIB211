from _typeshed import Self
import classes
 
import unittest
from unittest.mock import patch
import pygame 


class GameUnittest(unittest.TestCase):

    @patch('shot')
    def test_shot(self, test_patch):
        Tank = classes.DefaultTank(100, 100, (1, 0), (0, 255, 0))
        Tank.shot()
        self.assertEqual(len(classes.all_objects), 1)
        classes.all_objects = 0

                test_patch.return_value = {self.prev_shoot: 0}
        self.assertRaises(TypeError, self.testListNone[:1])


if __name__ == '__main__':
    unittest.main()
