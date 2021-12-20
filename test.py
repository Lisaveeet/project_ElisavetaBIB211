import classes
 
import unittest
import pygame

from classes import Bullet 


class GameUnittest(unittest.TestCase):


    def test_shot(self):
        Tank = classes.DefaultTank(100, 100, (1, 0), (0, 255, 0))
        Tank.prev_shoot = False
        Tank.shot()
        self.assertEqual(len(classes.all_objects), 2)
        testBullet = classes.all_objects[1]
        bullet = Bullet(125, 125, (2, 0), (0, 255, 0))
        self.assertEqual(bullet.rect, testBullet.rect)
        self.assertEqual(bullet.dir, testBullet.dir)
        self.assertEqual(bullet.color, testBullet.color)
