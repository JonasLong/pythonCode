#Mario game

#Special keys:
#m- enable/disable music
#t- show/hide lag info
#w- enable/disable walk cycle
#i- display/hide info for objects, animation, and errors
#h- show/hide character hitbox
#s- stop everything
#p- enable/disable printing matrix to screen


def clear_matrix():
    #load the level
    global width
    global matrix
    width=level_widths[level-1]
    matrix=[]
    spacers=['|']
    under=['']
    count=0
    while count < width:
        spacers.append('░')
        count+=1
    spacers.append('|')
    count=0
    while count < height:
        matrix.append(spacers[:])
        count+=1

def render_game():
    global blocks
    if blocks!=0:
        if not blocks>145:
            blocks=0
    print('\n\n\n\n\n\n\n\n')
    for line in matrix_copy:
        group=''
        if not printall:
            for char in line:
                group+=char
            print(group)
        else:
            print(line)

def walk():
    #walk animation
    global character_animation
    if character_animation==0:
        character_animation=1
    elif character_animation==1:
        character_animation=2
    elif character_animation==2:
        character_animation=3
    elif character_animation==3:
        character_animation=0

def stop_game(text):
    global running
    global music
    sound.pause()
    timer.stop()
    timer2.stop()
    timer3.stop()
    timer4.stop()
    timer5.stop()
    running=False
    music=False
    sound.pause()
    if text!='':
        print('\n')
        if type(text)==list:
            for err in text:
                print(err)
        else:
            print(text)
            print('\n\n')
        
    if type(text)!=list:
        if coins_collected==0:
            print('NO COINS COLLECTED')
            for ln in coin6:
                print((ln+' ')*total_coins)
            print('\n\n\n'+game_end_msg)
            #if no coins collected
            if win:
                clear_sound.play()
            else:
                lose_sound.play()
        else:
            #if some coins collected
            timer7.start()

def generate_error(obj, curr_down, curr_right, curr_list, row, index):
    m_loc='N/A'
    o_loc='N/A'
    try:
        m_loc=matrix_copy[row+curr_down][curr_right+index]
        m_loc='is within range'
    except:
        try:
            m_loc=matrix_copy[row+curr_down]
            m_loc='horizontal index is out of range (width='+str(width)+')'
        except:
            m_loc='vertical index out of range (height='+str(height)+')'
    try:
        o_loc=curr_list[row][index]
        o_loc='is within range'
    except:
        try:
            o_loc=curr_list[row]
            o_loc='horizontal index is out of range (width='+str(len(curr_list[0]))+')'
        except:
            o_loc='vertical index out of range (height='+str(len(curr_list))+')'
            
    build='Error copying '+obj+' to matrix: # matrix '+m_loc+' # object '+o_loc+' # index='+str(index)+' row='+str(row)+' object_down='+str(curr_down)+' object_right='+str(curr_right)
    return build

def remove_coin(coin_id):
    global coin_animation
    global coin_down
    global coin_right
    global coins_collected
    coins_collected+=1
    coin_animation.pop(coin_id)
    coins_down.pop(coin_id)
    coins_right.pop(coin_id)

