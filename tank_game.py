#This program was written before I had learned about python classes, and uses the CodeSkulptor simpleGUI

import simplegui
#GUI
def load():
    global playing
    global x
    global nmy_x
    global y
    global nmy_y
    global dirx
    global nmy_dirx
    global diry
    global nmy_diry
    global dir_dist
    global rotation
    global nmy_rotation
    global move
    global turn
    global gamesize_x
    global gamesize_y
    global points
    global timer
    global mode
    global shoot
    global player_shooting
    global shotx
    global shoty
    global shot_dir
    global shot_speed
    global health
    global nmy_health
    #Set Variables
    health = 10
    nmy_health = health
    player_shooting = 0
    shot_speed = 10
    shoot = False
    playing = False
    gamesize_x = 400
    gamesize_y = 400
    turn = 1
    x = gamesize_x - 10
    nmy_x = 10
    y = gamesize_y - 10
    nmy_y = 10
    dir_dist = 20
    rotation = 1
    nmy_rotation = 3
    move = 20
    points = 0

    
    #Functions here
    
    def end():
        global playing
        if playing == True:
            playing = False
            print('game ended')
            gameframe.stop()
            initalize_menu()
            

    def playing():
        global playing
        if playing != True:
            playing = True
            print('')
            print('game started')
        
    def inst():
        print('')
        print('Instructions:')
        print('')
        print('Press the left and right to turn and the up button to go forward.')
        print('Press the space bar to fire.')
        print('Destroy the other tank by shooting it or by runnig into it.')
        print('')
    
    #Function to shoot
    def shooting():
        global player_shooting
        global shoot
        global shotx
        global shoty
        global shot_dir
        global x
        global y
        global nmy_x
        global nmy_y
        global rotation
        global nmy_rotation
        shoot = True
        if player_shooting == 1:
            shot_dir = rotation
            shotx = x
            shoty = y
        else:
            shot_dir = nmy_rotation
            shotx = nmy_x
            shoty = nmy_y
            
        
    #Function to rotate
    def direction(direct):
        global turn
        global dir_dist
        if turn == 1:
            global rotation
            global dirx
            global diry
            rotation = rotation + direct
            if rotation == 5:
                rotation = 1
            elif rotation == 0:
                rotation = 4
            if rotation == 1:
                dirx = 0
                diry = -dir_dist
            elif rotation == 2:
                dirx = dir_dist
                diry = 0
            elif rotation == 3:
                dirx = 0
                diry = dir_dist
            elif rotation == 4:
                dirx = -dir_dist
                diry = 0
                
        else:
            global nmy_rotation
            global nmy_dirx
            global nmy_diry
            
            nmy_rotation = nmy_rotation + direct
            if nmy_rotation == 5:
                nmy_rotation = 1
            elif nmy_rotation == 0:
                nmy_rotation = 4
            if nmy_rotation == 1:
                nmy_dirx = 0
                nmy_diry = -dir_dist
            elif nmy_rotation == 2:
                nmy_dirx = dir_dist
                nmy_diry = 0
            elif nmy_rotation == 3:
                nmy_dirx = 0
                nmy_diry = dir_dist
            elif nmy_rotation == 4:
                nmy_dirx = -dir_dist
                nmy_diry = 0
                
    #Function to move forward       
    def moving():
        global turn
        global move
        global gamesize_x
        global gamesize_y
        global nmy_rotation
        global nmy_x
        global nmy_y
        global rotation
        global x
        global y
        global mode
        if turn == 1:
            global rotation
            global x
            global y
            if rotation == 1:
                y = y - move
            elif rotation == 2:
                x = x + move
            elif rotation == 3:
                y = y + move
            elif rotation == 4:
                x = x - move
            #Jump to other end of screen for p1
            if x >= gamesize_x:
                x = 10
            elif x <= 0:
                x = gamesize_x - 10
            elif y >= gamesize_y:
                y = 10
            elif y <= 0:
                y = gamesize_y - 10
            #Crashing
            if x == nmy_x and y == nmy_y and mode != 1:
                global nmy_health
                nmy_health = 0
                print('PLAYER1 WINS!')
                end()
        else:
            if nmy_rotation == 1:
                nmy_y = nmy_y - move
            elif nmy_rotation == 2:
                nmy_x = nmy_x + move
            elif nmy_rotation == 3:
                nmy_y = nmy_y + move
            elif rotation == 4:
                nmy_x = nmy_x - move
            #Jump to other end of screen for p2
            if nmy_x >= gamesize_x:
                nmy_x = 10
            elif nmy_x <= 0:
                nmy_x = gamesize_x - 10
            elif nmy_y >= gamesize_y:
                nmy_y = 10
            elif nmy_y <= 0:
                nmy_y = gamesize_y - 10
            #Crashing
            if x == nmy_x and y == nmy_y and mode != 1:
                global health
                health = 0
                if mode == 3:
                    print('PLAYER2 WINS!')
                else:
                    print('COMPUTER WINS!')
                end()
    
    #Refresh screen
    def draw(canvas):
        global playing
        global gamesize_x
        global gamesize_y
        global shoot
        global mode
        if playing == True:
            global x
            global y
            global dirx
            global diry
            finx = x + dirx
            finy = y + diry
            canvas.draw_line([x, y], [finx, finy], 5, 'blue')
            canvas.draw_circle((x, y), 2, 20, 'blue')
            #Load other player
            if mode == 2 or mode == 3:
                global nmy_x
                global nmy_y
                global nmy_dirx
                global nmy_diry
                global turn
                finx = nmy_x + nmy_dirx
                finy = nmy_y + nmy_diry
                canvas.draw_line([nmy_x, nmy_y], [finx, finy], 5, 'red')
                canvas.draw_circle((nmy_x, nmy_y), 2, 20, 'red')
                if turn == 1:
                    canvas.draw_circle((x, y), 2, 12, 'white')
                else:
                    canvas.draw_circle((nmy_x, nmy_y), 2, 12, 'white')
            if shoot == True:
                global shotx
                global shoty
                global shot_dir
                global shot_speed
                global randomcolor
                global health
                global nmy_health
                #Do the math for the shot
                if shot_dir == 1:
                    shotx = shotx + 0
                    shoty = shoty - shot_speed
                elif shot_dir == 2:
                    shotx = shotx + shot_speed
                    shoty = shoty + 0
                elif shot_dir == 3:
                    shotx = shotx + 0
                    shoty = shoty + shot_speed
                elif shot_dir == 4:
                    shotx = shotx - shot_speed
                    shoty = shoty + 0
                #Draw shot
                import random
                randomcolor = random.choice(['yellow', 'orange', 'pink', 'teal', 'silver', 'purple', 'navy', 'maroon', 'olive', 'lime', 'gray'])
                canvas.draw_circle((shotx, shoty), 2, 5, randomcolor)
                #Collisions
                if shotx == x and shoty == y and mode != 1:
                    shoot = False
                    health = health - 1
                    if health == 0:
                        if mode == 3:
                            print('PLAYER2 WINS!')
                        else:
                            print('COMPUTER WINS!')
                        end()
                    else:
                        print('player1 was hit.',health,'life remaining.')
                    turnchange()
                if shotx == nmy_x and shoty == nmy_y and mode != 1:
                    shoot = False
                    nmy_health = nmy_health - 1
                    if nmy_health == 0:
                        print('PLAYER1 WINS!')
                        end()
                    else:
                        if mode == 3:
                            print('player2 was hit.',nmy_health,'life remaining.')
                        else:
                            print('computer was hit.',nmy_health,'life remaining.')
                
                    turnchange()
                if shotx == 0 or shoty == 0 or shotx == gamesize_x or shoty == gamesize_y:
                    shoot = False
                    turnchange()
            
        else:
            canvas.draw_text('Press the start game button', [gamesize_x / 2,gamesize_y / 2], gamesize_x / 25, "white")

    #Change turns        
    def turnchange():
        global playing
        global mode
        global turn
        global shoot
        if mode != 1:
            if turn == 1:
                turn = 2
                if mode == 2 and playing == True and shoot == False:
                    timer.start()
            else:
                turn = 1
    
    #Handling keypresses for p1 and p2
    def key_handle(key):
        global player_shooting
        global turn
        global mode
        global shoot
        if turn == 2:
            if mode == 2 or shoot == True:
                print('Not your turn!')
            else:
                if key == 38:
                    print('player2 moved forward')
                    moving()
                    turnchange()
                elif key == 32:
                    print('player2 fired')
                    player_shooting = 2
                    shooting()
                elif key == 37:
                    print('player2 turned left')
                    direction(-1)
                    turnchange()
                elif key == 39:
                    print('player2 turned right')
                    direction(1)
                    turnchange()
        else:
            if shoot == False:
                if key == 38:
                    print('player1 moved forward')
                    moving()
                    turnchange()
                elif key == 32:
                    print('player1 fired')
                    player_shooting = 1
                    shooting()
                elif key == 37:
                    print('player1 turned left')
                    direction(-1)
                    turnchange()
                elif key == 39:
                    print('player1 turned right')
                    direction(1)
                    turnchange()
            else:
                print('Not your turn!')
    
    #Handles computer moves
    def nmy_timer():
        global playing
        global player_shooting
        import random
        if playing == True:
            random = random.choice([1, 2, 3, 4])
            if random == 1:
                direction(-1)
                print('computer turned left')
                turnchange()
            elif random == 2:
                direction(1)
                print('computer turned right')
                turnchange()
            elif random == 3:
                moving()
                print('computer moved forward')
                turnchange()
            elif random == 4:
                print('computer fired')
                player_shooting = 2
                shooting()
            else:
                print('Error, computer chose', random)
            timer.stop()


                
    #Setup stuff
    
    gameframe = simplegui.create_frame("Game", gamesize_x, gamesize_y)
    gameframe.set_canvas_background('green')
    gameframe.add_button("Start game", playing)
    gameframe.add_button("Instructions", inst)
    gameframe.set_keydown_handler(key_handle)
    gameframe.set_draw_handler(draw)
    timer = simplegui.create_timer(500, nmy_timer)
    timer.stop()
    direction(0)
    if mode != 1:
        turnchange()
        direction(0)
        turnchange()
    gameframe.start()


def initalize_menu():
    global menuframe
    menuframe = simplegui.create_frame("Menu", 200, 200)
    def begin_game():
        menuframe.stop()
        load()
    def alone():
        global mode
        mode = 1
        begin_game()
    def computer():
        global mode
        mode = 2
        begin_game()
    def versus():
        global mode
        mode = 3
        begin_game()

    menuframe.add_button("Play alone", alone)
    menuframe.add_button("Play against computer", computer)
    menuframe.add_button("Play against a friend", versus)

initalize_menu()
