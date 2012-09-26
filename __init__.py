"""
Spyral, an awesome library for making games.
"""

__version__ = '0.1.1'
__license__ = 'MIT'
__author__ = 'Robert Deaton'

import compat

import memoize
import point
import camera
import sprite
import scene
import _lib
import event
import animator
import animation
import pygame
import image
import color
import rect
import signal
import vector

Scene = scene.Scene
Image = image.Image
Sprite = sprite.Sprite
Group = sprite.Group
AnimationSprite = animation.AnimationSprite
AnimationGroup = animation.AnimationGroup
Rect = rect.Rect
Signal = signal.Signal
Vec2D = vector.Vec2D

keys = event.keys
director = scene.Director()


def init():
    event.init()
    pygame.init()
    pygame.font.init()


def quit():
    pygame.quit()
    director._stack = []