def add_items(reason):
    global matrix
    global matrix_copy
    global character_animation
    global coin_animation
    global right
    errors=[]
    #walk cycle animation
    if walk_cycle:
        if character_animation==0:
            costume=text2
        elif character_animation==1:
            costume=text3
        elif character_animation==2:
            costume=text4
        elif character_animation==3:
            costume=text5
    else:
        costume=text
    
    reverse_start=len(costume[0])-1
    if reverse==1:
        r=-1
    else:
        r=1
    
    matrix_copy=[row[:] for row in matrix]
    
    #render coins
    if len(coin_animation)!=0:
        coin_id=0
        while coin_id < len(coin_animation):
            #get current costume
            coin_sprite=coin_costumes[coin_animation[coin_id]-1]
            
            #get current position
            coin_down=coins_down[coin_id]
            coin_right=coins_right[coin_id]
            
            collision=is_touching(coin_right,coin_right+len(coin_sprite[0]),coin_down,coin_down+len(coin_sprite))
            if collision:
                remove_coin(coin_id)
                coin_sound.play()
            else:
                #copy sprite into matrix_copy
                row=0
                while row < len(coin_sprite):
                    index=0
                    while index < len(coin_sprite[row]):
                        try:
                            matrix_copy[row+coin_down][coin_right+index]=coin_sprite[row][index]
                        except(IndexError):
                            #error
                            errors.append(generate_error('coin', coin_down, coin_right, coin_sprite, row, index))
                        index+=1
                    row+=1
            coin_id+=1
            
    #render bullets
    if len(bullet_right)!=0:
        bullet_id=0
        restart=False
        while bullet_id < len(bullet_right):
            #move the character to start if touching bullet
            if not restart:
                restart=is_touching(bullet_right[bullet_id],bullet_right[bullet_id]+len(bullet[0]),bullet_down[bullet_id],bullet_down[bullet_id]+len(bullet))
            
            #get current position
            current_bullet_down=bullet_down[bullet_id]
            current_bullet_right=bullet_right[bullet_id]
        
            #copy sprite into matrix_copy
            row=0
            while row < len(bullet):
                index=0
                while index < len(bullet[row]):
                    try:
                        matrix_copy[row+current_bullet_down][current_bullet_right+index]=bullet[row][index]
                    except(IndexError):
                        #error
                        errors.append(generate_error('bullet', current_bullet_down, current_bullet_right, bullet, row, index))
                    index+=1
                row+=1
            bullet_id+=1
        if restart:
            right=1
            
    #render the character
    if hitbox:
        row=0
        costume=costume[:]
        while row<len(costume):
            costume[row]=costume[row].replace('░','▓')
            row+=1
    row=0
    while row < len(text):
        index=0
        while index < len(text[row]):
            try:
                if reverse==1:
                    matrix_copy[row+down][right+index]=costume[row][reverse_start-index]
                else:
                    matrix_copy[row+down][right+index]=costume[row][index]
            except(IndexError):
                #error
                errors.append(generate_error('character', down, right, costume, row, index))
            index+=1
        row+=1
    
    #and finally, render the current frame
    if len(errors)==0:
        render_game()
        #check for story advancements
        story_progress()
    else:
        #fancy new error handling
        if not info:
            render_game()
            print('There was an error, press "i" to enable info')
    
    #show info, if applicable
    if info:
        print('character right:', right, '\tcharacter right2:', right+len(text[0]))
        print('character down: ', down, '\tcharacter down2: ', down+len(text))
        print('screen height:', height, '\tscreen width:', width)
        if len(bullet_right)!=0:
            print('bullet right:', bullet_right)
            print('bullet down: ', bullet_down)
        if len(coin_animation)!=0:
            print('coin animation:', coin_animation)
            print('coin right:', coins_right)
            print('coin down: ', coins_down)
        if len(object_txt)!=0:
            print('object right:', object_right)
            print('object down: ', object_down)
        if len(pop_item)!=0:
            for popped in pop_item:
                print('POPPING ITEM: index=', popped)
        print('this frame was created for:', reason)
        if len(errors)!=0:
            stop_game(errors)

def render_static():
    #render an inanimate object
    index=0
    while index < len(object_txt):
        obj_down=object_down[index]
        obj_right=object_right[index]
        obj=object_txt[index]
        row=0
        while row < len(obj):
            char=0
            while char < len(obj[row]):
                matrix[row+obj_down][obj_right+char]=obj[row][char]
                char+=1
            row+=1
        index+=1

def level_up():
    global level
    global object_txt
    global object_down
    global object_right
    global down
    global right
    global coin_animation
    global coins_down
    global coins_right
    global bullet_down
    global bullet_right
    level+=1
    if level>len(level_contents):
        global win
        win=True
        stop_game('\n\nYOU WIN!')
    else:
        print('\n\nLEVEL UP: LEVEL', level-1) #subtract 1 from level
        right=1
        #load new objects
        object_txt=level_contents[level-1][:]
        object_down=level_down[level-1][:]
        object_right=level_right[level-1][:]
        #remove old objects
        coin_animation=[]
        coins_down=[]
        coins_right=[]
        bullet_down=[]
        bullet_right=[]
        timer4.start()

def is_touching(r1, r2, d1, d2):
    #test for collision with bullet or coin
    user_r1=right
    user_d1=down
    user_r2=right+len(text[0])
    user_d2=down+len(text)
    hit=False
    if user_r2>r1 and not user_r1>r2:
        hit=True
    if user_r1>r2 and not user_r2>r1:
        hit=True
        
    if hit:
        hit=False
        if user_d1<d2 and not user_d2<=d1:
            hit=True
        if user_d2>d1 and not user_d1>=d2:
            hit=True
       
    #return whether there is a collision
    #and the character needs to restart
    return hit

