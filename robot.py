import PIL.ImageGrab
from PIL import Image
import time
import win32api
import win32con
zero_count = 0
while True:
        time.sleep(0.2)
        im = PIL.ImageGrab.grab()
        #im.show()
        #im.save('example.bmp')
        #im = Image.open('example.bmp')
        #nim = im.crop((929,72,1338,481))
        def getGrid(im,x,y):
                startx = 930
                starty = 72
                r = 51
                g = 0
                b = 0
                #nim = im.crop((startx+x*r,starty+y*r,startx+x*r+r,starty+y*r+r))
                for i in range(startx+x*r+5,startx+x*r+15):
                        for j in range(starty+y*r+20,starty+y*r+30):
                                p = im.getpixel((i,j))
                                g = g + p[1] - p[0]
                                b = b + p[2] - p[0]
                return (g,b)
                                
        startx = 930
        starty = 72
        r = 51
        #center from k-means
        center = [[  93.53772622,  151.93638933],
       [ -17.54040123, -101.41988675],
       [ -87.86378427,   25.91097952],
       [ 118.8733442 ,  -43.85132179],
       [-112.49430466, -147.50353961],
       [  -1.04022727,   -2.59401229]]
        m = [[-1 for col in range(8)] for row in range(8)]  
        for x in range(8):
                for y in range(8):
                        g = getGrid(im,x,y)
                        min = 1000000
                        for i in range(6):
                                tmin = (g[0]/100 - center[i][0])**2 + (g[1]/100 - center[i][1])**2
                                if tmin < min:
                                        m[y][x] = i
                                        min = tmin
                        if min > 400: #uncertern
                                m[y][x] = -1
                        

        def test_click(l,m,c,x,y,px,py):
                startx = 930
                starty = 72
                r = 51
                if c==-1 or x<0 or y<0 or px<0 or py<0:
                        return
                if m[x][y] == c:
                        l.append((x,y,px,py))
                        print("(%d,%d)->(%d,%d)"%(x,y,px,py))
        l = []
        for x in range(8):
                for y in range(7,-1,-1):
                        c = m[x][y]
                        try:
                                if m[x+1][y] == c:
                                        test_click(l,m,c,x+3,y,x+2,y)
                                        test_click(l,m,c,x+2,y-1,x+2,y)
                                        test_click(l,m,c,x+2,y+1,x+2,y)
                                if y > 0 and m[x][y-1] == c:
                                        test_click(l,m,c,x,y-3,x,y-2)
                                        test_click(l,m,c,x-1,y-2,x,y-2)
                                        test_click(l,m,c,x+1,y-2,x,y-2)
                                if m[x+2][y] == c:
                                        test_click(l,m,c,x+1,y+1,x+1,y)
                                        test_click(l,m,c,x+1,y-1,x+1,y)
                                if y > 1 and m[x][y-2] == c:
                                        test_click(l,m,c,x-1,y-1,x,y-1)
                                        test_click(l,m,c,x+1,y-1,x,y-1)
                        except IndexError:
                                pass
        print(l)
        if not len(l):
                zero_count = zero_count + 1
                if zero_count == 3:
                        win32api.keybd_event(90,0,0,0) #z键位码是90  
                        win32api.keybd_event(90,0,win32con.KEYEVENTF_KEYUP,0)  
                        print('z')
                continue
        else:
                zero_count = 0
        import random
        t = random.choice(l)
        print(t)
        win32api.SetCursorPos([startx+t[1]*r+25,starty+t[0]*r+25])    #为鼠标焦点设定一个位置
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0) 
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
        #time.sleep(0.1)
        win32api.SetCursorPos([startx+t[3]*r+25,starty+t[2]*r+25])    #为鼠标焦点设定一个位置
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0) 
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
        win32api.SetCursorPos([300,300])        
                  
          

