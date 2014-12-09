try:
    import _path
except NameError:
    pass
import spyral
from functools import partial

RESOLUTION =(640, 480)
PLACES_TO_PRESS = [(1,1), (1, 51), (1,101)]
i = 0

'''
Note: For some reason, testing this causes the events to repeat exponentially. This does not
affect the outcome of the test.
'''



def touch_screen(): 
    ''' 
    Walk through PLACES_TO_PRESS, triggering each one (one per tick), and then 
    exiting. You will probably use this pattern to walk through a list of 
    events that you want to handle. A more sophisticated approach would be 
    to build up a list of runnable event handles: 
     
    EVENTS_TO_RUN = [ 
        lambda : spyral.event.handle('input.mouse.down', spyral.Event(pos=(5, 5), button='left'), my_scene), 
        lambda : spyral.event.handle('input.mouse.up', spyral.Event(pos=(5, 5), button='left'), my_scene), 
        lambda : spyral.event.handle('input.mouse.down', spyral.Event(pos=(55, 55), button='right'), my_scene), 
        lambda : spyral.event.handle('input.mouse.up', spyral.Event(pos=(55, 55), button='right'), my_scene), 
        ... 
        lambda : spyral.event.handle('system.quit', spyral.Event(), my_scene), 
    ] 
    '''
    global i 
    if i < len(PLACES_TO_PRESS): 
        trigger_fake_mouse_click(PLACES_TO_PRESS[i]) 
    elif i > len(PLACES_TO_PRESS): 
        # We wait an extra frame before exiting so that we handle all the 
        #   triggered events 
        spyral.director.quit() 
    i += 1 
      
          
def trigger_fake_mouse_click(pos): 
    ''' 
    Build up a fake mouse event and then send it to be handled. 
    ''' 
    mouse_press_event = spyral.Event(pos=pos, button=1) 
    spyral.event.handle('input.mouse.down', mouse_press_event, my_scene) 
      
     ### Similar: 
     ##keyboard_press_event = spyral.Event(unicode=, key=, mod=) 
     ##spyral.event.handle('input.keyboard.down', keyboard_press_event, my_scene) 
       

def button_clicked(widget): 
    ''' 
    React to button click 
    '''
    print "Button was clicked, ", widget.pos
    printer()
    change_state(widget)
    print "Changing " + widget.name + " to up"
    assert widget.state == 'up'
    printer()
    print "Pass"

def focused_clicked(widget): 
    ''' 
    React to button click 
    '''
    print "Button was clicked, ", widget.pos
    printer()
    change_state(widget)
    print "Changing " + widget.name + " to up" 
    assert widget.state == 'up_focused'
    printer()
    print "Pass"
    
def change_state(widget):
    widget._handle_mouse_down(radio)
    
def printer():
    print "Current State:" + radio.one.state + " " + radio.two.state + " " + radio.three.state
        
spyral.director.init(RESOLUTION)
my_scene = spyral.Scene(RESOLUTION)
my_scene.background = spyral.Image(size=RESOLUTION).fill((0,0,0))
spyral.event.register("system.quit", spyral.director.quit, scene=my_scene)
class RadioForm(spyral.Form):
    one= spyral.widgets.RadioButton()
    two= spyral.widgets.RadioButton()
    three= spyral.widgets.RadioButton()
radio = RadioForm(my_scene)
radio.focus()
radio.one.pos = (0, 0)
radio.two.pos = (0, 50)
radio.three.pos = (0, 100)



spyral.event.register("form.RadioForm.one.changed", focused_clicked, scene=my_scene)
spyral.event.register("form.RadioForm.two.changed", button_clicked, scene=my_scene)
spyral.event.register("form.RadioForm.three.changed", button_clicked, scene=my_scene)
spyral.event.register("director.update", touch_screen, scene=my_scene)


spyral.director.run(scene=my_scene)