def collide(direction):
    #collision detection
    if not running:
        return False
    no_collision=True
    barriers=['▀', '▄', '█', '▓', '▌', '▐']
    if direction=='up':
        row=matrix[down-1]
        detection=1
    elif direction=='down':
        row=matrix[len(text)+down]
        detection=1
    elif direction=='left':
        column=[i[right] for i in matrix]
        detection=2
    elif direction=='right':
        column=[i[right+len(text[0])] for i in matrix]
        detection=2
    if detection==1:
        row=row[right:right+len(text[0])]
        for each in barriers:
            if each in row:
                no_collision=False   
    else:
        column=column[down:down+len(text)]
        for each in barriers:
            if each in column:
                no_collision=False   
    global blocks
    if blocks>145:
        return True
    elif not no_collision:
        #if colliding
        name='COLLISION()'
        enemy='KEY SPAMMER'
        if blocks==3:
            print('Path is blocked, try hitting the "h" key to see your hitbox')
        elif blocks<5:
            print('Path is blocked')
        elif blocks<10:
            print('I already told you, the path is blocked')
        elif blocks<15:
            print("You can't go this way!")
        elif blocks<20:
            print('Stop it!')
        elif blocks<35:
            print('Path is blocked')
        elif blocks<45:
            print('Aww, I almost had you fooled there.')
        elif blocks<50:
            print("What, so you're just going to sit here spamming the arrow key?")
        elif blocks<65:
            print("Don't make me angry.")
        elif blocks<70:
            print("You know what, take this!")
        elif blocks<95:
            print('\n\n\n\n\n\n\n\n\n\n')
        elif blocks<100:
            print("That didn't even stop you?")
        elif blocks<110:
            print("Fine, you asked for it.")
        elif blocks<=125:
            print("Time to use my WIZARD POWERS!")
        elif blocks==126:
            print(name, 'ATTACKED!')
        elif blocks==127:
            print(name, 'USED GARBLE')
        elif blocks==128:
            total_lines=0
            while total_lines<50:
                build=''
                num_rands=0
                while num_rands<100:
                    build=build+str(randint(0,9))
                    num_rands+=1
                print(build)
                total_lines+=1
        elif blocks==129:
            print("IT'S SUPER EFFECTIVE!")
        elif blocks<=140:
            print(enemy, 'USED SPAM')
        elif blocks==141:
            print("IT'S SUPER EFFECTIVE!")
        elif blocks==142:
            print(name, 'FAINTED!')
        elif blocks==143:
            print(enemy, 'GAINED 100XP')
        elif blocks==144:
            print(enemy, 'LEVELED UP!')
        elif blocks==145:
            print(enemy, 'GAINED ABILITY: WALK THROUGH OBSTACLES')
        else:
            print('?')
        blocks+=1
    elif blocks<=145:
        blocks=0
    return no_collision

def iterate_tutorial():
    #prints out the next item in the tutorial
    global tutorial_counter
    global progress
    global running
    if tutorial_counter<=len(tutorial_text)-1:
        text=tutorial_text[tutorial_counter]
        if type(text)==str:
            if text!='':
                print('\n\n'+text)
    tutorial_counter+=1
    if tutorial_counter>len(tutorial_text):
        quit_tutorial()

def quit_tutorial():
    #quit the tutorial
    global running
    tutorial_frame.stop()
    timer6.start()
    running=True
    remove_item(0,True)
    create_frame()

def timer_handler():
    if running:
        timer2.start()
    timer.stop()

def timer2_handler():
    #simulates repeated keypresses if the key is held down
    global down
    global right
    global vertical_held
    global horizontal_held
    
    #use the code below instead of calling key_handler(),
    #because that function restarts the timer
    
    #code could be refactored to pass whether keypress is simulated
    #to key_handler() to require less code. The function would
    #only start timer if called by real keypress.
    if not running:
        timer2.stop()
    tmpright=right
    tmpdown=down
    if vertical_held!=False:
        if vertical_held==1:
            if down!=0:
                if collide('up'):
                    down-=1
                else:
                    vertical_held=False
            else:
                vertical_held=False
        else:
            if down!=height-len(text):
                if collide('down'):
                    down+=1
                else:
                    vertical_held=False
            else:
                vertical_held=False
    if horizontal_held!=False:
        if horizontal_held==1:
            if right!=1:
                if collide('left'):
                    right-=1
                else:
                    horizontal_held=False
            else:
                horizontal_held=False
        else:
            if right!=width-len(text[0])+1:
                if collide('right'):
                    right+=1
                else:
                    horizontal_held=False
            else:
                horizontal_held=False
                #level up if at the edge
                level_up()
    if tmpright!=right or tmpdown!=down:
        print('Loading, please wait')
        walk()
        add_items('long keypress')

def timer3_handler():
    #clears the debris cloud after an object is destroyed
    global pop_item
    if len(pop_item)==1:
        timer3.stop()
    remove_item(pop_item[0], False)
    pop_item.pop(0)

def timer4_handler():
    #loads the new level
    timer4.stop()
    clear_matrix()
    render_static()
    add_items('load new level')
    print(' '*(level_widths[level-2]-30), 'Scroll to the left\n\n')

