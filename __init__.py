import spyral.memoize
import spyral.point
import spyral.camera
import spyral.util
import spyral.sprite
import spyral.gui
import spyral.scene
import spyral._lib
import spyral.event
import pygame

director = scene.Director()

def init():
    pygame.init()
    pygame.font.init()
    
def quit():
    pygame.quit()
    spyral.director._stack = []