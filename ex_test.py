import random
import unittest
import spyral



class Game(spyral.Scene) :
    def __init__(self):
        spyral.Scene.__init__(self)
        self.background = spyral.Image(size=SIZE).fill(BG_COLOR)
        self.add_style_finction("make_box", make_box)
        self.load_style("style.spys")
        class RegisterForm(spyral.Form):
            one= spyral.widgets.RadioButton()
            two= spyral.widgets.RadioButton()
        my_form = RegisterForm(self)
        my_form.focus()
        self.num = 12
class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        my_game = Game()
    
    def test_alwaysTrue(self):
        self.assertTrue(1)

    """def test_sanity(self):
        spyral.director.init(SIZE)"""

    def test_button(self):
        self.assertEquals(my_game.my_form.one, 1)
        

if __name__ == '__main__':
    unittest.main()