def timer5_handler():
    #animates coins and moves bullets
    global coin_animation
    global bullet_right
    if len(coin_animation)==0 and len(bullet_right)==0:
        #stop if unneeded
        timer5.stop()
    else:
        #animates coins
        if len(coin_animation)!=0:
            current=0
            while current<len(coin_animation):
                if coin_animation[current]==len(coin_costumes):
                    coin_animation[current]=1
                else:
                    coin_animation[current]=coin_animation[current]+1
                current+=1
        
        #animates bullets
        if len(bullet_right)!=0:
            current=0
            while current<len(bullet_right):
                current_right=bullet_right[current]-2
                if current_right<=-17:
                    current_right=width-len(bullet[0])
                bullet_right[current]=current_right
                current+=1
        #render
        add_items('animation')

def timer6_handler():
    #plays music at the start of the game
    if music:
        sound.play()
        
def timer7_handler():
    #displays coins at the end of the game
    global coin_counter
    coin_counter+=1
    lines=['','','']
    
    if coin_counter<=coins_collected:
        c=0
        while c<3:
            #add the normal coins
            lines[c]+=(coin5[c]+' ')*coin_counter
            #add blank coins
            lines[c]+=(coin6[c]+' ')*(total_coins-coin_counter)
            c+=1
        
        coin_sound.play()
        #print('\n\n\n\n\n\n\n\n\n\n\n\n')
        for e in lines:
            print(e)
        
    if coin_counter>=coins_collected+2:
        timer7.stop()
        if win:
            if coins_collected==total_coins:
                win_sound.play()
                print('\nALL COINS COLLECTED')
            else:
                clear_sound.play()
        else:
            lose_sound.play()
        print('\n\n'+game_end_msg)

def timer8_handler():
    #shows tutorial
    iterate_tutorial()
    if tutorial_counter==4:
        global tutorial_frame
        tutorial_frame=simplegui.create_frame('Click the box to use the keyboard', 100, 100)
        tutorial_frame.add_label('Press space to advance the tutorial')
        tutorial_frame.add_label('Press "q" to quit the tutorial')
        tutorial_frame.set_keydown_handler(key_handler2)
        timer8.stop()

def release_handler(key):
    global vertical_held
    global horizontal_held
    #handles key releases
    if key==upkey or key==downkey:
        vertical_held=False
    if key==leftkey or key==rightkey:
        horizontal_held=False
    if vertical_held==False and horizontal_held==False:
        timer.stop()
        timer2.stop()

def key_handler(key):
    #handles user keypresses
    start_time=time()
    global down
    global right
    global vertical_held
    global horizontal_held
    global reverse
    tmpright=right
    tmpdown=down
    if running:
        if key==upkey:
            if down!=0:
                if collide('up'):
                    down-=1
                    vertical_held=1
        elif key==downkey:
            if down!=height-len(text):
                if collide('down'):
                    down+=1
                    vertical_held=2
        elif key==leftkey:
            if right!=1:
                if collide('left'):
                    right-=1
                    horizontal_held=1
                reverse=1
        elif key==rightkey:
            if right!=width-len(text[0])+1:
                if collide('right'):
                    right+=1
                    horizontal_held=2
                reverse=0
            else:
                #level up if at the edge
                level_up()
                
        elif key==m_key:
            global music
            music=not music
            if music:
                sound.play()
            else:
                sound.pause()
        elif key==w_key:
            global walk_cycle
            walk_cycle=not walk_cycle
            add_items('enable/disable walk cycle')
        elif key==i_key:
            global info
            info=not info
            add_items('enable/diasble info')
        elif key==t_key:
            global show_time
            show_time=not show_time
        elif key==s_key:
            global win
            win=False
            stop_game('')
        elif key==h_key:
            global hitbox
            hitbox=not hitbox
            add_items('enable/disable hitbox')
        elif key==p_key:
            global printall
            printall=not printall
    
    if tmpright!=right or tmpdown!=down:
        print('Loading, please wait')
        walk()
        add_items('move character')
        timer.start()
        end_time=time()
        time_taken=end_time-start_time
        time_list.append(time_taken)
        if show_time:
            print('current lag:', time_taken)
            avg=0
            for item in time_list:
                avg+=item
            if len(time_list)!=0:
                avg=avg/len(time_list)
                print('average lag:', avg)
            else:
                print('No time data yet, try moving the character')

def key_handler2(key):
    #handles keypresses for tutorial
    if level==1:
        if key==spacekey:
            #advance in the tutorial
            iterate_tutorial()
        if key==q_key:
            quit_tutorial()

def destroy_item(l_index):
    #creates debris
    global cloud
    build_destroyed=[]
    txt=0
    for item in object_txt[l_index]:
        build_destroyed.append('▓'*len(item))
    cloud=build_destroyed[:]

