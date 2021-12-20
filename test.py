import classes
 
import unittest
from unittest.mock import patch
import pygame

from classes import Bullet 


class GameUnittest(unittest.TestCase):


    def test_shot(self, test_patch):
        Tank = classes.DefaultTank(100, 100, (1, 0), (0, 255, 0))
        Tank.shot()
        self.assertEqual(len(classes.all_objects), 1)
        classes.all_objects = 0
        self.assertEqual(classes.shot(), classes.all_objects.append(Bullet))
