#Keypress test
#simulates repeated keypresses when a key is held down
#was made for use with the mario game

import simplegui

def timer_handler():
    #start timer 2 if it is off
    if not timer_on:
        timer2.start()
    #stop timer 1
    timer.stop()

def timer2_handler():
    #simulates repeated keypresses if the key is held down
    global timer_on
    timer_on=True
    if len(held_keys)==0:
        timer2.stop()
        timer_on=False
    else:
        for item in held_keys:
            action(item)

def action(key):
    #this is where all the code to make something happen goes
    if key==upkey:
        #do something
        print('up key pressed')
    elif key==downkey:
        #do something else
        print('down key pressed')

def key_handler(key):
    #handles user keypresses
    #add key to held keys
    global held_keys
    held_keys.append(key)
    #do something with key
    action(key)
    #start timer 1 if timer 2 is off
    if not timer_on:
        timer.start()

def release_handler(key):
    #handles key releases
    #remove the key from the list
    global held_keys
    if key in held_keys:
        held_keys.remove(key)
    #if no keys are held, stop both timers
    global timer_on
    if len(held_keys)==0:
        timer.stop()
        timer2.stop()
        timer_on=False

timer_on=False
held_keys=[]

#starts timer 2
timer = simplegui.create_timer(300, timer_handler)
#automatic keypress
timer2 = simplegui.create_timer(100, timer2_handler)

#map whatever keys you need
spacekey=simplegui.KEY_MAP['space']
leftkey=simplegui.KEY_MAP['left']
rightkey=simplegui.KEY_MAP['right']
upkey=simplegui.KEY_MAP['up']
downkey=simplegui.KEY_MAP['down']

#create a frame and set key down/up handlers
frame=simplegui.create_frame('Click the box, then use arrow keys to move', 100, 100)
frame.set_keydown_handler(key_handler)
frame.set_keyup_handler(release_handler)
frame.start()