def remove_item(l_index, destroy):
    #removes an object from the screen
    global object_txt
    global object_down
    global object_right
    global matrix
    global pop_item
    clear_matrix()
    if destroy:
        pop_item.append(l_index)
        destroy_item(l_index)
        object_txt[l_index]=cloud
        if len(pop_item)==1:
            timer3.start()
    else:
        object_txt.pop(l_index)
        object_down.pop(l_index)
        object_right.pop(l_index)
    render_static()
    if destroy:
        add_items('destroy item (create debris)')
    else:
        add_items('pop item/remove debris')

def create_coins(tmp_animation, tmp_right, tmp_down):
    #create a coin
    global coin_animation
    global coins_down
    global coins_right
    start_timer=len(coin_animation)==0 and len(bullet_right)==0
    
    coin_animation.append(tmp_animation)
    coins_right.append(tmp_right)
    coins_down.append(tmp_down)
    
    if start_timer:
        timer5.start()
        
def place_coins(r1, r2, d1, d2, times):
    #make some coins in the area provided
    #not currently in use
    coin_counter=0
    while coin_counter<times:
        tmp_animation=randint(1,len(coin_costumes))
        tmp_right=randint(r1,r2)
        tmp_down=randint(d1,d2)
        create_coins(tmp_animation, tmp_right, tmp_down)
        coin_counter+=1

def create_bullets(r,d):
    global bullet_down
    global bullet_right
    #make a bullet
    bullet_right.append(r)
    bullet_down.append(d)
    if len(bullet_down)==0:
        timer5.start()

def button_handler(button_id):
    if running:
        global progress
        if button_id==1:
        #pick up hammer
            if progress==1:
                if down==14 and right==26:
                    progress=2
                    button=frame.add_button('Hammer', button2_press)
                    remove_item(1, False)
                    powerup_sound.play()
                else:
                    print('Nothing to pick up, move to the end of the hammer handle')
            else:
                print('Nothing to pick up')
        #use hammer
        elif button_id==2:
            if progress==2:
                if right==54:
                    #hit goomba
                    remove_item(0, True)
                    progress=3
                    hit_sound.play()
                    right1=object_right[0]
                    right2=object_right[0]+len(goomba[0])
                    down1=object_down[0]
                    down2=object_down[0]+len(goomba)-len(coin1)
                    create_coins(randint(1,len(coin_costumes)), right1, down1)
                    create_coins(randint(1,len(coin_costumes)), right2, down1)
                    create_coins(randint(1,len(coin_costumes)), right1, down2)
                    create_coins(randint(1,len(coin_costumes)), right2, down2)
                    create_coins(randint(1,len(coin_costumes)), round(right1+((right2-right1)/2)), round(down1+((down2-down1)/2)))
                else:
                    print('Nothing to hit')
                    
            elif level==3:
                if right==4 and 0<down<8:
                    if progress==3:
                        progress=4
                        #hit treasure chest
                        right1=object_right[0]
                        right2=object_right[0]+len(chest[0])
                        down1=object_down[0]
                        down2=object_down[0]+len(chest)
                        remove_item(0, True)
                        
                        #place the coins
                        create_coins(randint(1,len(coin_costumes)), right1+3, down1)
                        create_coins(randint(1,len(coin_costumes)), right2, down2)
                        create_coins(randint(1,len(coin_costumes)), right1, down2)
                        
                        #syntax: create_bullets(right, down)
                        create_bullets(85,0)
                        create_bullets(45,15)
                        create_bullets(31,20)
                        hit_sound.play()
                    else:
                        print('Nothing to hit')
                else:
                    print('Nothing to hit')
            else:
                print('Nothing to hit')

def button1_press():
    button_handler(1)
    
def button2_press():
    button_handler(2)
        
def story_progress():
    global progress
    if level==1:
        if progress==-1:
            global running
            progress=0
            running=False
            timer8.start()
    elif level==2:
        if down>=10:
            if progress==0:
                button=frame.add_button('Pick up item', button1_press)
                progress=1

def create_frame():
    global frame
    frame=simplegui.create_frame('Click the box, then use arrow keys to move', 100, 100)
    frame.set_keydown_handler(key_handler)
    frame.set_keyup_handler(release_handler)
    frame.start()

print('Loading...')

#code is below costumes

