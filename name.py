#Prints my name repeatedly, alternating the characters in it

import simplegui
global character
global tmi
global num
global last
character = "#"
num = 0
last = '^'

def char(string):
    global character
    global num
    global last
    print((string.replace('*', last)).replace(last, character , num))



def timer_handler():
    global character
    global tmi
    global num
    global last
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
    char('  ******************        *************         *****        ***       *************       ***********           ***')
    char('  ******************      *****************       ******       ***     ****************     *************          ***')
    char('        ****             *****         *****      *** ***      ***     *****************    ***                    ***')
    char('        ****            *****           ****      ***  ***     ***     *****       *****    ***                    ***')
    char('        ****            ****             ****     ***  ***     ***     ***           ***    ***                    ***')
    char('        ****            ***               ***     ***   ***    ***     ***           ***    ***                    ***')
    char('        ****            ***               ***     ***   ***    ***     ***           ***    ***                    ***')
    char('        ****            ***               ***     ***    ***   ***     ***           ***    ***                    ***')
    char('        ****            ***               ***     ***    ***   ***     *****************    ************           ***')
    char('        ****            ***               ***     ***     ***  ***     *****************    ************           ***')
    char('       *****            ***               ***     ***     ***  ***     ***           ***              ***          ***')
    char('      *****             ****             ****     ***      *** ***     ***           ***              ***          ***')
    char('**   *****              *****           *****     ***      *** ***     ***           ***              ***          ***')
    char('*** ****                 *****         *****      ***       ******     ***           ***              ***          ***')
    char('*******                   *****************       ***        *****     ***           ***    *************          ************      ')
    char('******                     ***************        ***         ****     ***           ***     ***********           ************      ')

    if num == 80:
        num = 0
        if character == '*':
            last = '*'
            character = '#'
        elif character == '#':
            last = '#'
            character = '@'
        elif character == '@':
            last = '@'
            character = '!'
        elif character == '!':
            last = '!'
            character = '^'
        elif character == '^':
            last = '^'
            character = '*'
    else:
        num = num + 1


timer = simplegui.create_timer(100, timer_handler)
timer.start()
