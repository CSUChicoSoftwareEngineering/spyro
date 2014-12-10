try:
    import _path
except NameError:
    pass
import spyral
from functools import partial

RESOLUTION =(640, 480)
COUNT = 0
PLACES_TO_PRESS=[(0,0), (50, 50)]
i = 0


'''def click(widget):
    print "Hi"
    count.counter.update_text(COUNT +1)
    print count.counter.text'''
spyral.director.init(RESOLUTION)
my_scene = spyral.Scene(RESOLUTION)
my_scene.background = spyral.Image(size=RESOLUTION).fill((0,0,0))

class CountForm(spyral.Form):
    counter= spyral.widgets.Counter()
count=CountForm(my_scene)

count.counter.pos = (0,0)
count.counter.text = COUNT
print "Counter contains " + str(count.counter.text)
print "Testing update_text by adding 1 to counter"
count.counter.update_text(str(int(count.counter.text) + 1))
assert count.counter.text == "1"
print "Pass. Counter now equals: " + str(count.counter.text)
print "Adding 100 to counter"
count.counter.update_text(str(int(count.counter.text) + 100))
assert count.counter.text == "101"
print "Pass. Counter now equals: " + str(count.counter.text)
print "Now changing value of counter to contain the word: Program"
count.counter.update_text("Program")
assert count.counter.text == "Program"
print "Pass. Counter now says: " + count.counter.text
print "Testing _get_text function"
assert count.counter._get_text() == "Program"
print "pass"
print "Testing failure situation. Looking for 1 when counter desplays Program. This should result in an Assertion Error"
assert count.counter._get_text() == "1"