text="""░░░░░░░▄▄▄▄░░░░░
░░░░▄▀▀░░░▀█░░░░
░░▄▀░░▄██████▄░░
░▄█▄█▀░░▄░▄░█▀░░
▄▀░██▄░░▀░▀░▀▄░░
▀▄░░▀░▄█▄▄░░▄█▄░
░░▀█▄▄░░▀▀▀█▀░░░
░▄▀░░░▀██▀▀█▄▀▀▄
█░░▄▀▀▀▄█▄░░▀█░█
▀▄█░░░░░█▀▀▄▄▀█░
░▄▀▀▄▄▄██▄▄█▀░░█
█▀░█████████░░░█
█░░██▀▀▀░░░▀▄▄█▀
░▀▀░░░░░░░░░░░░░""".split('\n') #Used when walk cycle is disabled,
                                #exactly the same costume as text2

text2="""░░░░░░░▄▄▄▄░░░░░
░░░░▄▀▀░░░▀█░░░░
░░▄▀░░▄██████▄░░
░▄█▄█▀░░▄░▄░█▀░░
▄▀░██▄░░▀░▀░▀▄░░
▀▄░░▀░▄█▄▄░░▄█▄░
░░▀█▄▄░░▀▀▀█▀░░░
░▄▀░░░▀██▀▀█▄▀▀▄
█░░▄▀▀▀▄█▄░░▀█░█
▀▄█░░░░░█▀▀▄▄▀█░
░▄▀▀▄▄▄██▄▄█▀░░█
█▀░█████████░░░█
█░░██▀▀▀░░░▀▄▄█▀
░▀▀░░░░░░░░░░░░░""".split('\n')

text3="""░░░░░░░▄▄▄▄░░░░░
░░░░▄▀▀░░░▀█░░░░
░░▄▀░░▄██████▄░░
░▄█▄█▀░░▄░▄░█▀░░
▄▀░██▄░░▀░▀░▀▄░░
▀▄░░▀░▄█▄▄░░▄█▄░
░░▀█▄▄░░▀▀▀█▀░░░
░▄▀░░░▀██▀▀█▄▀▀▄
█░░▄▀▀▀▄█▄░░▀█░█
▀▄█░░░░░█▀▀▄▄█▀░
░▄▀▀▄▄▄██▄▄█▀░░░
█▀░██████████▄░░
█░░██▀▀▀░█░░░░█░
░▀▀░░░░░░▀▀▀▀▀▀░""".split('\n')

text4="""░░░░░░░▄▄▄▄░░░░░
░░░░▄▀▀░░░▀█░░░░
░░▄▀░░▄██████▄░░
░▄█▄█▀░░▄░▄░█▀░░
▄▀░██▄░░▀░▀░▀▄░░
▀▄░░▀░▄█▄▄░░▄█▄░
░░▀█▄▄░░▀▀▀█▀░░░
░▄▀░░░▀██▀▀█▄▀▀▄
█░░▄▀▀▀▄█▄░░▀█░█
▀▄█░░░░░█▀▀▄▄█▀░
░░██▄▄▄██▄▄█▀░░░
░░█████▄███▄░░░░
░░█░░░░░█░░░█░░░
░░▀▀▀▀▀▀▀▀▀▀▀░░░""".split('\n')

text5="""░░░░░░░▄▄▄▄░░░░░
░░░░▄▀▀░░░▀█░░░░
░░▄▀░░▄██████▄░░
░▄█▄█▀░░▄░▄░█▀░░
▄▀░██▄░░▀░▀░▀▄░░
▀▄░░▀░▄█▄▄░░▄█▄░
░░▀█▄▄░░▀▀▀█▀░░░
░▄▀░░░▀██▀▀█▄▀▀▄
█░░▄▀▀▀▄█▄░░▀█░█
▀▄█░░░░░█▀▀▄▄▀█░
░░██▄▄▄██▄▄█▀░░█
░░██████▀▀▀█░░░█
░░█░░░░░█░░▀▄▄█▀
░░▀▀▀▀▀▀▀░░░░░░░""".split('\n')

