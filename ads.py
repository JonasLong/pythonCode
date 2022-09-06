#Displays fake ads

#Sometimes simplegui fails to load images when opening them for
#the first time in a new session. To fix this, you have to run the
#program multiple times until the images show up.

from random import randint as r
import simplegui

#dependencies:
import weather as w


class ad_displayer:
    max_len=70
    init=False
    spaces=0
    
    @classmethod
    def initalize(cls):
        cls.init=True
        print('\n\n'+'#'*cls.max_len)
        cls.dynamic_ads=0
        cls.split('Ads keep us free. To remove ads, please upgrade to the premium version by leaving $5.00 in an unmarked envelope within a 5 mile radius of our main office in Anchorage, Alaska.\n')
        
        #Static ads:
        cls.static_ads=[]
        cls.app('Hello. I am Mr. Yappers, manager of Yappers Pet Store.\nI am writing to ask you for your help. After an incident with contaminated dog food, we have had to throw away our entire dog food lineup. This has cost us severely. If we do not obtain $1,000 USD within the next week, our store will, sadly, have to close and we will no longer be able to serve our dedicated customers. That is why I need YOUR help to keep Yappers Pet Store open. If you are able, please send as much as money as possible to our store on 573 Milky Wy. by this weekend.\nPlease act quickly so that we can continue to stay in business!\n\nSincerely,\nMr Yappers.')
        cls.app("Yenom Srelaets: We offer the best products for the lowest price, at a value our competitors can't match.\n\nVisit us online at:\ngoogle.com")
        cls.app("Ad sponsored by Goggle: Buy one laptop for the price of two, and get one free! You don't want to miss out on this great deal! Buy now!\n(All your friends are doing it, it'll make you look cool)")
        cls.app("Introducing Genome, the world's first combination DNA and code editor. Find out more!")
        cls.app("Need an app? Chances are, we have what you're looking for. Choose from a selection of twelve unique apps in categories ranging from games to productivity.")
        cls.app("Here is today's weather, courtesy of Weather Helper. For all of your weather-related home and auto needs, choose from our extensive line of Weather Helper products!\n\n"+w.forecast('your area'))
        cls.app('Interested in advertising here?\nChoose from picture ads, text ads, or even dynamic ads that allow code execution!\n\nContact us during normal business hours to learn about pricing options.')
        
        #Picture ads:
        cls.picture_ads='''https://i.imgur.com/Q9IVx37.png
        https://i.imgur.com/xSPMOZt.png
        https://what-if.xkcd.com/imgs/a/44/high_throw_5.png'''.replace(' ', '').split('\n')
        for ind, itm in enumerate(cls.picture_ads):
            print(itm)
            cls.picture_ads[ind]=cls.load(itm)
        cls.static_ads=[]
        cls.picture_titles=['Buy yours now!', 'Go to the internet now to learn more.', 'order your giraffe stacks now']
        cls.max_ads=len(cls.static_ads)+cls.dynamic_ads+len(cls.picture_ads)
    
    @classmethod
    def main(cls, num=0, max_char_len='', offset='', *args, **kwargs):
        if not max_char_len=='':
            try:
                cls.max_len=int(max_char_len)
            except:
                print('invalid character length')
        if not offset=='':
            try:
                cls.spaces=int(offset)
            except:
                print('invalid offset value')
        if not cls.init:
            cls.initalize()
        try:
            num=int(num)
            if num<0:
                num=0
        except:
            num=0
        if num==0:
            cls.split('0 ads displayed')
        
        num=min(num, cls.max_ads)
        choices=[]
                
        if num==cls.max_ads:
            #if max ads are required, display all ads
            z=0
            while z<cls.max_ads:
                choices.append(z)
                z+=1
        else:
            #pick random ads
            i=0
            while i<num:
                choice=r(1, cls.max_ads)
                if not choice in choices:
                    choices.append(choice)
                    i+=1
                    
        for item in choices:
            if item<len(cls.static_ads):
                cls.static(item)
            elif item<len(cls.static_ads)+cls.dynamic_ads:
                cls.dynamic(item-len(cls.static_ads)+1)
            elif item<=len(cls.static_ads)+cls.dynamic_ads+len(cls.picture_ads):
                cls.picture(item-len(cls.static_ads)-cls.dynamic_ads-1)
            else:
                print('none', item)
    
    @classmethod
    def split(cls, text, brk=False, delim=' ', return_info=False):
        if brk==True:
            print('\n'+'#'*cls.max_len)
        #splits lines of text so they fit on the screen
        if '\n' in text:
            #in case there is a newline char,
            #break the list apart and split
            #each segment seperately
            lst=text.split('\n')
            lst=lst[0].split(delim)
            flag=True
        else:
            lst=text.split(delim)
            flag=False
        newstr=['']
        currentbuild=0
        currentwordindex=0
        run=True
        while run:
            if currentwordindex>len(lst)-1:
                run=False
            else:
                old=newstr[currentbuild]
                new=lst[currentwordindex]
                total=len(old)+len(new)+1
                long=len(new)>=cls.max_len
                force=long and old==''
                if long and '/' in new and delim!='/':
                    data=cls.split(new, False, '/', True)
                    for split_line in data:
                        newstr.append(split_line+'/')
                        currentbuild+=1
                elif total>cls.max_len and not force:
                    newstr.append(new)
                    currentbuild+=1
                else:
                    if old=='':
                        newstr[currentbuild]=new
                    else:
                        newstr[currentbuild]=old+delim+new
                currentwordindex+=1
        
        if not return_info:
            for item in newstr:
                if cls.spaces!=0:
                    #must be spaces, not delim, this is for offset
                    print(cls.spaces*' '+item)
                else:
                    print(item)
            
            if flag:
                #call split for each line
                for item in text.split('\n')[1:]:
                    cls.split(item)
        else:
            return newstr
    
    @classmethod
    def app(cls, item):
        cls.static_ads.append(item)
    
    @classmethod
    def static(cls, item):
        cls.split(cls.static_ads[item], True)
    
    @classmethod
    def dynamic(cls, item):
        if item==1:
            #cls.split("hi\n", True)
            #cls.split(w.forecast('your area'))
            print('dynamic1')
        elif item==2:
            cls.split('lalala', True)
        else:
            print('N/A')
    
    @classmethod
    def picture(cls, item):
        img=cls.picture_ads[item]
        title=cls.picture_titles[item]
        _pic(img, title)
    
    @classmethod
    def load(cls, img, new=0):
        error=0
        try:
            img2=simplegui.load_image(img)
        except:
            error=1
                
        if img2.get_width()==0:
            error=2
        else:
            return img2
            
        #if there is an error
        if error!=0:
            if error==1:
                print('Exception while loading')
            else:
                print('Image size is 0')
            if new<5:
                if new==3:
                    print('Could not load, loading the error image', new, img)
                    cls.load(_pic.err_img, new+1)
                    
                else:
                    print('Error loading, retrying', new, img)
                    cls.load(img, new+1)
                    
            else:
                print('Could not load any image', new, img)
                return img


class _pic:
    index=0
    err_img='https://ih0.redbubble.net/image.485923660.1240/ap,550x550,12x16,1,transparent,t.u1.png'
    
    def __init__(self, img, title, height=400, width=400):
        
        def draw(canvas, *args):
            #canvas.draw_image(image, center_source, width_height_source, center_dest, width_height_dest)
            canvas.draw_image(img, (img.get_width()/2, img.get_height()/2), (img.get_width(), img.get_height()), (height/2, width/2), (height, width))
            #print('exception, size is', self.image.get_width(), self.image.get_height())
        
        self.image=img
        self.height=height
        self.width=width
        self.frame=simplegui.create_frame(title,self.height,self.width)
        self.frame.set_canvas_background('White')
        _pic.index+=1
        self.frame.set_draw_handler(draw)
        self.frame.start()
        

def show_ad(num=0, max_len='', offset='', *args, **kwargs):
    #call ad displayer with number of ads to display
    ad_displayer.main(num, max_len, offset)

def disp_help():
    #show documentation
    print("""This incident has been reported, help is on the way!""")

def init():
    pass

ad_displayer.initalize()
#ad_displayer.max_ads
show_ad(3)