goomba="""░░░░░░░░░░░░░░▄▄▀▀▀▀▀▀▀▀▄▄░░░░░░░░░░░░░░
░░░░░░░░░▄██▄▀▓▓▓▓▓▓▓▓▓▓▓▓▀▄██▄░░░░░░░░░
░░░░░░░░░░░███▓▓▓▓▓▓▓▓▓▓▓▓███░░░░░░░░░░░
░░░░░░░░░░█▓▀██▓▓▓▓▓▓▓▓▓▓██▀▓█░░░░░░░░░░
░░░░░░░░░█▓▓▓▄██▄▓▓▓▓▓▓▄██▄▓▓▓█░░░░░░░░░
░░░░░░░░▄▀▓▄▀░░▀█▄▓▓▓▓▄█▀░░▀▄▓▀▄░░░░░░░░
░░░░░░░▄▀▓▄▀░░░▄░██▓▓██░▄░░░▀▄▓▀▄░░░░░░░
░░░░░▄▀▓▓▓█░░░███░█▓▓█░███░░░█▓▓▓▀▄░░░░░
░░░▄▀▓▓▓▓▓█░░░░▀░░█▓▓█░░▀░░░░█▓▓▓▓▓▀▄░░░
░▄▀▓▓▓▓▓▓▓█░░░░░░█▓▓▓▓█░░░░░░█▓▓▓▓▓▓▓▀▄░
█▓▓▓▓▓▄▓▓▓▓▀▄▄▄▄▀▓▓▓▓▓▓▀▄▄▄▄▀▓▓▓▓▄▓▓▓▓▓█
█▓▓▓▓▓▌▀▄▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▄▀▐▓▓▓▓▓█
█▓▓▓▓▐▄▄▄█▄▄▄▄▄▀▀▀▀▀▀▀▀▀▀▄▄▄▄▄█▄▄▄▌▓▓▓▓█
█▓▓▓▓▀▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▀▓▓▓▓█
░▀▄▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▄▀░
░░░▀▀▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▀▀░░░
░░░░░░░░░░░█░░░░░░░░░░░░░░░░█░░░░░░░░░░░
░░░░░░░░░░░█░░░░░░░░░░░░░░░░█░░░░░░░░░░░
░░░░░░░░░░░█░░░░░░░░░░░░░░░░█░░░░░░░░░░░
░░░░░░░░░░░█░░░░░░░░░░░░░░░░█░░░░░░░░░░░
░░░░░░░░░░░█░░░░░░░░░░░░░░░░█░░░░░░░░░░░
░░░░░░░▄▄▀▀▀▀▄░░░░░░░░░░░░▄▀▀▀▀▄▄░░░░░░░
░░░░░▄▀▓▓▓▓▓▓▓▀▄▄▄▄▄▄▄▄▄▄▀▓▓▓▓▓▓▓▀▄░░░░░
░░░░░█▓▓▓▓▓▓▓▓▓▓▓▄▀░░▀▄▓▓▓▓▓▓▓▓▓▓▓█░░░░░
░░░░░░▀▄▓▓▓▓▓▓▓▄▀░░░░░░▀▄▓▓▓▓▓▓▓▄▀░░░░░░
░░░░░░░░▀▀▀▀▀▀▀░░░░░░░░░░▀▀▀▀▀▀▀░░░░░░░░""".split('\n')

mallot="""░░░░░░░░░░░▐▓▓▓▓▓▌
░░░░░░░░░░░▐▓▓▓▓▓▌
▐███████████▓▓▓▓▓█
░░░░░░░░░░░▐▓▓▓▓▓▌
░░░░░░░░░░░▐▓▓▓▓▓▌""".split('\n')

chest="""░░░░▄▀▀▀▀▀▀▀▀▄░░░░
░░▄▀░░░░░░░░░░▀▄░░
▄▀░░░░░░░░░░░░░░▀▄
█░░░░░░░░░░░░░░░░█
█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
█░░░░░░░░░░░░░░░░█
█░░░░░░▄▄▄▄░░░░░░█
█░░░░░▐░░░░▌░░░░░█
█░░░░░░▀▀▀▀░░░░░░█
█░░░░░░░░░░░░░░░░█
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀""".split('\n')

coin1="""░░▄▄░
░▐░░▌
░░▀▀░""".split('\n')

coin2="""░░▄░░
░▐░▌░
░░▀░░""".split('\n')

coin3="""░░▄░░
░░█░░
░░▀░░""".split('\n')

coin4="""░▄▄░░
▐░░▌░
░▀▀░░""".split('\n')

coin5=""" ▄▄ 
▐░░▌
 ▀▀ """.split('\n') #shows at the end

coin6=""" ▄▄ 
▐--▌
 ▀▀ """.split('\n') #shows at the end

sign="""░░░░░░▄░░░░░░
▐▓▓▓░▓▓▓▓▓░▓▌
▐▓▓░▓▓▓░▓▓▓▓▌
▐░▓▓▓░▓▓▓░▓▓▌
░░░░░░█░░░░░░
░░░░░░█░░░░░░
░░░░░░█░░░░░░
""".split('\n')

bullet="""░░░░▄▄█▀▀▀▀▀█▄▀▀
░▄██▀█▄██████▄██
▄▀█░░███████████
█▄▄▄██▀▀█░░▀████
▀████░░░░░░▄████
░▀████▄▄▄███████
░░░░▀▀██████▀▀██""".split('\n') #len[0]=16

cloud=[]

coin_animation=[]
coin_costumes=[coin1,coin2,coin3,coin2,coin4,coin2,coin3,coin2]

level_contents=[[sign],[goomba, mallot], [chest]]
level_down=[[9],[1, 20],[5]]
level_right=[[30],[70, 42],[20]]

import simplegui
from time import time
from random import randint
matrix=[]
matrix_copy=[]
vertical_held=False
horizontal_held=False
time_list=[]
reverse=0
blocks=0
character_animation=0
coins_collected=0
coin_counter=0
total_coins=8
tutorial_text=["\n\n\n\nHi there! It's me, Bill Board.", "I bet you could use some help!", 'To take the tutorial, press the spacebar. Otherwise, press the "q" key.', '', "Great, let's get started! Press space whenever you want to advance the tutorial.", 'In this game, you can use the up, down, left, and right arrows to move.', 'To continue to the next level, move to the right until you reach the end.', 'In the game, there will also be objects you can pick up.', 'To pick up objects, move your character so that your hand is touching the handle of the object.', 'Then press the button that says "pick up item" to grab it.', 'You do not need to do this for coins, which will be picked up automatically when you touch them.', 'If you find a hammer, you can hit obstacles by pressing the button labeled "hammer".', 'The hammer will not work on bullets.', 'If you are hit by a bullet, you will be teleported back to the start of the level.', "That's all for the tutorial, have fun!"]		#
tutorial_counter=0
game_end_msg='\n\nGAME ENDED. Scroll up to view previous frames.'
running=True
music=True
show_time=False
walk_cycle=True
hitbox=False
info=False
printall=False
win=False
progress=-1
pop_item=[]

coins_down=[]
coins_right=[]

bullet_down=[]
bullet_right=[]

#this should be set to 1 by default
level=1

#objects in the current level
#to modify, change the level_contents list above
object_txt=level_contents[level-1][:]
object_down=level_down[level-1][:]
object_right=level_right[level-1][:]

#how large the screen is
level_widths=[50, 140, 101]
width=0
height=28

clear_matrix()

down=int(round((len(matrix)-len(text))/2))
right=1

m_key=simplegui.KEY_MAP['m']
t_key=simplegui.KEY_MAP['t']
w_key=simplegui.KEY_MAP['w']
i_key=simplegui.KEY_MAP['i']
s_key=simplegui.KEY_MAP['s']
h_key=simplegui.KEY_MAP['h']
p_key=simplegui.KEY_MAP['p']
q_key=simplegui.KEY_MAP['q']
spacekey=simplegui.KEY_MAP['space']
leftkey=simplegui.KEY_MAP['left']
rightkey=simplegui.KEY_MAP['right']
upkey=simplegui.KEY_MAP['up']
downkey=simplegui.KEY_MAP['down']

frame=''
tutorial_frame=''
if not level==1:
    create_frame()
    timer6.start()

sound=simplegui.load_sound('https://ia800504.us.archive.org/15/items/SuperMarioBros.ThemeMusic/SuperMarioBros.mp3')
hit_sound=simplegui.load_sound('https://d1490khl9dq1ow.cloudfront.net/sfx/mp3preview/rubber-mallet-drop-1_M1jQGMVu.mp3')
coin_sound=simplegui.load_sound('https://themushroomkingdom.net/sounds/wav/smw/smw_coin.wav')
#cleared the game, all coins collected
win_sound=simplegui.load_sound('https://themushroomkingdom.net/sounds/wav/smb/smb_world_clear.wav')
#cleared the game, not all coins colleted
clear_sound=simplegui.load_sound('https://themushroomkingdom.net/sounds/wav/smb/smb_stage_clear.wav')
#exited the game
lose_sound=simplegui.load_sound('https://themushroomkingdom.net/sounds/wav/smb/smb_gameover.wav')
powerup_sound=simplegui.load_sound('https://themushroomkingdom.net/sounds/wav/smb/smb_powerup.wav')

#starts timer 2
timer = simplegui.create_timer(300, timer_handler)
#automatic keypress
timer2 = simplegui.create_timer(100, timer2_handler)
#clears debris cloud
timer3 = simplegui.create_timer(500, timer3_handler)
#starts new level
timer4 = simplegui.create_timer(500, timer4_handler)
#animates coins and moves bullets
timer5 = simplegui.create_timer(500, timer5_handler)
#starts music
timer6 = simplegui.create_timer(2000, timer6_handler)
#adds up coins at end
timer7 = simplegui.create_timer(500, timer7_handler)
#tutorial
timer8 = simplegui.create_timer(1500, timer8_handler)

render_static()
add_items('beginning frame (you should not be able to see this, make sure info variable is set to False by default)')

#if the user wants to start at a different level
if level==2:
    progress=0
elif level>2:
    button=frame.add_button('Pick up item', button1_press)
    button=frame.add_button('Hammer', button2_press)
    progress=3

if level==1:
    print('\nTUTORIAL')
else:
    print('\nLEVEL', level)
